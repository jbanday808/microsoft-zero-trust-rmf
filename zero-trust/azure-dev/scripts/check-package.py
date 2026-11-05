#!/usr/bin/env python3
"""Offline checks for the EZTA DEV package. Does not validate a live deployment."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[1]
errors = []
checks = 0


def require(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def read_json(relative):
    try:
        return json.loads((PACKAGE / relative).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f'{relative}: {exc}')
        return {}


def resource(template, kind, name=None):
    values = [r for r in template.get('resources', []) if r.get('type') == kind and (name is None or r.get('name') == name)]
    require(len(values) == 1, f'Expected one resource: {kind} {name or ""}')
    return values[0] if len(values) == 1 else {}


def check_arm_expression_strings(value, path='root'):
    # Detect unclosed delimiters and quoted strings, including escaped ARM quotes.
    # This is a lexical check, not a replacement for Azure validation/what-if.
    if isinstance(value, dict):
        for key, child in value.items():
            check_arm_expression_strings(child, path + '.' + key)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            check_arm_expression_strings(child, f'{path}[{i}]')
    elif isinstance(value, str) and value.startswith('[') and not value.startswith('[['):
        require(value.endswith(']'), f'Unclosed ARM expression: {path}')
        quoted = False
        depth = 0
        i = 1
        while i < len(value) - 1:
            char = value[i]
            if char == "'":
                if quoted and i + 1 < len(value) - 1 and value[i + 1] == "'":
                    i += 2
                    continue
                quoted = not quoted
            elif not quoted:
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                    require(depth >= 0, f'Unexpected closing parenthesis: {path}')
            i += 1
        require(not quoted and depth == 0, f'Unbalanced ARM expression: {path}')


def main():
    all_json = list(PACKAGE.rglob('*.json'))
    for path in all_json:
        read_json(path.relative_to(PACKAGE))

    foundation = read_json('infra/azure-foundation.json')
    windows = read_json('infra/windows-lab.json')
    for template in (foundation, windows):
        require(template.get('contentVersion') == '1.0.0.0', 'Missing ARM content version')
        check_arm_expression_strings(template)
        identities = [(r.get('type'), r.get('name'), r.get('scope')) for r in template.get('resources', [])]
        require(len(identities) == len(set(identities)), 'Duplicate ARM resources')

    vault = resource(foundation, 'Microsoft.KeyVault/vaults').get('properties', {})
    require(vault.get('publicNetworkAccess') == 'Disabled', 'Vault public network access must be disabled')
    require(vault.get('enableRbacAuthorization') is True, 'Vault must use RBAC')
    require(vault.get('enablePurgeProtection') is True, 'Vault must retain purge protection')
    require(vault.get('networkAcls', {}).get('bypass') == 'None', 'Vault bypass must not be broadened')
    require(not any(r.get('type', '').lower().endswith('/secrets') for r in foundation.get('resources', [])), 'Do not embed secrets in the foundation')
    require(foundation.get('parameters', {}).get('enableSentinel', {}).get('defaultValue') is False, 'Sentinel must be opt-in')

    vnet = resource(foundation, 'Microsoft.Network/virtualNetworks')
    subnets = {s.get('name'): s.get('properties', {}) for s in vnet.get('properties', {}).get('subnets', [])}
    for name in ('snet-connector', 'snet-app', 'snet-private-endpoints'):
        subnet = subnets.get(name, {})
        require(bool(subnet.get('networkSecurityGroup')), f'{name} needs its NSG')
        require(subnet.get('defaultOutboundAccess') is False, f'{name} must not depend on implicit outbound access')
    endpoint_subnet = subnets.get('snet-private-endpoints', {})
    require(endpoint_subnet.get('privateEndpointNetworkPolicies') == 'Enabled', 'Private endpoint NSG enforcement must be enabled')
    for name in ('snet-connector', 'snet-app'):
        require(bool(subnets.get(name, {}).get('natGateway')), f'{name} needs explicit NAT egress')

    for nsg in (r for r in foundation.get('resources', []) if r.get('type') == 'Microsoft.Network/networkSecurityGroups'):
        rules = [r.get('properties', {}) for r in nsg.get('properties', {}).get('securityRules', [])]
        inbound = [r for r in rules if r.get('direction') == 'Inbound']
        require(any(r.get('access') == 'Deny' and r.get('sourceAddressPrefix') == 'VirtualNetwork' and r.get('priority', 65535) < 65000 for r in inbound), f'{nsg.get("name")}: override default VNet inbound allow')
        for direction in ('Inbound', 'Outbound'):
            priorities = [r.get('priority') for r in rules if r.get('direction') == direction]
            require(len(priorities) == len(set(priorities)), f'{nsg.get("name")}: duplicate {direction} priorities')
        for rule in inbound:
            require(not (rule.get('access') == 'Allow' and rule.get('sourceAddressPrefix') in ('*', 'Internet', '0.0.0.0/0')), f'{nsg.get("name")}: broad inbound allow')

    vm_password = windows.get('parameters', {}).get('adminPassword', {})
    require(vm_password.get('type', '').lower() == 'securestring', 'VM password must be secureString')
    require('defaultValue' not in vm_password, 'VM password must have no default')
    for nic in (r for r in windows.get('resources', []) if r.get('type') == 'Microsoft.Network/networkInterfaces'):
        for config in nic.get('properties', {}).get('ipConfigurations', []):
            p = config.get('properties', {})
            require('publicIPAddress' not in p, f'{nic.get("name")}: no public VM IP')
            require(bool(p.get('applicationSecurityGroups')), f'{nic.get("name")}: missing ASG')
    for vm in (r for r in windows.get('resources', []) if r.get('type') == 'Microsoft.Compute/virtualMachines'):
        security = vm.get('properties', {}).get('securityProfile', {})
        require(security.get('uefiSettings', {}).get('secureBootEnabled') is True, f'{vm.get("name")}: Secure Boot required')
        require(security.get('uefiSettings', {}).get('vTpmEnabled') is True, f'{vm.get("name")}: vTPM required')
    app = resource(windows, 'Microsoft.Compute/virtualMachines', 'ezta-app01')
    require(app.get('identity', {}).get('type') == 'SystemAssigned', 'App VM managed identity required')

    ca = read_json('policy/ca-pilot-report-only.example.json')
    require(ca.get('state') == 'enabledForReportingButNotEnforced', 'CA example must start report-only')
    grant = ca.get('grantControls', {})
    require(grant.get('operator') == 'AND' and set(grant.get('builtInControls', [])) == {'mfa', 'compliantDevice'}, 'Require both MFA and a compliant device')
    users = ca.get('conditions', {}).get('users', {})
    require(len(users.get('includeGroups', [])) == 1 and not users.get('includeUsers'), 'CA scope must be the pilot group')
    require(len(set(users.get('excludeUsers', []))) >= 2, 'CA example needs two emergency exclusions')
    apps = ca.get('conditions', {}).get('applications', {}).get('includeApplications', [])
    require(len(apps) == 1 and 'All' not in apps, 'CA example must target the pilot app, not all resources')

    policy = read_json('policy/key-vault-public-access.policy.json').get('properties', {})
    require(policy.get('parameters', {}).get('effect', {}).get('defaultValue') == 'Audit', 'Policy must start in Audit mode')

    evidence = read_json('evidence/templates/test-results.json')
    cases = evidence.get('cases', [])
    ids = [case.get('id') for case in cases]
    require(len(cases) >= 20 and len(ids) == len(set(ids)), 'Acceptance cases need unique identifiers')
    for case in cases:
        require(case.get('status') == 'NOT RUN' and case.get('actual') is None and case.get('executed_utc') is None, f'{case.get("id")}: tracked evidence template must not invent execution')

    # Validate relative links within this package. Parent repository links are also
    # checked when the full repository is present; they remain unchanged assets.
    for path in PACKAGE.rglob('*.md'):
        text = path.read_text(encoding='utf-8')
        require(text.count('```') % 2 == 0, f'{path.relative_to(REPO)}: unclosed code fence')
        for link in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
                continue
            dest = (path.parent / unquote(link.split('#', 1)[0])).resolve()
            try:
                dest.relative_to(PACKAGE)
            except ValueError:
                if (REPO / '.git').is_dir():
                    require(dest.exists(), f'{path.relative_to(REPO)}: missing repository link {link}')
            else:
                require(dest.exists(), f'{path.relative_to(REPO)}: missing package link {link}')

    if errors:
        for error in errors:
            print('ERROR:', error, file=sys.stderr)
        print(f'FAILED: {len(errors)} errors in {checks} offline checks.', file=sys.stderr)
        return 1
    print(f'PASS: {checks} offline checks; {len(all_json)} JSON files parsed.')
    print('Azure validation, Windows execution, KQL execution, and live tenant tests were not performed by this checker.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
