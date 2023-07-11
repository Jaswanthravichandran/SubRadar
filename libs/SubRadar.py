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


def main():
    parser = argparse.ArgumentParser(
        prog="SubRadar",
        description="Subdomain Enumeration using Reverse DNS Lookups")
    pass