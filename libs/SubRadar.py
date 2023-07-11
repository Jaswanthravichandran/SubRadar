'''

            Here we import all the submodules of the Radar module
                - BruteForce
                - CTL
                - DNS dumpster (not working)
                - DNS zone transfer
                - Search engines (have to work on it)
                - Reverse DNS lookup 
                - Web scraping 
            

'''
import argparse
import concurrent
import sys
from concurrent.futures import ThreadPoolExecutor
import time


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"



def func_call(*args, **kwargs):
    pass


def main():
    parser = argparse.ArgumentParser(
        prog="SubRadar",
        description="Use with -h or --help for help")
    parser.add_argument("-d", "--domain", help="Domain to scan", required=True)
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-t", "--threads", help="Number of threads", default=10)
    parser.add_argument()
    args = parser.parse_args()
    result = func_call(args.domain, args.output, args.threads)
    print(f"{Colors.GREEN}result{Colors.RESET}")
