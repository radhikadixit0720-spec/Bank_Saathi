"""
Legacy endpoints from the original Bank Saathi prototype (the guided,
field-by-field "samjhao" walkthrough with Hindi text-to-speech on the
frontend). Kept working, unmodified in behaviour, so nothing that already
worked is broken by the upgrade. New feature work lives in the other
routes/* modules instead of being bolted onto this file.
"""
from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Legacy (original prototype)"])

LEGACY_FORM_TEMPLATE = [
    {"field_id": "account_number", "label": "Account Number", "required": True},
    {"field_id": "ifsc", "label": "IFSC Code", "required": True},
    {"field_id": "name", "label": "Account Holder Name", "required": True},
    {"field_id": "mobile_number", "label": "Mobile Number", "required": True},
    {"field_id": "aadhaar_last_4", "label": "Last 4 digits of Aadhaar", "required": False},
    {"field_id": "branch_name", "label": "Branch Name", "required": False},
]

LEGACY_EXPLANATIONS = {
    "account_number": "Yahan apna bank account number likhiye. Ye aapke passbook ya cheque book ke pehle page par milta hai.",
    "ifsc": "IFSC code 11 characters ka hota hai, jaise SBIN0001234. Ye aapki branch ko identify karta hai. Ye bhi passbook par milta hai.",
    "name": "Account holder ka poora naam likhiye, bilkul waisa jaisa bank ke records me hai.",
    "mobile_number": "Wo mobile number likhiye jo aapke bank account se link hai. Isi par OTP aata hai.",
    "aadhaar_last_4": "Sirf apne Aadhaar number ke last 4 dummy digits dikhaiye. Poora Aadhaar number kabhi kisi form ya app me na likhein jab tak bank staff khud na maange.",
    "branch_name": "Aapki home branch ka naam, jo passbook ke pehle page par likha hota hai.",
}


class ExplainRequest(BaseModel):
    field_id: str


class ValidateRequest(BaseModel):
    values: Dict[str, str]


@router.get("/form-template")
def get_template():
    return LEGACY_FORM_TEMPLATE


@router.post("/explain")
def explain_field(req: ExplainRequest):
    explanation = LEGACY_EXPLANATIONS.get(
        req.field_id, "Is field ke liye explanation available nahi hai."
    )
    return {"field_id": req.field_id, "explanation": explanation}


@router.post("/validate")
def validate_form(req: ValidateRequest):
    missing = []
    for field in LEGACY_FORM_TEMPLATE:
        if field["required"]:
            value = req.values.get(field["field_id"], "").strip()
            if not value:
                missing.append(field["field_id"])
    return {"complete": len(missing) == 0, "missing_fields": missing}
