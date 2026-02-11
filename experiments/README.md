experiments — QMD + retrieval + summarization experiments

This folder contains small experiments that combine local retrieval (qmd) with cloud LLM summarization and other workflows.

Current experiments
- topic_summarizer.py — Retrieve top‑K local snippets from a qmd collection and summarize them with the OpenAI Responses API (or return snippets only).
  - Path: experiments/topic_summarizer.py
  - Usage (example):
    python experiments/topic_summarizer.py --topic "Miller's college preparation" --k 5 --out experiments/miller_summary.json
  - Notes:
    - Requires qmd installed and a collection named 'user_profile' (or set QMD_COLLECTION env). We built and embedded the user_profile collection earlier.
    - Requires OPENAI_API_KEY in the environment for summarization (if you select cloud summarization). The script will save the retrieved snippets and the model response to the output JSON file.

How to run experiments safely
1. Ensure qmd is available and embedded collections include the content you want to query.
2. Set OPENAI_API_KEY in the environment if you want the LLM polish step (costs may apply).
3. Run the script and inspect the saved JSON before committing any generated text.

Planned experiments
- progressive_summarizer.py — multi-stage chunking + local summarizer + final LLM polish
- faq_builder.py — convert a set of docs into FAQ Q/A pairs with citations

Notes
- Keep experiments in this folder; once an experiment stabilizes it can be promoted to a subproject.
