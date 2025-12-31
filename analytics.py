from collections import defaultdict
from typing import List, Dict, Any
from .schemas import BankReceiptExtraction, TranscriptExtraction
from .utils import month_key_from_iso

def compute_money_totals(receipts: List[BankReceiptExtraction]) -> Dict[str, Any]:
    insurance_total = 0.0
    semester_fee_total = 0.0
    insurance_by_month = defaultdict(float)
    semester_fee_by_month = defaultdict(float)

    for r in receipts:
        for tx in r.transactions:
            if tx.amount is None:
                continue
            if tx.amount_sign == "credit":
                continue
            amt = float(tx.amount)
            if tx.category == "insurance":
                insurance_total += amt
                mk = month_key_from_iso(tx.period_start)
                if mk:
                    insurance_by_month[mk] += amt
            elif tx.category == "university_fee":
                semester_fee_total += amt
                mk = month_key_from_iso(tx.period_start)
                if mk:
                    semester_fee_by_month[mk] += amt

    grand_total = insurance_total + semester_fee_total
    return {
        "insurance_total": round(insurance_total, 2),
        "semester_fee_total": round(semester_fee_total, 2),
        "grand_total": round(grand_total, 2),
        "insurance_by_month": {k: round(v, 2) for k, v in sorted(insurance_by_month.items())},
        "semester_fee_by_month": {k: round(v, 2) for k, v in sorted(semester_fee_by_month.items())},
    }

def group_transcript_with_ects(transcripts: List[TranscriptExtraction]) -> Dict[str, Any]:
    grouped = defaultdict(list)
    ects_by_semester = defaultdict(float)
    student = {}

    for t in transcripts:
        if not student:
            student = t.student.model_dump()
        for rec in t.records:
            sem = (rec.semester or "UNKNOWN").strip()
            grouped[sem].append(rec.model_dump())
            if rec.ects is not None:
                ects_by_semester[sem] += float(rec.ects)

    return {
        "student": student or None,
        "semesters": dict(grouped),
        "ects_by_semester": {k: round(v, 2) for k, v in sorted(ects_by_semester.items())},
    }