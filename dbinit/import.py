#!/bin/python3

import os
import sys
import json
import urllib.request
import urllib.parse
import re
from pathlib import Path

USE_LOCAL_CACHE = True
API_BASE_URL = "https://ergast.com/api/"

def url2localpath(input_str):
  input_str = re.sub(r"(https)|(ergast\.com)|(api)|[:/?&=]", ".", input_str)
  input_str = re.sub(r"\.+", ".", ".cache." + input_str)
  return input_str

def cache_check(url):
  if not USE_LOCAL_CACHE: return None
  path = url2localpath(url)
  if not Path(path).is_file(): return None
  res = ""
  with open(path, "r") as f:
    res = f.read()
    f.close()
  return res

def cache_save(url, response):
  if not USE_LOCAL_CACHE: return
  path = url2localpath(url)
  with open(path, "w+") as f:
    f.write(response)
    f.close()

def api_request(endpoint, options={}):
  url = urllib.parse.urljoin(API_BASE_URL, endpoint + ".json")
  options_str = urllib.parse.urlencode(options)
  if options_str: url += "?" + options_str

  cache_hit = cache_check(url)
  if cache_hit != None:
    return cache_hit
  
  print("actually requesting api")
  conn = urllib.request.urlopen(url)
  res = conn.read().decode("utf-8")
  cache_save(url, res)
  return json.loads(res)

def main(year):
  print(f"fetching year {year}")
  print(api_request("f1/2018/1"))

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("please provide a year to fetch f1 data from")
    exit(1)
  main(sys.argv[1])

