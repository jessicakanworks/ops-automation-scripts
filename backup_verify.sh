#!/usr/bin/env bash
# Verify the most recent backup: exists, < 26h old, checksum matches its .sha256 file.
set -euo pipefail
BACKUP_DIR="${1:-/backups/db}"
latest=$(ls -1t "$BACKUP_DIR"/*.dump 2>/dev/null | head -n1 || true)
[[ -n "$latest" ]] || { echo "FAIL no backups in $BACKUP_DIR"; exit 1; }
age_h=$(( ( $(date +%s) - $(stat -c %Y "$latest") ) / 3600 ))
(( age_h < 26 )) || { echo "FAIL latest backup is ${age_h}h old: $latest"; exit 1; }
[[ -f "$latest.sha256" ]] || { echo "FAIL missing checksum for $latest"; exit 1; }
sha256sum -c --quiet "$latest.sha256" || { echo "FAIL checksum mismatch: $latest"; exit 1; }
echo "OK   $latest (${age_h}h old, $(du -h "$latest" | cut -f1))"
