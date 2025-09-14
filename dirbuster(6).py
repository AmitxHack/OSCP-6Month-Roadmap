#!/usr/bin/env python3
# dirbuster_improved.py
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import sys

def valid_url(u):
    p = urlparse(u)
    return p.scheme in ('http', 'https') and p.netloc

parser = argparse.ArgumentParser(description="Simple dirbuster (lab use only). Use only with authorization.")
parser.add_argument('-u', '--url', required=True, help='Base URL (http(s)://host[:port])')
parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file (one path per line)')
parser.add_argument('-t', '--threads', type=int, default=20, help='Max concurrent threads (default 20)')
parser.add_argument('-o', '--output', default='found_paths.txt', help='Output file')
parser.add_argument('-v', '--verbose', action='store_true', help='Show 401/403/redirects too')
args = parser.parse_args()

if not valid_url(args.url):
    print("Invalid URL. Include scheme (http:// or https://).")
    sys.exit(1)

headers = {'User-Agent': 'Mozilla/5.0 (OSCP-DirBuster)'}

def check_path(base, path):
    url = base.rstrip('/') + '/' + path.lstrip('/')
    try:
        r = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
        code = r.status_code
        # treat 400 and 404 as not found; adjust as needed
        if code not in (404, 400):
            # if verbose show everything, otherwise show common interesting codes
            if args.verbose or code < 400 or code in (401, 403, 301, 302):
                print(f"[+] {url} ({code})")
                with open(args.output, 'a') as f:
                    f.write(f"{url},{code}\n")
    except requests.RequestException as e:
        # optionally log network errors when verbose
        if args.verbose:
            print(f"[-] {url} error: {e}")

# read wordlist
try:
    with open(args.wordlist, 'r') as f:
        words = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("Wordlist file not found.")
    sys.exit(1)

# use ThreadPoolExecutor to limit concurrency
with ThreadPoolExecutor(max_workers=args.threads) as ex:
    futures = [ex.submit(check_path, args.url, w) for w in words]
    # optional: iterate to allow keyboard interrupt handling
    try:
        for _ in as_completed(futures):
            pass
    except KeyboardInterrupt:
        print("Interrupted by user. Shutting down executor...")
        ex.shutdown(wait=False)
        sys.exit(1)
# python3 dirbuster.py -u http://192.168.56.102 -w common.txt