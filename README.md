# ops-automation-scripts

Small, dependable Python and Bash utilities for day-to-day operations:

| Script | What it does |
|--------|--------------|
| `health_check.py` | checks TCP ports and HTTP endpoints from `checks.yml`, exits non-zero on failure |
| `cert_expiry.py` | reports TLS certificates expiring within N days |
| `backup_verify.sh` | confirms last night's backup exists, is recent, and its checksum matches |
| `log_housekeeping.sh` | compresses logs older than 7 days, deletes older than 90 |
| `sla_report.py` | pulls availability from Prometheus and writes a monthly SLA summary (CSV) |

All scripts are safe to run from cron/systemd timers and print machine-readable output.
