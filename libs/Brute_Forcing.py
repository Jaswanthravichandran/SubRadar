import dns.resolver
import argparse
from prettytable import PrettyTable
import concurrent.futures

# ANSI escape sequences for text color
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

# Reading the wordlist file
def read_wordlist(wordlist_file):
    with open(wordlist_file, "r") as file:
        wordlist = file.read().splitlines()
    return wordlist

# Resolving subdomains using the DNS protocol
def resolve_subdomain(subdomain, target_domain):
    domain = subdomain + "." + target_domain
    try:
        answers = dns.resolver.resolve(domain)
        return [answer.to_text() for answer in answers]
    except dns.resolver.NoAnswer:
        pass
    except dns.resolver.NXDOMAIN:
        pass
    return []

# Resolving subdomains concurrently
def resolve_subdomains_concurrently(wordlist, target_domain):
    resolved_subdomains = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(resolve_subdomain, subdomain, target_domain) for subdomain in wordlist]
        for future in concurrent.futures.as_completed(results):
            resolved_subdomains.extend(future.result())
    return resolved_subdomains

# Performing a reverse DNS lookup on the IP address of a subdomain
def reverse_dns_lookup(ip_address):
    try:
        reverse_dns = dns.resolver.resolve_address(ip_address)
        return reverse_dns[0].to_text()
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return ip_address

# Printing the resolved subdomains in a table
def print_subdomains_table(subdomains):
    if subdomains:
        table = PrettyTable()
        table.field_names = ["Subdomain", "IP Address"]
        for subdomain in subdomains:
            table.add_row([reverse_dns_lookup(subdomain), subdomain])
        print(f"{Color.GREEN}{table}{Color.RESET}")
    else:
        print(f"{Color.RED}No subdomains found.{Color.RESET}")

# Saving the resolved subdomains in a file
def save_subdomains_to_file(subdomains, output_file):
    with open(output_file, "w") as file:
        for subdomain in subdomains:
            file.write(reverse_dns_lookup(subdomain) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Wordlist-Based Brute Forcing Tool")
    parser.add_argument("wordlist", help="Path to the wordlist file")
    parser.add_argument("target_domain", help="Target domain to perform brute forcing on")
    parser.add_argument("file_name", help="The result will be saved in this file")
    args = parser.parse_args()

    wordlist = read_wordlist(args.wordlist)
    resolved_subdomains = resolve_subdomains_concurrently(wordlist, args.target_domain)
    save_subdomains_to_file(resolved_subdomains, args.file_name)

    print_subdomains_table(resolved_subdomains)

if __name__ == "__main__":
    main()
