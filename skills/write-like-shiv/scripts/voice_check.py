#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import re
import statistics


def prose_lines(text):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence or re.match(r"^\s*(>|#|\||https?://|<table|</?tr|</?td)", line):
            continue
        line = re.sub(r"(`+).*?\1", "", line)
        line = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", line)
        item = re.match(r"^\s*(?:[-*+] |\d+[.)] )", line) is not None
        line = re.sub(r"^\s*(?:[-*+] |\d+[.)] )", "", line)
        yield number, line, item


parser = argparse.ArgumentParser(description="Review prose patterns; never classify authorship.")
parser.add_argument("file", type=Path)
parser.add_argument("--strict", action="store_true", help="Exit 1 when manual review candidates exist.")
parser.add_argument("--surface", choices=["default", "vision"], default="default", help="vision adds length and list-density checks (references/vision.md).")
parser.add_argument("--min-words", type=int, help="Flag prose shorter than this (vision default: 300).")
parser.add_argument("--max-words", type=int, help="Flag prose longer than this (vision default: 450).")
args = parser.parse_args()
source = args.file.read_text(encoding="utf-8")
lines = list(prose_lines(source))
text = "\n".join(line for _, line, _ in lines)
patterns = {
    "stock_phrase": r"\b(?:delve|tapestry|groundbreaking|seamless|foster(?:s|ed|ing)?|leverag(?:e|es|ed|ing)|great question|hope this helps|at the end of the day|game[- ]changer|excited to share|thrilled to announce|in today['’]s (?:fast[- ]paced|rapidly evolving) (?:world|landscape)|it['’]s worth noting|in conclusion)\b",
    "stock_contrast": r"\b(?:it['’]s not|this isn['’]t about)\b[^.!?\n]{1,120}?(?:,|--|—)\s*(?:it['’]s|but)\b",
    "vague_attribution": r"\b(?:experts say|studies show|many believe)\b",
    "punctuation_default": "—",
}
findings = []
for number, line, _ in lines:
    for kind, pattern in patterns.items():
        for match in re.finditer(pattern, line, flags=re.IGNORECASE):
            findings.append({"kind": kind, "line": number, "text": match.group(0)})
sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n\s*\n", text) if s.strip()]
word_sets = [re.findall(r"\b[\w]+(?:['’][\w]+)*\b", s) for s in sentences]
word_sets = [words for words in word_sets if words]
lengths = [len(words) for words in word_sets]
starts = {}
for words in word_sets:
    if len(words) >= 3:
        start = " ".join(words[:3]).lower()
        starts[start] = starts.get(start, 0) + 1
for start, count in starts.items():
    if count >= 3:
        findings.append({"kind": "repeated_opening", "text": start, "count": count})
word_count = sum(lengths)
if args.surface == "vision":
    low = args.min_words if args.min_words is not None else 300
    high = args.max_words if args.max_words is not None else 450
else:
    low, high = args.min_words, args.max_words
if low is not None and word_count < low:
    findings.append({"kind": "length", "text": f"{word_count} words; below {low}"})
if high is not None and word_count > high:
    findings.append({"kind": "length", "text": f"{word_count} words; above {high}"})
if args.surface == "vision":
    filled = [item for _, line, item in lines if line.strip()]
    list_items = sum(filled)
    if list_items >= 3 and list_items * 3 > len(filled):
        findings.append({"kind": "list_heavy", "text": f"{list_items} of {len(filled)} prose lines are list items; carry the argument in paragraphs"})
mean = statistics.mean(lengths) if lengths else None
report = {
    "findings": findings,
    "surface": args.surface,
    "word_count": word_count,
    "rhythm": {
        "sentence_count": len(lengths),
        "sentence_lengths": lengths,
        "mean_words": round(mean, 2) if mean else None,
        "coefficient_of_variation": round(statistics.pstdev(lengths) / mean, 3) if len(lengths) >= 8 else None,
    },
    "notes": [
        "Heuristic English/Markdown diagnostics; inspect findings in context.",
        "Fenced code, blockquotes, headings, table rows, URL-only lines, and inline code are excluded.",
        "Rhythm has no target; fewer than eight sentences suppresses the coefficient of variation.",
        "This is not an AI detector or a measure of Shiv's voice fidelity.",
        "Vision mode checks length (300-450 words unless overridden) and list density; see references/vision.md.",
    ],
}
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(1 if args.strict and findings else 0)
