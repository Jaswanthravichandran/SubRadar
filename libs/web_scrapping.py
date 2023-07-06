import requests
from bs4 import BeautifulSoup
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

# Subdomain Enumeration using Web Scraping
def subdomain_enumeration(target_domain):
    subdomains = set()
    url = f"https://www.{target_domain}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for anchor_tag in soup.find_all("a"):
            href = anchor_tag.get("href")
            if href.startswith("http://") or href.startswith("https://"):
                subdomain = href.split("//")[1].split(".")[0]
                subdomains.add(subdomain)
    return subdomains

# Perform subdomain enumeration concurrently
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
        print(f"{Color.GREEN}{table}{Color.RESET}")
    else:
        print(f"{Color.RED}No subdomains found.{Color.RESET}")

def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumeration using Web Scraping")
    parser.add_argument("target_domains", nargs="+", help="Target domains for subdomain enumeration")
    args = parser.parse_args()

    subdomains = subdomain_enumeration_concurrently(args.target_domains)

    print_colored_subdomains(subdomains)

if __name__ == "__main__":
    main()


# Usage example: python subdomain_enumeration.py example.com example2.com 