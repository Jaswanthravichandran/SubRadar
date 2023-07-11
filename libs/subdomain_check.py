import requests
import sys
import time
import argparse


'''

    !!! CODE IS NOT WORKING AS EXPECTED !!!
    !!! NEED TO BE FIXED !!!
    !!! IN UPCOMING VERSIONS !!!
    !!! DO NOT USE THIS CODE !!!

'''

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"



try: 
    with open('result.txt','r') as file:
        for line in file:
            sub = line.strip()
            response = requests.get(f"https://{sub}")
            if response.status_code == 200:
                print(f"{Colors.GREEN}Valid subdomain: {sub} => {response.status_code}{Colors.RESET}")
            else:
                print(f"{Colors.RED}Invalid subdomain: {sub} => {response.status_code}{Colors.RESET}")
except FileNotFoundError:
    print(f"{Colors.RED}File not found.{Colors.RESET}")
    sys.exit(1)
except KeyboardInterrupt:
    print(f"{Colors.RED}Keyboard interrupt.{Colors.RESET}")
    sys.exit(1)
except:
    print(f"{Colors.RED}An error occurred.{Colors.RESET}")
    sys.exit(1)


