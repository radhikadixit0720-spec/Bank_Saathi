"""
Configurable document checklists, keyed by banking service.

Kept as structured backend data (not hard-coded inside frontend components)
so it can later be moved into a MongoDB `checklists` collection and edited
by bank admins without a frontend deploy. Service names and document
labels are translated on the fly for Hindi/Hinglish via LABEL_TRANSLATIONS
(same approach as backend/data/templates.py).
"""
from typing import Dict, List

from backend.data.i18n import normalize_lang

LABEL_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "Account Opening": {"hi": "खाता खोलना", "hinglish": "Account opening (khata kholna)"},
    "KYC Update": {"hi": "केवाईसी अपडेट", "hinglish": "KYC update"},
    "Address Change": {"hi": "पता परिवर्तन", "hinglish": "Address change"},
    "PAN Update": {"hi": "पैन अपडेट", "hinglish": "PAN update"},
    "Loan Enquiry": {"hi": "ऋण पूछताछ", "hinglish": "Loan enquiry"},
    "Cheque-related Request": {"hi": "चेक संबंधी अनुरोध", "hinglish": "Cheque-related request"},
    "ATM / Debit Card Request": {"hi": "एटीएम / डेबिट कार्ड अनुरोध", "hinglish": "ATM / Debit card request"},
    "Aadhaar / Valid Photo ID": {"hi": "आधार / मान्य फोटो पहचान पत्र", "hinglish": "Aadhaar / valid photo ID"},
    "PAN Card": {"hi": "पैन कार्ड", "hinglish": "PAN card"},
    "Address Proof": {"hi": "पता प्रमाण", "hinglish": "Address proof"},
    "Passport-size Photograph": {"hi": "पासपोर्ट साइज़ फोटो", "hinglish": "Passport-size photo"},
    "Initial Deposit Amount": {"hi": "प्रारंभिक जमा राशि", "hinglish": "Initial deposit amount"},
    "Aadhaar / Valid ID": {"hi": "आधार / मान्य पहचान पत्र", "hinglish": "Aadhaar / valid ID"},
    "New Address Proof (utility bill, etc.)": {
        "hi": "नया पता प्रमाण (बिजली/पानी का बिल आदि)",
        "hinglish": "Naya address proof (utility bill, etc.)",
    },
    "Valid Photo ID": {"hi": "मान्य फोटो पहचान पत्र", "hinglish": "Valid photo ID"},
    "Passbook / Cheque Leaf": {"hi": "पासबुक / चेक पन्ना", "hinglish": "Passbook / cheque leaf"},
    "PAN Card Copy": {"hi": "पैन कार्ड की प्रति", "hinglish": "PAN card ki copy"},
    "Passbook": {"hi": "पासबुक", "hinglish": "Passbook"},
    "Income Proof / Salary Slips": {"hi": "आय प्रमाण / वेतन पर्ची", "hinglish": "Income proof / salary slips"},
    "Last 6 Months Bank Statement": {"hi": "पिछले 6 महीनों का बैंक स्टेटमेंट", "hinglish": "Pichle 6 mahine ka bank statement"},
    "Filled Requisition Slip": {"hi": "भरी हुई अनुरोध पर्ची", "hinglish": "Bhari hui requisition slip"},
    "Filled Card Request Form": {"hi": "भरा हुआ कार्ड अनुरोध फ़ॉर्म", "hinglish": "Bhara hua card request form"},
}


def _translate(label: str, lang: str) -> str:
    if normalize_lang(lang) == "en":
        return label
    return LABEL_TRANSLATIONS.get(label, {}).get(normalize_lang(lang), label)

CHECKLISTS: Dict[str, Dict] = {
    "account_opening": {
        "service_id": "account_opening",
        "service_name": "Account Opening",
        "documents": [
            {"doc_id": "id_proof", "label": "Aadhaar / Valid Photo ID", "required": True},
            {"doc_id": "pan_card", "label": "PAN Card", "required": True},
            {"doc_id": "address_proof", "label": "Address Proof", "required": True},
            {"doc_id": "photo", "label": "Passport-size Photograph", "required": True},
            {"doc_id": "initial_deposit", "label": "Initial Deposit Amount", "required": False},
        ],
    },
    "kyc_update": {
        "service_id": "kyc_update",
        "service_name": "KYC Update",
        "documents": [
            {"doc_id": "id_proof", "label": "Aadhaar / Valid ID", "required": True},
            {"doc_id": "pan_card", "label": "PAN Card", "required": True},
            {"doc_id": "address_proof", "label": "Address Proof", "required": True},
            {"doc_id": "photo", "label": "Passport-size Photograph", "required": True},
        ],
    },
    "address_change": {
        "service_id": "address_change",
        "service_name": "Address Change",
        "documents": [
            {"doc_id": "address_proof", "label": "New Address Proof (utility bill, etc.)", "required": True},
            {"doc_id": "id_proof", "label": "Valid Photo ID", "required": True},
            {"doc_id": "passbook", "label": "Passbook / Cheque Leaf", "required": False},
        ],
    },
    "pan_update": {
        "service_id": "pan_update",
        "service_name": "PAN Update",
        "documents": [
            {"doc_id": "pan_card", "label": "PAN Card Copy", "required": True},
            {"doc_id": "id_proof", "label": "Valid Photo ID", "required": True},
            {"doc_id": "passbook", "label": "Passbook", "required": False},
        ],
    },
    "loan_enquiry": {
        "service_id": "loan_enquiry",
        "service_name": "Loan Enquiry",
        "documents": [
            {"doc_id": "id_proof", "label": "Valid Photo ID", "required": True},
            {"doc_id": "address_proof", "label": "Address Proof", "required": True},
            {"doc_id": "income_proof", "label": "Income Proof / Salary Slips", "required": True},
            {"doc_id": "bank_statement", "label": "Last 6 Months Bank Statement", "required": True},
            {"doc_id": "photo", "label": "Passport-size Photograph", "required": False},
        ],
    },
    "cheque_request": {
        "service_id": "cheque_request",
        "service_name": "Cheque-related Request",
        "documents": [
            {"doc_id": "passbook", "label": "Passbook", "required": True},
            {"doc_id": "id_proof", "label": "Valid Photo ID", "required": False},
            {"doc_id": "request_slip", "label": "Filled Requisition Slip", "required": True},
        ],
    },
    "atm_card_request": {
        "service_id": "atm_card_request",
        "service_name": "ATM / Debit Card Request",
        "documents": [
            {"doc_id": "passbook", "label": "Passbook", "required": True},
            {"doc_id": "id_proof", "label": "Valid Photo ID", "required": True},
            {"doc_id": "request_form", "label": "Filled Card Request Form", "required": True},
        ],
    },
}


def list_services(lang: str = "en") -> List[Dict]:
    return [
        {"service_id": c["service_id"], "service_name": _translate(c["service_name"], lang)}
        for c in CHECKLISTS.values()
    ]


def get_checklist(service_id: str, lang: str = "en") -> Dict:
    checklist = CHECKLISTS.get(service_id)
    if not checklist:
        return None
    if normalize_lang(lang) == "en":
        return checklist
    translated = dict(checklist)
    translated["service_name"] = _translate(checklist["service_name"], lang)
    translated["documents"] = [
        {**doc, "label": _translate(doc["label"], lang)} for doc in checklist["documents"]
    ]
    return translated
