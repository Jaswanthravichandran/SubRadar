import dns.resolver
import argparse

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
def resolve_subdomains(wordlist, target_domain):
    resolved_subdomains = []
    for subdomain in wordlist:
        domain = subdomain + "." + target_domain
        try:
            answers = dns.resolver.resolve(domain)
            for answer in answers:
                resolved_subdomains.append(answer.to_text())
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            pass
    return resolved_subdomains

# Performing a reverse DNS lookup on the IP address of a subdomain
def reverse_dns_lookup(ip_address):
    try:
        reverse_dns = dns.resolver.resolve_address(ip_address)
        return reverse_dns[0].to_text()
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return ip_address

# Printing the resolved subdomains in color
def print_colored_subdomains(subdomains):
    if subdomains:
        print(f"{Color.GREEN}Resolved Subdomains:{Color.RESET}")
        for subdomain in subdomains:
            print(f"{Color.YELLOW}{reverse_dns_lookup(subdomain)}{Color.RESET}")
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
    resolved_subdomains = resolve_subdomains(wordlist, args.target_domain)
    save_subdomains_to_file(resolved_subdomains, args.file_name)

    print_colored_subdomains(resolved_subdomains)

if __name__ == "__main__":
    main()
