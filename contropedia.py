#!/usr/bin/env python3
"""Simplified Contropedia script for analyzing controversies on Wikipedia."""

import json
import re
import argparse
from urllib import parse, request

REV_LIMIT = 500
REVERT_RE = re.compile(r"\b(revert|rv|undo|undid|reverted)\b", re.I)

API = "https://en.wikipedia.org/w/api.php"  # MediaWiki API endpoint


def fetch_revisions(title, limit=REV_LIMIT):
    """Fetch revision data for a Wikipedia article."""
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "timestamp|user|comment",
        "rvlimit": limit,
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


def parse_args(argv=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze revert activity in a Wikipedia article"
    )
    parser.add_argument("title", help="Wikipedia article title")
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=REV_LIMIT,
        help="Number of revisions to fetch (default: %(default)s)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional file to write results to instead of stdout",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    revisions = fetch_revisions(args.title, limit=args.limit)
    total = len(revisions)
    reverts = analyze_reverts(revisions)
    score = reverts / total if total else 0

    output = [
        f"Article: {args.title}",
        f"Total revisions fetched: {total}",
        f"Detected reverts: {reverts}",
        f"Controversy score: {score:.3f}",
    ]

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write("\n".join(output) + "\n")
    else:
        for line in output:
            print(line)


if __name__ == "__main__":
    main()
