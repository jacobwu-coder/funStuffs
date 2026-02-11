"""experiments/topic_summarizer.py

Retrieve top-K snippets from qmd for a topic and summarize with OpenAI (gpt-5-mini or configured model).

Usage:
  python experiments/topic_summarizer.py --topic "values" --k 5 --out results.json

Requirements:
- qmd CLI available and a collection named 'user_profile' indexed (we created it earlier)
- OpenAI python client installed and OPENAI_API_KEY accessible to the environment

This script is a small demo of local retrieval (qmd) + cloud LLM summarization.
"""
import argparse
import json
import shlex
import subprocess
import os
from pathlib import Path

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

QMD_BIN = os.environ.get("QMD_BIN", "/Users/wojack/.bun/bin/qmd")
COLLECTION = os.environ.get("QMD_COLLECTION", "user_profile")
DEFAULT_MODEL = os.environ.get("TOPIC_SUM_MODEL", "gpt-5-mini")


def qmd_vsearch(query: str, k: int = 5):
    cmd = [QMD_BIN, "vsearch", query, "-c", COLLECTION, "-n", str(k), "--json"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"qmd vsearch failed: {proc.stderr}")
    return json.loads(proc.stdout)


def summarize_with_openai(snippets: list, topic: str, model: str = DEFAULT_MODEL):
    if OpenAI is None:
        raise RuntimeError("OpenAI client not available. Install openai package.")
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set in environment.")

    client = OpenAI(api_key=key)
    # Build a compact prompt
    context = "\n\n".join([s.get("text", "") for s in snippets])
    prompt = (
        f"You are an expert summarizer. Given the following snippets about '{topic}',\n"
        "produce: (1) a 3-bullet executive summary, and (2) a one-line TL;DR. Keep bullets short.\n\n"
        f"Snippets:\n{context}\n\nOutput format:\n- BULLET 1\n- BULLET 2\n- BULLET 3\nTLDR: <one line>"
    )

    resp = client.responses.create(model=model, input=prompt)
    # Extract text (Responses API may return complex object)
    out = resp
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--out", default="topic_summary.json")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    print(f"Searching qmd for '{args.topic}' (top {args.k}) in collection {COLLECTION}...")
    results = qmd_vsearch(args.topic, args.k)
    # results is JSON list of hits; normalize
    snippets = []
    for r in results:
        txt = r.get('snippet') or r.get('text') or r.get('content') or ''
        snippets.append({'id': r.get('docid') or r.get('id'), 'text': txt})

    summary = None
    try:
        print('Calling OpenAI to summarize...')
        summary = summarize_with_openai([s['text'] for s in snippets], args.topic, model=args.model)
    except Exception as e:
        print('OpenAI summarization failed:', e)
        summary = None

    out_obj = {'topic': args.topic, 'snippets': snippets, 'summary': summary}
    Path(args.out).write_text(json.dumps(out_obj, indent=2))
    print('Saved output to', args.out)


if __name__ == '__main__':
    main()
