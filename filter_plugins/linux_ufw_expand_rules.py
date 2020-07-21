import unittest
from copy import deepcopy
from typing import List, Dict


class LinuxUFWExpandRules:
    @staticmethod
    def expand_rules(rules: List) -> List:
        rules = LinuxUFWExpandRules._expand_rules(rules, 'from_ip', ['from'])
        rules = LinuxUFWExpandRules._expand_rules(rules, 'from_port')
        rules = LinuxUFWExpandRules._expand_rules(rules, 'to_ip', ['to'])
        rules = LinuxUFWExpandRules._expand_rules(rules, 'to_port', ['port'])
        rules = LinuxUFWExpandRules._expand_rules(rules, 'interface')
        rules = LinuxUFWExpandRules._expand_rules(rules, 'proto')
        return rules

    @staticmethod
    def _expand_rules(rules: List, key: str, key_aliases=[]) -> List:
        expanded_rules = []
        for rule in rules:
            expanded_rules.extend(LinuxUFWExpandRules._expand_rule(rule, 'value', key, key_aliases))
        return expanded_rules

    @staticmethod
    def _expand_rule(obj: Dict, key: str, subkey: str, subkey_aliases: List) -> List[Dict]:
        if not obj[key]:
            return []
        expanded_obj = []

        for subkey_alias in subkey_aliases:
            if subkey_alias in obj[key]:
                if subkey in obj[key]:
                    if not isinstance(obj[key][subkey], list):
                        obj[key][subkey] = [obj[key][subkey]]
                    if not isinstance(obj[key][subkey_alias], list):
                        obj[key][subkey_alias] = [obj[key][subkey_alias]]
                    obj[key][subkey].extend(obj[key][subkey_alias])
                else:
                    obj[key][subkey] = obj[key][subkey_alias]
                del obj[key][subkey_alias]

        if subkey in obj[key]:
            if not isinstance(obj[key][subkey], list):
                obj[key][subkey] = [obj[key][subkey]]
            for value in obj[key][subkey]:
                if value is None or value == '[AnsibleUndefined]':
                    continue
                additional_obj = deepcopy(obj)
                additional_obj[key][subkey] = value
                expanded_obj.append(additional_obj)
        else:
            expanded_obj.append(obj)

        return expanded_obj


class LinuxUFWExpandRulesTest(unittest.TestCase):
    def test_expand_rules(self):
        self.assertEqual(
            LinuxUFWExpandRules.expand_rules(
                [
                    {
                        'key': 'foo',
                        'value': {
                            'proto': 'tcp',
                            'to_port': [
                                80
                            ],
                            'port': [
                                443,
                            ],
                            'from_ip': [
                                '1.1.1.1',
                                '1.0.0.1',
                            ],
                        },
                    },
                    {
                        'key': 'bar',
                        'value': {
                            'proto': 'udp',
                            'to_port': 53,
                            'from_ip': '8.8.8.8',
                        },
                    },
                    {
                        'key': '123',
                        'value': None,
                    },
                    {
                        'key': 'baz',
                        'value': {
                            'proto': 'udp',
                            'port': 53,
                            'to': '8.8.4.4',
                            'to_ip': [
                                '8.8.8.8',
                            ],
                        },
                    },
                    {
                        'key': 'baz',
                        'value': {
                            'proto': 'udp',
                            'port': 53,
                            'to': [
                                '8.8.4.4',
                            ],
                            'to_ip': '8.8.8.8',
                        },
                    },
                    {
                        'key': 'baz',
                        'value': {
                            'proto': 'udp',
                            'port': 53,
                            'to': [
                                None,
                            ],
                            'to_ip': None,
                        },
                    },
                    {
                        'key': 'baz',
                        'value': {
                            'proto': 'udp',
                            'port': 53,
                            'to': None,
                            'to_ip': [
                                None
                            ],
                        },
                    },
                    {
                        'key': 'baz',
                        'value': {
                            'proto': 'udp',
                            'port': 53,
                            'to_ip': None,
                        },
                    },
                    {
                        'key': 'baz',
                        'value': {
                            'proto': 'udp',
                            'port': 53,
                            'to': None,
                        },
                    },
                ],
            ),
            [
                {
                    'key': 'foo',
                    'value': {
                        'proto': 'tcp',
                        'to_port': 80,
                        'from_ip': '1.1.1.1',
                    },
                },
                {
                    'key': 'foo',
                    'value': {
                        'proto': 'tcp',
                        'to_port': 443,
                        'from_ip': '1.1.1.1',
                    },
                },
                {
                    'key': 'foo',
                    'value': {
                        'proto': 'tcp',
                        'to_port': 80,
                        'from_ip': '1.0.0.1',
                    },
                },
                {
                    'key': 'foo',
                    'value': {
                        'proto': 'tcp',
                        'to_port': 443,
                        'from_ip': '1.0.0.1',
                    },
                },
                {
                    'key': 'bar',
                    'value': {
                        'proto': 'udp',
                        'to_port': 53,
                        'from_ip': '8.8.8.8',
                    },
                },
                {
                    'key': 'baz',
                    'value': {
                        'proto': 'udp',
                        'to_port': 53,
                        'to_ip': '8.8.8.8',
                    },
                },
                {
                    'key': 'baz',
                    'value': {
                        'proto': 'udp',
                        'to_port': 53,
                        'to_ip': '8.8.4.4',
                    },
                },
                {
                    'key': 'baz',
                    'value': {
                        'proto': 'udp',
                        'to_port': 53,
                        'to_ip': '8.8.8.8',
                    },
                },
                {
                    'key': 'baz',
                    'value': {
                        'proto': 'udp',
                        'to_port': 53,
                        'to_ip': '8.8.4.4',
                    },
                },
            ],
        )


class FilterModule:
    def filters(self):
        return {
            'linux_ufw_expand_rules': LinuxUFWExpandRules.expand_rules,
        }


if __name__ == '__main__':
    unittest.main()
