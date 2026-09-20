"""
Predefined bank form templates.

These act as the "expected field list" that an uploaded/scanned form is
compared against in the Form Scanner feature. In a production system these
would live in the `form_templates` MongoDB collection and be manageable by
bank admins; here they are seeded as static, well-structured data so the
rest of the app (services, routes) can be written against a stable shape
and later swapped for a database-backed version with no other changes.

Field labels are stored in English and translated on the fly via
LABEL_TRANSLATIONS so the Form Scanner works the same way in English,
Hindi, and Hinglish (see backend/data/i18n.py for the language codes).
"""
from typing import Dict, List, TypedDict

from backend.data.i18n import normalize_lang


class TemplateField(TypedDict):
    field_id: str
    label: str
    required: bool
    # simple synonyms/keywords used to detect this field inside free text
    # extracted from an uploaded document (see services/form_scanner_service.py)
    keywords: List[str]


# English label -> {hi, hinglish}. Centralised because the same field
# labels (e.g. "Signature", "Account Number") repeat across templates.
LABEL_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "Customer Name": {"hi": "ग्राहक का नाम", "hinglish": "Customer ka naam"},
    "Account Holder Name": {"hi": "खाताधारक का नाम", "hinglish": "Account holder ka naam"},
    "Card Holder Name": {"hi": "कार्डधारक का नाम", "hinglish": "Card holder ka naam"},
    "Applicant Name": {"hi": "आवेदक का नाम", "hinglish": "Applicant ka naam"},
    "Date of Birth": {"hi": "जन्म तिथि", "hinglish": "Date of Birth (janm tithi)"},
    "Address": {"hi": "पता", "hinglish": "Address (pata)"},
    "Mobile Number": {"hi": "मोबाइल नंबर", "hinglish": "Mobile number"},
    "PAN Number": {"hi": "पैन नंबर", "hinglish": "PAN number"},
    "Aadhaar Number": {"hi": "आधार नंबर", "hinglish": "Aadhaar number"},
    "Nominee Name": {"hi": "नामिती का नाम", "hinglish": "Nominee ka naam"},
    "Signature": {"hi": "हस्ताक्षर", "hinglish": "Signature (dastkhat)"},
    "Account Number": {"hi": "खाता संख्या", "hinglish": "Account number"},
    "Identity Proof Number": {"hi": "पहचान प्रमाण संख्या", "hinglish": "ID proof number"},
    "Old Address": {"hi": "पुराना पता", "hinglish": "Purana address"},
    "New Address": {"hi": "नया पता", "hinglish": "Naya address"},
    "Address Proof Document": {"hi": "पता प्रमाण दस्तावेज़", "hinglish": "Address proof document"},
    "Loan Type": {"hi": "ऋण का प्रकार", "hinglish": "Loan type"},
    "Requested Amount": {"hi": "अनुरोधित राशि", "hinglish": "Requested amount"},
    "Income Proof": {"hi": "आय प्रमाण", "hinglish": "Income proof"},
    "Number of Cheque Leaves": {"hi": "चेक पन्नों की संख्या", "hinglish": "Cheque leaves ki sankhya"},
    "Card Type Requested": {"hi": "अनुरोधित कार्ड प्रकार", "hinglish": "Requested card type"},
}


def translate_label(label: str, lang: str = "en") -> str:
    lang = normalize_lang(lang)
    if lang == "en":
        return label
    translation = LABEL_TRANSLATIONS.get(label, {})
    return translation.get(lang, label)


