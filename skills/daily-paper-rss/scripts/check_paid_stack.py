#!/usr/bin/env python3
"""Fail-closed paid-stack mix check for a daily-paper-rss edition.

Counts http(s) story-cite URLs in the edition markdown. Classifies each host
against paid-stack suffixes (suffix match, strip www.). No network.

Exit 0 if paid/total >= threshold and total > 0.
Exit 1 if below threshold or no cites found.

Suraj is the brief's alias for Swarajya. No separate Suraj host is known;
swarajyamag.com and swarajya.com are the Swarajya/Suraj suffixes.
"""

from __future__ import annotations

import argparse
import re
import sys
from urllib.parse import urlparse

# Sameer's brief paid stack. Override with --stack.
DEFAULT_STACK = (
    "nytimes.com",
    "wsj.com",
    "bloomberg.com",
    "economist.com",
    "newyorker.com",
    "theatlantic.com",
    "indianexpress.com",
    "newindianexpress.com",
    "economictimes.com",
    "economictimes.indiatimes.com",
    "swarajyamag.com",
    "swarajya.com",
)

URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
TRAILING_PUNCT = ".,;:!?)]}'\">"


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    for raw in URL_RE.findall(text):
        url = raw.rstrip(TRAILING_PUNCT)
        if url:
            urls.append(url)
    return urls


def normalize_host(host: str) -> str:
    host = host.lower().strip().lstrip(".")
    if host.startswith("www."):
        host = host[4:]
    return host


def host_of(url: str) -> str:
    parsed = urlparse(url)
    return normalize_host(parsed.hostname or "")


def is_paid_host(host: str, suffixes: tuple[str, ...] | list[str]) -> bool:
    if not host:
        return False
    for suffix in suffixes:
        suffix = normalize_host(suffix)
        if not suffix:
            continue
        if host == suffix or host.endswith("." + suffix):
            return True
    return False


def count_mix(urls: list[str], suffixes: tuple[str, ...] | list[str]) -> tuple[int, int]:
    paid = sum(1 for url in urls if is_paid_host(host_of(url), suffixes))
    return paid, len(urls)


def summary_line(paid: int, total: int, passed: bool) -> str:
    pct = (100.0 * paid / total) if total else 0.0
    verdict = "PASS" if passed else "FAIL"
    return f"paid {paid} / total {total} ({pct:.1f}%) {verdict}"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail-closed paid-stack mix check for an edition markdown file."
    )
    parser.add_argument("edition", help="Path to the edition markdown file")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Minimum paid/total ratio to pass (default: 0.5)",
    )
    parser.add_argument(
        "--stack",
        nargs="+",
        default=None,
        metavar="HOST",
        help="Paid-stack host suffixes (default: Sameer brief list)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.threshold < 0 or args.threshold > 1:
        print("error: --threshold must be between 0 and 1", file=sys.stderr)
        return 1
    try:
        with open(args.edition, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        print(f"error: cannot read {args.edition}: {exc}", file=sys.stderr)
        return 1

    suffixes = tuple(args.stack) if args.stack else DEFAULT_STACK
    paid, total = count_mix(extract_urls(text), suffixes)
    passed = total > 0 and (paid / total) >= args.threshold
    print(summary_line(paid, total, passed))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
