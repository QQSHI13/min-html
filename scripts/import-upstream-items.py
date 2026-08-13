#!/usr/bin/env python3
"""Copy open issues and PRs from wilsonzlin/minify-html to QQSHI13/min-html.

Idempotent: skips items already present in the target repo.
For PRs, fetches the PR head ref from upstream and pushes it to the target repo
as `imported/pr-<N>`, then opens a new PR from that branch.
"""

import json
import subprocess
import sys

UPSTREAM = "wilsonzlin/minify-html"
TARGET = "QQSHI13/min-html"
TARGET_DEFAULT_BRANCH = "master"


def gh(*args, repo=None, input_text=None, check=True):
    cmd = ["gh"]
    if repo:
        cmd.extend(["-R", repo])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        print(f"gh command failed: {' '.join(cmd)}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def list_upstream_issues():
    result = gh(
        "issue", "list", "--state", "open", "-L", "100",
        "--json", "number,title,body,labels,author,createdAt,updatedAt",
        repo=UPSTREAM,
    )
    return json.loads(result.stdout)


def list_upstream_prs():
    result = gh(
        "pr", "list", "--state", "open", "-L", "100",
        "--json",
        "number,title,body,labels,author,createdAt,updatedAt,headRefName,headRefOid,baseRefName,isCrossRepository",
        repo=UPSTREAM,
    )
    return json.loads(result.stdout)


def list_target_issues():
    result = gh(
        "issue", "list", "--state", "all", "-L", "200",
        "--json", "number,title,body",
        repo=TARGET,
    )
    return json.loads(result.stdout)


def list_target_prs():
    result = gh(
        "pr", "list", "--state", "all", "-L", "200",
        "--json", "number,title,body,headRefName",
        repo=TARGET,
    )
    return json.loads(result.stdout)


def list_target_labels():
    result = gh("label", "list", "--json", "name", repo=TARGET)
    return {label["name"] for label in json.loads(result.stdout)}


def already_copied_target_issue(items, number, kind="issue"):
    marker = f"Copied from {UPSTREAM}#{number}"
    for item in items:
        if marker in (item.get("title") or "") or marker in (item.get("body") or ""):
            return item
    return None


def make_body(original_body, number, kind):
    header = f"> Copied from {UPSTREAM}#{number}\n>\n> Original {kind} by {original_body.get('author', {}).get('login', 'unknown')}\n"
    body = original_body.get("body") or ""
    return header + "\n" + body


def copy_issue(issue, existing, valid_labels):
    if already_copied_target_issue(existing, issue["number"], "issue"):
        print(f"  issue #{issue['number']} already copied, skipping")
        return

    labels = [label["name"] for label in issue.get("labels", []) if label["name"] in valid_labels]
    title = f"[upstream#{issue['number']}] {issue['title']}"
    body = make_body(issue, issue["number"], "issue")

    args = ["issue", "create", "--title", title, "--body", body]
    if labels:
        args.extend(["--label", ",".join(labels)])

    result = gh(*args, repo=TARGET)
    url = result.stdout.strip()
    print(f"  created issue for upstream#{issue['number']}: {url}")


def import_pr(pr, existing_prs, existing_issues):
    number = pr["number"]
    if already_copied_target_issue(existing_prs, number, "pr"):
        print(f"  PR #{number} already copied, skipping")
        return
    if already_copied_target_issue(existing_issues, number, "pr"):
        print(f"  PR #{number} already tracked as issue, skipping")
        return

    branch = f"imported/pr-{number}"

    # Fetch PR head from upstream hidden ref. This works for PRs from any fork.
    fetch = subprocess.run(
        ["git", "fetch", "upstream", f"pull/{number}/head:{branch}"],
        capture_output=True,
        text=True,
    )
    if fetch.returncode != 0:
        print(f"  failed to fetch PR #{number}: {fetch.stderr.strip()}")
        create_tracking_issue(pr, existing_issues)
        return

    push = subprocess.run(
        ["git", "push", "fork", branch],
        capture_output=True,
        text=True,
    )
    if push.returncode != 0:
        print(f"  failed to push PR #{number}: {push.stderr.strip()}")
        create_tracking_issue(pr, existing_issues)
        return

    title = f"[upstream#{number}] {pr['title']}"
    body = make_body(pr, number, "PR")

    result = gh(
        "pr", "create",
        "--title", title,
        "--body", body,
        "--head", branch,
        "--base", TARGET_DEFAULT_BRANCH,
        repo=TARGET,
    )
    url = result.stdout.strip()
    print(f"  created PR for upstream#{number}: {url}")


def create_tracking_issue(pr, existing_issues):
    number = pr["number"]
    if already_copied_target_issue(existing_issues, number, "pr"):
        print(f"  tracking issue for PR #{number} already exists, skipping")
        return

    title = f"[upstream#{number}] [PR-tracking] {pr['title']}"
    body = make_body(pr, number, "PR")
    body += (
        "\n\n> Note: the original PR branch could not be imported automatically. "
        "This issue tracks it instead."
    )

    result = gh("issue", "create", "--title", title, "--body", body, repo=TARGET)
    url = result.stdout.strip()
    print(f"  created tracking issue for upstream PR#{number}: {url}")


def main():
    print(f"Fetching open issues from {UPSTREAM}...")
    upstream_issues = list_upstream_issues()
    print(f"  found {len(upstream_issues)} open issues")

    print(f"Fetching open PRs from {UPSTREAM}...")
    upstream_prs = list_upstream_prs()
    print(f"  found {len(upstream_prs)} open PRs")

    print(f"Fetching existing items from {TARGET}...")
    target_issues = list_target_issues()
    target_prs = list_target_prs()
    target_labels = list_target_labels()
    print(f"  found {len(target_issues)} existing issues, {len(target_prs)} existing PRs, {len(target_labels)} labels")

    print("Copying issues...")
    for issue in upstream_issues:
        copy_issue(issue, target_issues, target_labels)

    print("Importing PRs...")
    for pr in upstream_prs:
        import_pr(pr, target_prs, target_issues)

    print("Done.")


if __name__ == "__main__":
    main()
