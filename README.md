# Agentic AI Lab — RAGForge

An incremental, **production-minded RAG engineering study lab**. We start with a fully testable Python lexical retrieval baseline and progressively add token-aware chunking, Rust acceleration, embeddings, vector search, evaluation, and eventually agentic workflows.

**Current state: Stage 1 (working CLI demo).** This is intentionally **not yet full RAG**: it has no LLM, embeddings, persistent database, web API, or Rust extension. All commands work locally, with no credentials, Docker, GPU, paid service, or API key.

## Prerequisites

- Python **3.11 or newer** (`python3 --version`), ideally Python 3.12
- Git (`git --version`)
- pip (`python3 -m pip --version`)
- Terminal on macOS/Linux or PowerShell on Windows

On macOS, Homebrew users can install Python and Git using `brew install python@3.12 git`. On Windows, install Python from python.org and enable its PATH option.

## Step 1 — Clone

```bash
git clone https://github.com/Redcof/AgenticAILab.git
cd AgenticAILab
```

## Step 2 — Prepare an isolated environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
```

**Windows PowerShell**

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python --version
```

If PowerShell prevents activation, use `.venv\Scripts\python.exe` directly for subsequent Python commands. You do not need to change your system's execution policy.

## Step 3 — Install the app and developer dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Editable installation means changes under `src/ragforge/` take effect without reinstalling. The dev extra installs `pytest` and `ruff`.

## Step 4 — Test and validate

```bash
python -m pytest -q
python -m ruff check .
```

Expected: **10 tests pass**, with no Ruff errors. This covers tenant filtering, ranking, deterministic behavior, invalid inputs, and duplicate document IDs.

### Offline fallback (no package installation)

If your machine cannot download dependencies, you can run the standard-library-only demo directly from the repository root without installing anything:

**macOS / Linux:**

```bash
PYTHONPATH=src python3 -m ragforge.cli "RAG retrieval"
```

**Windows PowerShell:**

```powershell
$env:PYTHONPATH = "src"
py -3 -m ragforge.cli "RAG retrieval"
```

Unit tests still require `pytest`; the normal editable installation is recommended when you have internet access.

## Step 5 — Run the app

```bash
ragforge
```

Expected output:

```text
0.577 | rag-001 | RAG combines retrieval with language generation.
0.316 | rag-002 | Vector databases support semantic retrieval.
```

Try different search queries, tenants, and result limits:

```bash
ragforge "semantic retrieval"
ragforge "RAG retrieval" --tenant demo --limit 2
ragforge "RAG retrieval" --tenant other
ragforge "nonexistent phrase"
python -m ragforge.cli "RAG retrieval" --tenant demo
ragforge --help
```

To leave the environment: `deactivate`.

**Important:** `--tenant` is a learning/demo filter, not authentication. In production, obtain tenant identity from a validated security context, enforce authorization in storage and all downstream components, and never trust arbitrary caller-supplied tenant IDs.

## What the program actually does

```text
CLI arguments (cli.py)
   |
   v
Domain contracts (domain.py)
   |
   v
LexicalRetriever (retrieval.py)
   |-- tokenize text and count word occurrences
   |-- filter documents by tenant BEFORE scoring
   |-- compute raw term-frequency cosine similarity
   |-- sort by descending score, then ascending document ID
   v
Ranked SearchHit objects
```

The retrieval is lexical, not semantic: paraphrases may not match. Search scans an in-memory corpus rather than using a search index. Cosine scores describe overlap between word-count vectors, not probabilities or model confidence.

## Repository layout

```text
AgenticAILab/
├── README.md
├── pyproject.toml
├── .gitignore
├── src/
│   └── ragforge/
│       ├── __init__.py
│       ├── domain.py
│       ├── retrieval.py
│       └── cli.py
└── tests/
    └── test_retrieval.py
```

## Design principles (Staff-level engineering)

1. **Domain independence**: immutable domain contracts do not import HTTP, storage, or ML libraries.
2. **Deterministic tests**: document-ID tie-breaking produces stable retrieval order.
3. **Tenant boundaries**: filter before scoring; future stages must also enforce tenant isolation during indexing, caching, reranking, generation, and citations.
4. **Baseline first**: measure correctness, recall, latency, and memory *before* optimizing or adding complex frameworks.
5. **Honest scope**: no API keys, LLM calls, embeddings, or Rust build toolchain in Stage 1.
6. **Portable setup**: standard Python packaging and minimal dependencies keep this stage easy to run and debug.

## Reproducible worked examples

The [`usecase/` directory](usecase/README.md) contains six standalone Python scripts that demonstrate RAG concepts with sample data, outputs and tests. They require only Python 3.11+ and no API keys. Run all six from the repository root and check their tests:

```bash
python3 usecase/01_foundations.py
python3 usecase/02_chunking.py
python3 usecase/03_vector_search.py
python3 usecase/04_evaluation.py
python3 usecase/05_agent_authorization.py
python3 usecase/06_grounded_citations.py
python3 -m unittest discover -s usecase -p 'test_*.py' -v
```

See [full use-case setup and reproduction instructions](usecase/README.md). Related links also appear beside the worked examples in the [portfolio RAG Lab](https://redcof.github.io/study/rag/).

## Progressive curriculum

| Stage | Subject | Implementation |
|---|---|---|
| **1 (implemented)** | Foundations | Python packaging, contracts, lexical retrieval, CLI, unit tests |
| 2 | Chunking + Rust | Token-aware Python reference, Rust/PyO3 implementation, correctness and performance benchmark |
| 3 | Vector Search | Embeddings, PostgreSQL/pgvector, hybrid retrieval and ANN evaluation |
| 4 | Graph RAG | Entity/relation extraction, graph augmentation |
| 5 | Evaluation | Recall@k, MRR, factual-grounding and regression datasets |
| 6 | Agentic AI | Typed tools, bounded workflows, retries and failure handling |
| 7 | Production design | FastAPI, authentication, observability, caching, rate limiting |
| 8 | Deployment | Containers, CI/CD, secrets, cloud deployment |
| 9 | Grounding | Citations, evidence checks, abstention policy |
| 10 | Advanced retrieval | Reranking, query rewriting, retrieval strategies |
| 11 | Evaluation lab | Offline evaluation and operational benchmarks |
| 12 | Capstone | Integrated, deployable RAG system |

**Why Python + Rust?** Python owns models, application APIs, orchestration and experiments. Rust is introduced at an independently testable performance boundary (first: chunking/text processing). We will benchmark against the Python baseline before deciding to retain the extension. Stage 2 will document `rustup`, `maturin` and `PyO3`; **Rust is not required yet**.

## Troubleshooting

- `python3: command not found`: install Python 3.11+; Windows users can use `py -3`.
- `ragforge: command not found`: activate `.venv`; rerun `python -m pip install -e ".[dev]"`, or use `python -m ragforge.cli`.
- `No module named ragforge`: install in the **repository root**, inside the selected virtual environment.
- `No module named pytest`: install the dev extras with `python -m pip install -e ".[dev]"`.
- PowerShell blocks activation: run `.venv\Scripts\python.exe -m pytest -q` directly.
- No matching results: the demonstration is lexical; check word overlap and the selected `--tenant`.

## Extra developer commands

```bash
python -m pytest -v
python -m ruff check .
python -m pip list
python -c "from ragforge.retrieval import tokenize; print(tokenize('Hello, RAG!'))"
```

**Architecture practice:** How would you enforce tenant isolation at storage, retrieval, cache, rerank, and citation boundaries for 10 million documents and 500 tenants? The demo's pre-scoring filter is only an initial illustration, not a complete solution.
