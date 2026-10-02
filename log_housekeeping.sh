#!/usr/bin/env bash
# Compress logs older than 7 days, delete compressed logs older than 90 days.
set -euo pipefail
LOG_DIRS=("/var/log/app" "/opt/app/logs" "/var/log/nginx")
for d in "${LOG_DIRS[@]}"; do
  [[ -d "$d" ]] || continue
  find "$d" -type f -name "*.log" -mtime +7 ! -name "*.gz" -exec gzip -q {} \;
  find "$d" -type f -name "*.gz" -mtime +90 -delete
  echo "housekeeping done: $d ($(du -sh "$d" | cut -f1))"
done
