#!/usr/bin/env python3
"""Recreate imported PRs that were closed when master was deleted, now targeting main.
Skips upstream#284 (the user's own PR, already merged)."""

import json
import re
import subprocess
import sys

TARGET = "QQSHI13/min-html"
TARGET_BASE = "main"
SKIP_UPSTREAM = 284


def gh(*args, check=True):
    cmd = ["gh", "-R", TARGET, *args]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if check and result.returncode != 0:
        print(f"gh failed: {' '.join(cmd)}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def main():
    closed = json.loads(gh("pr", "list", "--state", "closed", "-L", "100",
                           "--json", "number,title,body,headRefName,baseRefName").stdout)
    open_prs = json.loads(gh("pr", "list", "--state", "open", "-L", "100",
                             "--json", "number,title,headRefName").stdout)
    open_heads = {pr["headRefName"] for pr in open_prs}

    imported = [pr for pr in closed
                if pr["baseRefName"] == "master" and pr["headRefName"].startswith("imported/pr-")]

    for pr in imported:
        m = re.search(r"\[upstream#(\d+)\]", pr["title"])
        if not m:
            print(f"  skipping PR #{pr['number']} (no upstream number in title)")
            continue
        upstream_num = int(m.group(1))
        if upstream_num == SKIP_UPSTREAM:
            print(f"  skipping upstream#{upstream_num} (your own PR, already merged)")
            continue

        head = pr["headRefName"]
        if head in open_heads:
            print(f"  {head} already has an open PR, skipping")
            continue

        result = gh("pr", "create",
                    "--head", head,
                    "--base", TARGET_BASE,
                    "--title", pr["title"],
                    "--body", pr["body"])
        url = result.stdout.strip()
        print(f"  recreated upstream#{upstream_num} as {url}")


if __name__ == "__main__":
    main()
