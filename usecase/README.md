# Reproducible RAG use cases

Small, **standard-library-only Python 3.11+** programs connected to the worked examples in [RAG Lab v2](https://redcof.github.io/study/rag/). Each script includes a Markdown-formatted module docstring with the problem, sample data, expected result, and limitations. All datasets are illustrative and local.

## Reproduce on macOS / Linux

```bash
git clone https://github.com/Redcof/AgenticAILab.git
cd AgenticAILab
python3 --version                   # 3.11+
python3 -m venv .venv
source .venv/bin/activate
# No pip install needed for these six examples.
python3 usecase/01_foundations.py
python3 usecase/02_chunking.py
python3 usecase/03_vector_search.py
python3 usecase/04_evaluation.py
python3 usecase/05_agent_authorization.py
python3 usecase/06_grounded_citations.py
python3 -m unittest discover -s usecase -p 'test_*.py' -v
```

Windows PowerShell: use `py -3 -m venv .venv`, `.venv\Scripts\Activate.ps1`, then `python` in place of `python3`. If activation is blocked, invoke `.venv\Scripts\python.exe` directly.

## Exercises and expected observations

| Lab chapter | Script | What to observe |
|---|---|---|
| Foundations | [01_foundations.py](01_foundations.py) | Latest effective policy wins; no evidence → abstain |
| Chunking | [02_chunking.py](02_chunking.py) | Overlap rescues a fact split at a chunk boundary |
| Vector Search | [03_vector_search.py](03_vector_search.py) | Exact cosine ranking and tenant pre-filter |
| Evaluation / RAG Evaluation Lab | [04_evaluation.py](04_evaluation.py) | Precision@k, recall@k, F1, reciprocal rank |
| Agentic AI | [05_agent_authorization.py](05_agent_authorization.py) | Untrusted refund requests are denied; approved scoped action succeeds once |
| Hallucination & Grounding | [06_grounded_citations.py](06_grounded_citations.py) | Unsupported numeric claim and incorrect citation are rejected |

These examples **do not** call a live LLM, perform production OCR, use real embeddings, or implement a production-grade security gateway. The authorization demo models a *trusted context* and a policy gate in memory; real systems must authenticate callers and enforce database and service permissions. The grounding demo uses exact toy claim checks, not natural-language entailment.

## Change inputs and experiment

Modify the `main()` sample data and rerun each script. Compare the printed output with the assertion-based tests in `test_usecases.py`. Try a tenant mismatch, a missing citation, an empty query, or a changed document version. Run `python3 -m unittest discover -s usecase -p 'test_*.py' -v` after every change.

The **RAGForge** package in `src/ragforge` is a separate, more structured learning baseline; these scripts are standalone, readable reproductions intended to be linked directly from quiz explanations.

## Next additions

Graph RAG, production latency/SLO simulation, AWS deployment configuration, reranking/RRF, and capstone integration are planned. These six scripts are an initial batch, **not** one implementation for every one of the 75 quiz questions.