FORM_TEMPLATES: Dict[str, Dict] = {
    "account_opening": {
        "template_id": "account_opening",
        "name": "Account Opening Form",
        "fields": [
            {"field_id": "full_name", "label": "Customer Name", "required": True,
             "keywords": ["name", "customer name", "applicant name"]},
            {"field_id": "date_of_birth", "label": "Date of Birth", "required": True,
             "keywords": ["date of birth", "dob"]},
            {"field_id": "address", "label": "Address", "required": True,
             "keywords": ["address", "residential address"]},
            {"field_id": "mobile_number", "label": "Mobile Number", "required": True,
             "keywords": ["mobile", "phone", "contact number"]},
            {"field_id": "pan_number", "label": "PAN Number", "required": True,
             "keywords": ["pan", "pan number", "permanent account number"]},
            {"field_id": "aadhaar_number", "label": "Aadhaar Number", "required": True,
             "keywords": ["aadhaar", "aadhar", "uid"]},
            {"field_id": "nominee_name", "label": "Nominee Name", "required": False,
             "keywords": ["nominee"]},
            {"field_id": "signature", "label": "Signature", "required": True,
             "keywords": ["signature", "sign"]},
        ],
    },
    "kyc_update": {
        "template_id": "kyc_update",
        "name": "KYC Update Form",
        "fields": [
            {"field_id": "account_number", "label": "Account Number", "required": True,
             "keywords": ["account number", "a/c no"]},
            {"field_id": "full_name", "label": "Customer Name", "required": True,
             "keywords": ["name", "customer name"]},
            {"field_id": "date_of_birth", "label": "Date of Birth", "required": True,
             "keywords": ["date of birth", "dob"]},
            {"field_id": "address", "label": "Address", "required": True,
             "keywords": ["address"]},
            {"field_id": "id_proof", "label": "Identity Proof Number", "required": True,
             "keywords": ["aadhaar", "passport", "voter id", "id proof"]},
            {"field_id": "signature", "label": "Signature", "required": True,
             "keywords": ["signature", "sign"]},
        ],
    },
    "address_change": {
        "template_id": "address_change",
        "name": "Address Change Request",
        "fields": [
            {"field_id": "account_number", "label": "Account Number", "required": True,
             "keywords": ["account number", "a/c no"]},
            {"field_id": "old_address", "label": "Old Address", "required": False,
             "keywords": ["old address", "previous address"]},
            {"field_id": "new_address", "label": "New Address", "required": True,
             "keywords": ["new address", "current address"]},
            {"field_id": "address_proof", "label": "Address Proof Document", "required": True,
             "keywords": ["address proof", "utility bill"]},
            {"field_id": "signature", "label": "Signature", "required": True,
             "keywords": ["signature", "sign"]},
        ],
    },
    "pan_update": {
        "template_id": "pan_update",
        "name": "PAN Update Form",
        "fields": [
            {"field_id": "account_number", "label": "Account Number", "required": True,
             "keywords": ["account number", "a/c no"]},
            {"field_id": "full_name", "label": "Customer Name", "required": True,
             "keywords": ["name"]},
            {"field_id": "pan_number", "label": "PAN Number", "required": True,
             "keywords": ["pan", "permanent account number"]},
            {"field_id": "signature", "label": "Signature", "required": True,
             "keywords": ["signature", "sign"]},
        ],
    },
    "loan_enquiry": {
        "template_id": "loan_enquiry",
        "name": "Loan Enquiry Form",
        "fields": [
            {"field_id": "full_name", "label": "Applicant Name", "required": True,
             "keywords": ["name", "applicant"]},
            {"field_id": "mobile_number", "label": "Mobile Number", "required": True,
             "keywords": ["mobile", "phone"]},
            {"field_id": "loan_type", "label": "Loan Type", "required": True,
             "keywords": ["loan type", "loan category"]},
            {"field_id": "loan_amount", "label": "Requested Amount", "required": True,
             "keywords": ["amount", "loan amount"]},
            {"field_id": "income_proof", "label": "Income Proof", "required": False,
             "keywords": ["income proof", "salary slip"]},
        ],
    },
    "cheque_request": {
        "template_id": "cheque_request",
        "name": "Cheque Book / Cheque Related Request",
        "fields": [
            {"field_id": "account_number", "label": "Account Number", "required": True,
             "keywords": ["account number", "a/c no"]},
            {"field_id": "full_name", "label": "Account Holder Name", "required": True,
             "keywords": ["name"]},
            {"field_id": "leaves_requested", "label": "Number of Cheque Leaves", "required": False,
             "keywords": ["leaves", "cheque leaves"]},
            {"field_id": "signature", "label": "Signature", "required": True,
             "keywords": ["signature", "sign"]},
        ],
    },
    "atm_card_request": {
        "template_id": "atm_card_request",
        "name": "ATM / Debit Card Request",
        "fields": [
            {"field_id": "account_number", "label": "Account Number", "required": True,
             "keywords": ["account number", "a/c no"]},
            {"field_id": "full_name", "label": "Card Holder Name", "required": True,
             "keywords": ["name"]},
            {"field_id": "mobile_number", "label": "Mobile Number", "required": True,
             "keywords": ["mobile", "phone"]},
            {"field_id": "card_type", "label": "Card Type Requested", "required": False,
             "keywords": ["card type"]},
            {"field_id": "signature", "label": "Signature", "required": True,
             "keywords": ["signature", "sign"]},
        ],
    },
}


NAME_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "Account Opening Form": {"hi": "खाता खोलने का फ़ॉर्म", "hinglish": "Account opening form"},
    "KYC Update Form": {"hi": "केवाईसी अपडेट फ़ॉर्म", "hinglish": "KYC update form"},
    "Address Change Request": {"hi": "पता परिवर्तन अनुरोध", "hinglish": "Address change request"},
    "PAN Update Form": {"hi": "पैन अपडेट फ़ॉर्म", "hinglish": "PAN update form"},
    "Loan Enquiry Form": {"hi": "ऋण पूछताछ फ़ॉर्म", "hinglish": "Loan enquiry form"},
    "Cheque Book / Cheque Related Request": {"hi": "चेक बुक / चेक संबंधी अनुरोध", "hinglish": "Cheque book / cheque related request"},
    "ATM / Debit Card Request": {"hi": "एटीएम / डेबिट कार्ड अनुरोध", "hinglish": "ATM / Debit card request"},
}


def list_templates(lang: str = "en") -> List[Dict]:
    return [
        {
            "template_id": t["template_id"],
            "name": t["name"] if normalize_lang(lang) == "en" else NAME_TRANSLATIONS.get(t["name"], {}).get(normalize_lang(lang), t["name"]),
            "field_count": len(t["fields"]),
        }
        for t in FORM_TEMPLATES.values()
    ]


def get_template(template_id: str, lang: str = "en") -> Dict:
    template = FORM_TEMPLATES.get(template_id)
    if not template:
        return None
    if normalize_lang(lang) == "en":
        return template
    translated = dict(template)
    translated["name"] = NAME_TRANSLATIONS.get(template["name"], {}).get(normalize_lang(lang), template["name"])
    translated["fields"] = [
        {**field, "label": translate_label(field["label"], lang)} for field in template["fields"]
    ]
    return translated
