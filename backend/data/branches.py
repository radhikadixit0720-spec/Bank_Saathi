"""
Prototype branch and service directory used by the Branch Token /
Appointment feature. This is intentionally NOT connected to any real bank
core-banking system - it only exists to demonstrate a digital queue/token
workflow. See services/token_service.py for the disclaimer surfaced to the
user in every API response.
"""
from typing import Dict, List

from backend.data.i18n import normalize_lang

BRANCHES: List[Dict] = [
    {"branch_id": "br_indore_mg_road", "name": "MG Road Branch", "city": "Indore"},
    {"branch_id": "br_indore_vijay_nagar", "name": "Vijay Nagar Branch", "city": "Indore"},
    {"branch_id": "br_bhopal_mp_nagar", "name": "MP Nagar Branch", "city": "Bhopal"},
    {"branch_id": "br_mumbai_andheri", "name": "Andheri Branch", "city": "Mumbai"},
    {"branch_id": "br_delhi_cp", "name": "Connaught Place Branch", "city": "Delhi"},
]

BRANCH_SERVICES: List[Dict] = [
    {"service_id": "account_opening", "service_name": "Account Opening", "prefix": "A"},
    {"service_id": "kyc_update", "service_name": "KYC Update", "prefix": "K"},
    {"service_id": "address_change", "service_name": "Address Change", "prefix": "D"},
    {"service_id": "pan_update", "service_name": "PAN Update", "prefix": "P"},
    {"service_id": "loan_enquiry", "service_name": "Loan Enquiry", "prefix": "L"},
    {"service_id": "cheque_request", "service_name": "Cheque Request", "prefix": "C"},
    {"service_id": "atm_card_request", "service_name": "ATM/Debit Card Request", "prefix": "M"},
]

SERVICE_NAME_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "Account Opening": {"hi": "खाता खोलना", "hinglish": "Account opening"},
    "KYC Update": {"hi": "केवाईसी अपडेट", "hinglish": "KYC update"},
    "Address Change": {"hi": "पता परिवर्तन", "hinglish": "Address change"},
    "PAN Update": {"hi": "पैन अपडेट", "hinglish": "PAN update"},
    "Loan Enquiry": {"hi": "ऋण पूछताछ", "hinglish": "Loan enquiry"},
    "Cheque Request": {"hi": "चेक अनुरोध", "hinglish": "Cheque request"},
    "ATM/Debit Card Request": {"hi": "एटीएम/डेबिट कार्ड अनुरोध", "hinglish": "ATM/Debit card request"},
}


def list_branches() -> List[Dict]:
    return BRANCHES


def list_branch_services(lang: str = "en") -> List[Dict]:
    lang = normalize_lang(lang)
    if lang == "en":
        return BRANCH_SERVICES
    return [
        {**s, "service_name": SERVICE_NAME_TRANSLATIONS.get(s["service_name"], {}).get(lang, s["service_name"])}
        for s in BRANCH_SERVICES
    ]


def get_branch(branch_id: str) -> Dict:
    return next((b for b in BRANCHES if b["branch_id"] == branch_id), None)


def get_service(service_id: str) -> Dict:
    return next((s for s in BRANCH_SERVICES if s["service_id"] == service_id), None)
