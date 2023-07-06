import socket
import argparse
import concurrent 
from concurrent.futures import ThreadPoolExecutor
from prettytable import PrettyTable
import sys

# ANSI escape sequences for text color
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

# Reverse DNS Lookup
def reverse_dns_lookup(ip_address):
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return ip_address
    except socket.gaierror:
        return ip_address

# Perform Reverse DNS Lookups concurrently
def reverse_dns_lookup_concurrently(ip_addresses):
    domains = {}
    with ThreadPoolExecutor() as executor:
        results = {executor.submit(reverse_dns_lookup, ip_address): ip_address for ip_address in ip_addresses}
        for future in concurrent.futures.as_completed(results):
            ip_address = results[future]
            try:
                domains[ip_address] = future.result()
            except Exception as e:
                print(f"{Color.RED}Error occurred while performing reverse DNS lookup for {ip_address}: {e}{Color.RESET}", file=sys.stderr)
    return domains

# Print subdomains as a colored table using PrettyTable
def print_colored_domains(domains):
    if domains:
        table = PrettyTable()
        table.field_names = ["IP Address", "Domain"]
        for ip_address, domain in domains.items():
            table.add_row([ip_address, domain])
        print(f"{Color.GREEN}Discovered Domains:{Color.RESET}")
        print(table)
    else:
        print(f"{Color.RED}No domains found.{Color.RESET}")

def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumeration using Reverse DNS Lookups")
    parser.add_argument("ip_addresses", nargs="+", help="IP addresses to perform reverse DNS lookup")
    args = parser.parse_args()

    domains = reverse_dns_lookup_concurrently(args.ip_addresses)

    print_colored_domains(domains)

if __name__ == "__main__":
    main()
