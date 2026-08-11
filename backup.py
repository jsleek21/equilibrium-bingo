"""Snapshot the items + cards tables from Supabase into timestamped JSON files
and commit/push them to the equilibrium-bingo GitHub repo. Run on a schedule
(see the scheduled task set up alongside this file) so a bad edit, an
accidental mass-delete, or a Supabase mishap is always recoverable.
"""
import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_DIR = Path(__file__).parent
BACKUP_DIR = REPO_DIR / "backups"
SUPABASE_URL = "https://nmwbwclpwvbcenhxfirw.supabase.co"
API_KEY = "sb_publishable_VlC6QzuXAYyKrfF-lf8V0Q_Vh8a-k5-"
KEEP_LAST = 200  # prune older snapshots beyond this count (per table)

HEADERS = {"apikey": API_KEY, "Authorization": f"Bearer {API_KEY}"}


def fetch(table):
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/{table}?select=*", headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def prune(prefix):
    files = sorted(BACKUP_DIR.glob(f"{prefix}-*.json"))
    for f in files[:-KEEP_LAST]:
        f.unlink()


def main():
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    items = fetch("items")
    cards = fetch("cards")

    (BACKUP_DIR / f"items-{ts}.json").write_text(json.dumps(items, indent=1), encoding="utf-8")
    (BACKUP_DIR / f"cards-{ts}.json").write_text(json.dumps(cards, indent=1), encoding="utf-8")

    prune("items")
    prune("cards")

    subprocess.run(["git", "add", "backups"], cwd=REPO_DIR, check=True)
    # nothing to commit is not an error — only commit/push if there's a diff
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_DIR)
    if diff.returncode == 0:
        print("no changes since last backup, skipping commit")
        return

    subprocess.run(
        ["git", "-c", "user.email=bingo-backup@local", "-c", "user.name=Bingo Backup",
         "commit", "-q", "-m", f"Backup {ts} ({len(items)} items, {len(cards)} cards)"],
        cwd=REPO_DIR, check=True,
    )
    subprocess.run(["git", "push"], cwd=REPO_DIR, check=True)
    print(f"backed up {len(items)} items, {len(cards)} cards at {ts}")


if __name__ == "__main__":
    main()
