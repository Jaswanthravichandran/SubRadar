'''

                !!! CODE IS NOT WORKING AS EXPECTED !!!
                !!! NEED TO BE FIXED !!!
                !!! IN UPCOMING VERSIONS !!!
                !!! DO NOT USE THIS CODE !!!

'''


import requests
import sys

class dns_dump:
    def __init__(self, domain):
        self.domain = domain

    def dns_dumpster(*args, **kwargs):
        domain = args.domain
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
            sys.exit(1)


