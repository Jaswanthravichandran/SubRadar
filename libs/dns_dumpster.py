import requests

def dns_dumpster(domain):
    url = f"https://dnsdumpster.com/static/map/{domain}.png"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Subdomains found:")
            subdomains = response.text.split('\n')
            for subdomain in subdomains:
                print(subdomain)
        else:
            print("Unable to retrieve subdomains.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Usage example
domain_name = "example.com"
dns_dumpster(domain_name)
