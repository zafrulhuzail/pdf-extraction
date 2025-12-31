import os
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from .openai_client import make_client, upload_pdf_to_openai, ask_with_file, MODEL
from .utils import safe_json_loads
from .schemas import BankReceiptExtraction, TranscriptExtraction
from .analytics import compute_money_totals, group_transcript_with_ects
from .prompts import CLASSIFY_PROMPT, RECEIPT_PROMPT, TRANSCRIPT_PROMPT

app = FastAPI(title="PDF Extraction Backend", version="1.1.0")
client = make_client()

@app.post("/extract")
async def extract(files: List[UploadFile] = File(...)) -> Dict[str, Any]:
    documents_out = []
    receipt_extractions: List[BankReceiptExtraction] = []
    transcript_extractions: List[TranscriptExtraction] = []

    for f in files:
        pdf_bytes = await f.read()
        try:
            file_id = upload_pdf_to_openai(client, pdf_bytes, f.filename or "document.pdf")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed for {f.filename}: {e}")

        doc_type = "unknown"
        try:
            classify_text = ask_with_file(client, CLASSIFY_PROMPT, file_id)
            classify = safe_json_loads(classify_text)
            doc_type = classify.get("doc_type", "unknown")
        except Exception:
            doc_type = "unknown"

        raw_output = None
        extraction = {"doc_type": "unknown"}
        issues = []

        try:
            if doc_type == "bank_receipt":
                raw_output = ask_with_file(client, RECEIPT_PROMPT, file_id)
                data = safe_json_loads(raw_output)
                parsed = BankReceiptExtraction.model_validate(data)
                receipt_extractions.append(parsed)
                extraction = parsed.model_dump()
            elif doc_type == "transcript":
                raw_output = ask_with_file(client, TRANSCRIPT_PROMPT, file_id)
                data = safe_json_loads(raw_output)
                parsed = TranscriptExtraction.model_validate(data)
                transcript_extractions.append(parsed)
                extraction = parsed.model_dump()
            else:
                issues.append("Could not classify document reliably; manual review needed.")
        except Exception as e:
            issues.append(f"Extraction failed: {e}")

        documents_out.append({
            "file_name": f.filename,
            "openai_file_id": file_id,
            "classified_as": doc_type,
            "extraction": extraction,
            "issues": issues,
            "raw_model_output": raw_output if os.getenv("INCLUDE_RAW", "0") == "1" else None,
        })

    computed = {
        "money": compute_money_totals(receipt_extractions),
        "transcript": group_transcript_with_ects(transcript_extractions),
    }

    return {
        "model": MODEL,
        "documents": documents_out,
        "computed": computed,
    }