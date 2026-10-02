#!/usr/bin/env python3
import socket, sys, urllib.request, yaml

def tcp_ok(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout): return True
    except OSError: return False

def http_status(url, timeout=5):
    try:
        return urllib.request.urlopen(url, timeout=timeout).status
    except urllib.error.HTTPError as e: return e.code
    except Exception: return None

def main(path="checks.yml"):
    cfg = yaml.safe_load(open(path)); failures = 0
    for c in cfg.get("tcp", []):
        ok = tcp_ok(c["host"], c["port"]); failures += not ok
        print(f"{'OK  ' if ok else 'FAIL'} tcp  {c['name']} {c['host']}:{c['port']}")
    for c in cfg.get("http", []):
        st = http_status(c["url"]); ok = st == c.get("expect", 200); failures += not ok
        print(f"{'OK  ' if ok else 'FAIL'} http {c['name']} -> {st}")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main(*sys.argv[1:])
