#!/usr/bin/env python3
import unittest
from typing import List


class SystemMOTD:
    @staticmethod
    def sort_fqdns(fqdns: List[str]) -> List[str]:
        reversed_fqdns = []
        for fqdn in fqdns:
            reversed_fqdn = '.'.join(fqdn.split('.')[::-1])
            reversed_fqdns.append(reversed_fqdn)
        reversed_fqdns.sort()
        sorted_fqdns = []
        for reversed_fqdn in reversed_fqdns:
            fqdn = '.'.join(reversed_fqdn.split('.')[::-1])
            sorted_fqdns.append(fqdn)
        return sorted_fqdns


class SystemMOTDTest(unittest.TestCase):
    def test_sort_fqdns(self):
        self.assertEqual(
            SystemMOTD.sort_fqdns([
                'example.com',
                'example.net',
                'www.example.com',
                'example.org',
                'www.example.net',
                'www.example.org',
            ]),
            [
                'example.com',
                'www.example.com',
                'example.net',
                'www.example.net',
                'example.org',
                'www.example.org',
            ],
        )


class FilterModule(object):
    def filters(self):
        return {
            'system_motd_sort_fqdns': SystemMOTD.sort_fqdns,
        }


if __name__ == '__main__':
    unittest.main()
