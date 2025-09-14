#!/bin/bash
# backup.sh - copy files from source to backup dir
SRC="/home/$USER/docs"
DEST="/home/$USER/backup"
mkdir -p "$DEST"
for f in "$SRC"/*; do
if [ -f "$f" ]; then
cp -a "$f" "$DEST/"
echo "Copied: $f -> $DEST"
fi
done
echo "Backup completed: $DEST"
# Run: chmod +x backup.sh && ./backup.sh