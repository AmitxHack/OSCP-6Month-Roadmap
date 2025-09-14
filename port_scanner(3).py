#!/usr/bin/env python3
# improved_port_scanner.py

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

parser = argparse.ArgumentParser(description="Simple TCP port scanner with optional banner grab")
parser.add_argument("-t", "--target", required=True, help="target hostname or IP")
parser.add_argument("-p", "--ports", default="1-1024",
                    help="port or range (e.g. 22,80 or 1-1024)")
parser.add_argument("-w", "--workers", type=int, default=100,
                    help="max concurrent worker threads (default: 100)")
parser.add_argument("--timeout", type=float, default=0.8, help="socket timeout in seconds")
args = parser.parse_args()

def parse_ports(pstr):
    """Parse a port string like '22,80,100-110' -> sorted list of ints."""
    out = set()
    for part in pstr.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                a, b = part.split('-', 1)
                a = int(a); b = int(b)
                if a < 1 or b > 65535 or a > b:
                    raise ValueError
                out.update(range(a, b + 1))
            except ValueError:
                raise argparse.ArgumentTypeError(f"Invalid port range: '{part}'")
        else:
            try:
                p = int(part)
                if p < 1 or p > 65535:
                    raise ValueError
                out.add(p)
            except ValueError:
                raise argparse.ArgumentTypeError(f"Invalid port: '{part}'")
    return sorted(out)

try:
    ports = parse_ports(args.ports)
except Exception as e:
    print(f"Error parsing ports: {e}")
    raise SystemExit(1)

# Resolve hostname early
try:
    target_ip = socket.gethostbyname(args.target)
except socket.gaierror as e:
    print(f"Could not resolve target '{args.target}': {e}")
    raise SystemExit(1)

file_lock = threading.Lock()

def scan_port(host_ip, port, timeout=0.8):
    """Return tuple (port, is_open, banner)"""
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        res = s.connect_ex((host_ip, port))
        if res == 0:
            banner = ""
            try:
                # Try a non-blocking recv after a tiny send; some servers respond without a send
                s.settimeout(0.5)
                # It's safer to not send garbage to services; attempt recv first
                try:
                    banner = s.recv(1024).decode(errors='ignore').strip()
                except socket.timeout:
                    # Try a gentle probe
                    try:
                        s.send(b"\r\n")
                        banner = s.recv(1024).decode(errors='ignore').strip()
                    except Exception:
                        banner = ""
            except Exception:
                banner = ""
            return (port, True, banner)
        else:
            return (port, False, "")
    finally:
        if s:
            try:
                s.close()
            except Exception:
                pass

# Scan with a thread pool and append results safely
results = []
with ThreadPoolExecutor(max_workers=args.workers) as ex:
    future_to_port = {ex.submit(scan_port, target_ip, p, args.timeout): p for p in ports}
    for fut in as_completed(future_to_port):
        p = future_to_port[fut]
        try:
            port, is_open, banner = fut.result()
            if is_open:
                print(f"[+] {args.target} ({target_ip}):{port} OPEN | {banner}")
                # append to file in a thread-safe way
                with file_lock:
                    with open('scan_results.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{args.target},{target_ip},{port},OPEN,{banner}\n")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            # print error for debugging but continue scanning
            print(f"[!] Error scanning port {p}: {e}")

# python3 improved_port_scanner.py -t example.com -p 1-1024 --workers 200 --timeout 0.6
