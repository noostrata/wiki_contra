#!/usr/bin/env python3
"""Simplified Contropedia script for analyzing controversies on Wikipedia."""

import json
import re
import sys
from urllib import parse, request

REV_LIMIT = 500
REVERT_RE = re.compile(r"\b(revert|rv|undo|undid|reverted)\b", re.I)

API = "https://en.wikipedia.org/w/api.php"  # MediaWiki API endpoint


def fetch_revisions(title):
    """Fetch revision data for a Wikipedia article."""
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        # Request revision ids and sha1 so we can detect reverts by identical
        # content hashes in addition to edit summaries.
        "rvprop": "timestamp|user|comment|ids|sha1",
        "rvlimit": REV_LIMIT,
        "format": "json",
    }
    url = API + "?" + parse.urlencode(params)
    with request.urlopen(url) as resp:
        data = json.load(resp)
    page = next(iter(data["query"]["pages"].values()))
    return page.get("revisions", [])


def analyze_reverts(revisions):
    """Return the number of reverts in the revision list."""
    revert_count = 0
    seen_hashes = set()

    # Sort revisions chronologically so "previous" refers to earlier edits
    revisions = sorted(revisions, key=lambda r: r.get("timestamp", ""))

    for rev in revisions:
        comment = rev.get("comment", "")
        sha1 = rev.get("sha1")

        is_summary_revert = bool(REVERT_RE.search(comment))
        is_hash_revert = sha1 in seen_hashes if sha1 else False

        if is_summary_revert or is_hash_revert:
            revert_count += 1

        if sha1:
            seen_hashes.add(sha1)

    return revert_count


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 contropedia.py 'Article Title'")
        sys.exit(1)

    title = sys.argv[1]
    revisions = fetch_revisions(title)
    total = len(revisions)
    reverts = analyze_reverts(revisions)
    score = reverts / total if total else 0

    print(f"Article: {title}")
    print(f"Total revisions fetched: {total}")
    print(f"Detected reverts: {reverts}")
    print(f"Controversy score: {score:.3f}")


if __name__ == "__main__":
    main()
