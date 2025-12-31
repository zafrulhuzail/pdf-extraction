from typing import List, Literal, Optional

from pydantic import BaseModel, Field


DocType = Literal["bank_receipt", "transcript", "unknown"]
TxnCategory = Literal["insurance", "university_fee", "other"]
AmountSign = Literal["debit", "credit"]


class Transaction(BaseModel):
    payee: Optional[str] = None
    category: TxnCategory = "other"
    amount: Optional[float] = None
    amount_sign: Optional[AmountSign] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    booking_date: Optional[str] = None
    reference_text: Optional[str] = None


class BankReceiptExtraction(BaseModel):
    doc_type: Literal["bank_receipt"]
    currency: Optional[str] = None
    transactions: List[Transaction] = Field(default_factory=list)


class TranscriptStudent(BaseModel):
    name: Optional[str] = None
    matriculation: Optional[str] = None
    program: Optional[str] = None


class TranscriptRecord(BaseModel):
    semester: Optional[str] = None
    module_code: Optional[str] = None
    module_name: Optional[str] = None
    grade: Optional[str] = None
    ects: Optional[float] = None


class TranscriptExtraction(BaseModel):
    doc_type: Literal["transcript"]
    student: TranscriptStudent = Field(default_factory=TranscriptStudent)
    records: List[TranscriptRecord] = Field(default_factory=list)