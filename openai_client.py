from typing import Any
import os
from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

def make_client() -> OpenAI:
    # Create client factory so tests can patch / dependency inject
    return OpenAI()

def upload_pdf_to_openai(client: OpenAI, pdf_bytes: bytes, filename: str) -> str:
    uploaded = client.files.create(
        file=(filename, pdf_bytes, "application/pdf"),
        purpose="assistants",
    )
    return uploaded.id

def ask_with_file(client: OpenAI, prompt: str, file_id: str, model: str = MODEL) -> str:
    resp = client.responses.create(
        model=model,
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_file", "file_id": file_id},
            ]
        }],
    )
    return resp.output_text