#!/bin/python3

import os
import sys
import urllib.request

global YEAR
USE_LOCAL_CACHE = True
API_BASE_URL = "https://ergast.com/"

def api_request(endpoint):
  conn = urllib.request.urlopen(API_BASE_URL + endpoint)
  return conn.read()

def main():
  print(f"fetching year {YEAR}")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("please provide a year to fetch f1 data from")
    exit(1)
  YEAR = int(sys.argv[1])
  main()

