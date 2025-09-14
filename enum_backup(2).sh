#!/bin/bash
# enum_backup.sh - collect quick enumeration data to /tmp/enum_backup
OUTDIR="/tmp/enum_backup_$(date +%F_%T)"
mkdir -p "$OUTDIR"
echo "Collecting system info to $OUTDIR"
uname -a > "$OUTDIR/uname.txt"
id > "$OUTDIR/id.txt"
ps aux > "$OUTDIR/ps_aux.txt"
cp /etc/passwd "$OUTDIR/passwd.txt" 2>/dev/null
cp /etc/hosts "$OUTDIR/hosts.txt" 2>/dev/null
find / -perm -4000 -type f 2>/dev/null > "$OUTDIR/suid.txt"
find / -writable -type f 2>/dev/null > "$OUTDIR/writable_files.txt"
ls -la /etc/cron* > "$OUTDIR/cron.txt" 2>/dev/null
echo "Done. Archive: $OUTDIR.tar.gz"
tar -czf "$OUTDIR.tar.gz" -C "$(dirname "$OUTDIR")" "$(basename "$OUTDIR")"

# sudo chmod +x enum_backup.sh && sudo ./enum_backup.sh