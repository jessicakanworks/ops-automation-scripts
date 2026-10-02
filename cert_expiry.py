#!/usr/bin/env python3
"""Usage: cert_expiry.py host1:443 host2:443 [--days 30]"""
import argparse, datetime, socket, ssl, sys

def expiry(host, port):
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=5) as s, ctx.wrap_socket(s, server_hostname=host) as ss:
        cert = ss.getpeercert()
    return datetime.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")

ap = argparse.ArgumentParser(); ap.add_argument("targets", nargs="+"); ap.add_argument("--days", type=int, default=30)
a = ap.parse_args(); warn = 0
for t in a.targets:
    host, _, port = t.partition(":")
    try:
        exp = expiry(host, int(port or 443)); left = (exp - datetime.datetime.utcnow()).days
        flag = "WARN" if left < a.days else "OK  "; warn += flag == "WARN"
        print(f"{flag} {t} expires {exp:%Y-%m-%d} ({left} days)")
    except Exception as e:
        print(f"ERR  {t} {e}"); warn += 1
sys.exit(1 if warn else 0)
