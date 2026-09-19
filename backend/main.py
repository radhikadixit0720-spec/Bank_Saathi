from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Bank Saathi API")

# Allow the frontend (running on a different port/domain) to call this API.
# For the hackathon demo we allow all origins - tighten this before any real use.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# DUMMY form template. This is NOT a real bank form - it only exists so the
# demo has something to walk a user through field by field.
# ---------------------------------------------------------------------------
FORM_TEMPLATE = [
    {"field_id": "account_number", "label": "Account Number", "required": True},
    {"field_id": "ifsc", "label": "IFSC Code", "required": True},
    {"field_id": "name", "label": "Account Holder Name", "required": True},
    {"field_id": "mobile_number", "label": "Mobile Number", "required": True},
    {"field_id": "aadhaar_last_4", "label": "Last 4 digits of Aadhaar", "required": False},
    {"field_id": "branch_name", "label": "Branch Name", "required": False},
]

EXPLANATIONS = {
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


@app.get("/")
def root():
    return {"status": "Bank Saathi API is running", "docs": "/docs"}


@app.get("/form-template")
def get_template():
    return FORM_TEMPLATE


@app.post("/explain")
def explain_field(req: ExplainRequest):
    explanation = EXPLANATIONS.get(
        req.field_id, "Is field ke liye explanation available nahi hai."
    )
    return {"field_id": req.field_id, "explanation": explanation}


@app.post("/validate")
def validate_form(req: ValidateRequest):
    """Check which required fields are still empty."""
    missing = []
    for field in FORM_TEMPLATE:
        if field["required"]:
            value = req.values.get(field["field_id"], "").strip()
            if not value:
                missing.append(field["field_id"])
    return {"complete": len(missing) == 0, "missing_fields": missing}
