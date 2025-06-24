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
        "rvprop": "timestamp|user|comment",
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
    for rev in revisions:
        comment = rev.get("comment", "")
        if REVERT_RE.search(comment):
            revert_count += 1
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
