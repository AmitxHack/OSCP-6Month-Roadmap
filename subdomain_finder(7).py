#!/usr/bin/env python3
# subdomain_finder_improved.py
"""
Usage example:
  python3 subdomain_finder_improved.py -d example.com -w subdomains.txt -t 50 -o found.txt -v

Only use against targets you are authorized to test.
"""
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from uuid import uuid4
import sys
import threading

parser = argparse.ArgumentParser(description="Subdomain finder (lab use only). Use only with authorization.")
parser.add_argument('-d', '--domain', required=True, help='Target domain (example.com)')
parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file (one subdomain per line)')
parser.add_argument('-t', '--threads', type=int, default=20, help='Max concurrent workers (default 20)')
parser.add_argument('-o', '--output', default='found_subdomains.txt', help='Output file')
parser.add_argument('--timeout', type=float, default=3.0, help='Socket timeout seconds (default 3.0)')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
parser.add_argument('--no-wildcard-check', action='store_true', help='Skip wildcard DNS detection')
args = parser.parse_args()

# Basic domain sanity check
if '.' not in args.domain or ' ' in args.domain:
    print("Invalid domain. Provide a proper domain like example.com")
    sys.exit(1)

socket.setdefaulttimeout(args.timeout)
write_lock = threading.Lock()
found_set = set()

def resolve_host(host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        return None
    except Exception as e:
        if args.verbose:
            print(f"[-] {host} error: {e}")
        return None

def wildcard_check(domain):
    # generate a random nonsense subdomain and see if it resolves
    rnd = f"{uuid4().hex[:12]}"
    host = f"{rnd}.{domain}"
    ip = resolve_host(host)
    if ip:
        if args.verbose:
            print(f"[!] Wildcard DNS detected: {host} -> {ip}")
        return ip
    return None

# optional wildcard detection
wildcard_ip = None
if not args.no_wildcard_check:
    wildcard_ip = wildcard_check(args.domain)

def worker(sub):
    host = f"{sub.strip()}.{args.domain}"
    ip = resolve_host(host)
    if ip:
        # if wildcard detected and IP equals wildcard IP, it's likely fake -> ignore
        if wildcard_ip and ip == wildcard_ip:
            if args.verbose:
                print(f"[~] Skipping (matches wildcard IP): {host} -> {ip}")
            return None
        with write_lock:
            if host not in found_set:
                found_set.add(host)
                with open(args.output, 'a') as f:
                    f.write(f"{host},{ip}\n")
        print(f"[+] {host} -> {ip}")
        return (host, ip)
    return None

# read wordlist
try:
    with open(args.wordlist, 'r') as f:
        words = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("Wordlist file not found.")
    sys.exit(1)

if not words:
    print("Wordlist is empty.")
    sys.exit(1)

# run with ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=args.threads) as ex:
    futures = {ex.submit(worker, w): w for w in words}
    try:
        for fut in as_completed(futures):
            # result consumed to propagate exceptions if any
            _ = fut.result()
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting.")
        ex.shutdown(wait=False)
        sys.exit(1)

print(f"Done. Results (unique) written to {args.output}")

# Run: python3 subdomain_finder.py -d example.com -w subdomains.txt