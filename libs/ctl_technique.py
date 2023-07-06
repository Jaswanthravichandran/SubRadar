import requests
import json
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

# Certificate Transparency Logs Subdomain Enumeration
def subdomain_enumeration(target_domain):
    subdomains = set()
    url = f"https://crt.sh/?q=%25.{target_domain}&output=json"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            certificates = json.loads(response.text)
            for certificate in certificates:
                subdomain = certificate["name_value"]
                if not subdomain.startswith("*"):
                    subdomains.add(subdomain)
        except json.JSONDecodeError:
            pass
    return subdomains

# Perform subdomain enumeration using Certificate Transparency Logs concurrently
def subdomain_enumeration_concurrently(target_domains):
    subdomains = {}
    with ThreadPoolExecutor() as executor:
        results = {executor.submit(subdomain_enumeration, domain): domain for domain in target_domains}
        for future in concurrent.futures.as_completed(results):
            domain = results[future]
            try:
                subdomains[domain] = future.result()
            except Exception as e:
                print(f"{Color.RED}Error occurred while enumerating subdomains for {domain}: {e}{Color.RESET}", file=sys.stderr)
    return subdomains

# Print subdomains as a colored table using PrettyTable
def print_colored_subdomains(subdomains):
    if subdomains:
        table = PrettyTable()
        table.field_names = ["Domain", "Subdomain"]
        for domain, subs in subdomains.items():
            for subdomain in subs:
                table.add_row([domain, subdomain])
        print(f"{Color.GREEN}Discovered Subdomains:{Color.RESET}")
        print(table)
    else:
        print(f"{Color.RED}No subdomains found.{Color.RESET}")

def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumeration using Certificate Transparency Logs")
    parser.add_argument("target_domains", nargs="+", help="Target domains for subdomain enumeration")
    args = parser.parse_args()

    subdomains = subdomain_enumeration_concurrently(args.target_domains)

    print_colored_subdomains(subdomains)

if __name__ == "__main__":
    main()
