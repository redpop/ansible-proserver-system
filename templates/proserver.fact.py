#!/usr/bin/env python3

import json
import subprocess
from ipaddress import ip_address
from ipaddress import ip_network


PUBLIC_INTERFACES = {{ system.network.public_interfaces|to_json }}
PUBLIC_SUBNETS = {{ system.network.public_subnets|to_json }}
PUBLIC_SUBNETS = [ip_network(public_subnet) for public_subnet in PUBLIC_SUBNETS]


class SystemInterfaces(list):
    def __init__(self):
        system_interfaces = subprocess.check_output(['ip', '--json', 'addr', 'show'], stderr=subprocess.DEVNULL)
        system_interfaces = json.loads(system_interfaces)
        self.extend(system_interfaces)


class SystemDefaultRoutes(list):
    @staticmethod
    def get_default_route(addr: str):
        stdout, stderr = subprocess.Popen(
            ['ip', '--json', 'route', 'get', addr],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        ).communicate()
        if not stdout:
            return []
        return json.loads(stdout)

    def __init__(self):
        self.extend(self.get_default_route('1.1.1.1'))
        self.extend(self.get_default_route('2606:4700:4700::1111'))


class Network(dict):
    def __init__(self):
        super().__init__()
        system_interfaces = SystemInterfaces()

        public_ipv4_address = None
        public_ipv6_address = None

        if PUBLIC_SUBNETS:
            for interface in system_interfaces:
                for public_subnet in PUBLIC_SUBNETS:
                    for addr in interface['addr_info']:
                        addr = ip_address(addr['local'])
                        if public_subnet.version == addr.version and public_subnet.supernet_of(ip_network(str(addr))):
                            if addr.version == 4 and not public_ipv4_address:
                                public_ipv4_address = addr
                            elif addr.version == 6 and not public_ipv6_address:
                                public_ipv6_address = addr

        if PUBLIC_INTERFACES:
            for interface in system_interfaces:
                for public_interface in PUBLIC_INTERFACES:
                    if interface['ifname'] == public_interface:
                        for addr in interface['addr_info']:
                            addr = ip_address(addr['local'])
                            if addr.version == 4 and not public_ipv4_address:
                                public_ipv4_address = addr
                            elif addr.version == 6 and not public_ipv6_address:
                                public_ipv6_address = addr

        system_default_routes = SystemDefaultRoutes()
        for route in system_default_routes:
            addr = ip_address(route['prefsrc'])
            if addr.version == 4 and not public_ipv4_address:
                public_ipv4_address = addr
            elif addr.version == 6 and not public_ipv6_address:
                public_ipv6_address = addr

        self['public_ipv4_address'] = public_ipv4_address.compressed if public_ipv4_address else None
        self['public_ipv6_address'] = public_ipv6_address.compressed if public_ipv6_address else None


class Routing(dict):
    def __init__(self):
        super().__init__()
        self['with_gate64'] = False
        self['gate64_ip_address'] = None


class Blueprint(dict):
    def __init__(self):
        super().__init__()
        self['name'] = None
        self['number'] = None
        self['year'] = None
        self['quarter'] = None
        self['version'] = None


class Facts:
    def __str__(self):
        return json.dumps({
            'network': Network(),
            'routing': Routing(),
            'blueprint': Blueprint(),
        })


if __name__ == '__main__':
    print(Facts())
