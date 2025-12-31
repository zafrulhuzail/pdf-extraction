# PDF Extraction Backend

Small FastAPI service that uploads PDFs to OpenAI and extracts structured data (bank receipts or university transcripts) using model prompts.

Quick links:
- API: [api.py](api.py) — endpoint function [`api.extract`](api.py)
- OpenAI client/wrappers: [openai_client.py](openai_client.py) — [`openai_client.make_client`](openai_client.py), [`openai_client.upload_pdf_to_openai`](openai_client.py), [`openai_client.ask_with_file`](openai_client.py)
- Prompts: [prompts.py](prompts.py) — [`prompts.CLASSIFY_PROMPT`](prompts.py), [`prompts.RECEIPT_PROMPT`](prompts.py), [`prompts.TRANSCRIPT_PROMPT`](prompts.py)
- Schemas: [schemas.py](schemas.py) — [`schemas.BankReceiptExtraction`](schemas.py), [`schemas.TranscriptExtraction`](schemas.py)
- Utilities: [utils.py](utils.py) — [`utils.safe_json_loads`](utils.py), [`utils.strip_markdown_fences`](utils.py)
- Analytics: [analytics.py](analytics.py) — [`analytics.compute_money_totals`](analytics.py), [`analytics.group_transcript_with_ects`](analytics.py)
- Entry point: [main.py](main.py)
- Requirements: [requirements.txt](requirements.txt)
- Docker: [Dockerfile](Dockerfile)
- Example environment: [.env](.env)

Requirements
1. Python 3.9
2. Install deps: pip install -r [requirements.txt](requirements.txt)
3. Podman (to run via Docker)

Environment
- Set OPENAI_API_KEY (see [.env](.env))
- Optionally set OPENAI_MODEL (defaults to gpt-4.1-mini via [openai_client.py](openai_client.py))

Run locally using podman
1. Install requirements.
2. Build
   ```sh
   podman build -t pdf-extractor .
2. Start container:
   ```sh
   podman run --rm -p 8000:8000 --env-file .env pdf-extractor

Run locally
1. Install requirements.
2. Start dev server:
   ```sh
   uvicorn main:app --reload --port 8000