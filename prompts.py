CLASSIFY_PROMPT = """
Return RAW JSON only (no markdown fences).
Classify this PDF into one of:
- bank_receipt
- transcript
- unknown

Output:
{ "doc_type": "bank_receipt" | "transcript" | "unknown" }
"""

RECEIPT_PROMPT = """
You are an information extraction engine.

Return RAW JSON only (no markdown fences). No explanations.

Extract bank receipt / statement transactions.

Return:
{
  "doc_type": "bank_receipt",
  "currency": "EUR" | "RM" | "USD" | null,
  "transactions": [
    {
      "payee": string|null,
      "category": "insurance" | "university_fee" | "other",
      "amount": number|null,
      "amount_sign": "debit" | "credit" | null,
      "period_start": "YYYY-MM-DD"|null,
      "period_end": "YYYY-MM-DD"|null,
      "booking_date": "YYYY-MM-DD"|null,
      "reference_text": string|null
    }
  ]
}

Rules:
- Extract ALL visible relevant transactions from the PDF.
- Never guess; use null if missing.
- Amount: numeric only (convert comma decimals to dot).
- Categorize:
  - insurance: health/insurance provider payee (DAK/TK/AOK/Allianz/etc.)
  - university_fee: payee is a university OR reference mentions semester fee/tuition
  - other: otherwise
- Debit means money going out, credit means money coming in.
"""

TRANSCRIPT_PROMPT = """
You are an information extraction engine.

Return RAW JSON only (no markdown fences). No explanations.

Extract a university transcript.

Return:
{
  "doc_type": "transcript",
  "student": { "name": string|null, "matriculation": string|null, "program": string|null },
  "records": [
    {
      "semester": string|null,
      "module_code": string|null,
      "module_name": string|null,
      "grade": string|null,
      "ects": number|null
    }
  ]
}

Rules:
- One record per module/course row.
- Semester must be taken from the document (WS2024 / SS2025 etc.). Never invent.
- Never guess; use null if missing.
"""