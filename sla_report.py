#!/usr/bin/env python3
"""Monthly availability per HTTP probe target from Prometheus -> CSV."""
import argparse, csv, datetime, json, sys, urllib.parse, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--prom", default="http://localhost:9090"); ap.add_argument("--days", type=int, default=30)
ap.add_argument("--out", default="sla_report.csv"); a = ap.parse_args()
q = f'avg_over_time(probe_success{{job="blackbox_http"}}[{a.days}d]) * 100'
url = f"{a.prom}/api/v1/query?" + urllib.parse.urlencode({"query": q})
data = json.load(urllib.request.urlopen(url, timeout=30))["data"]["result"]
with open(a.out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["target", f"availability_%_{a.days}d", "sla_target_%", "met"])
    for r in data:
        avail = float(r["value"][1]); w.writerow([r["metric"]["instance"], f"{avail:.3f}", 99.5, avail >= 99.5])
        print(f"{r['metric']['instance']}: {avail:.3f}%")
print(f"written {a.out} on {datetime.date.today()}")
