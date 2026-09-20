"""
Backend-side internationalisation helpers.

Bank Saathi supports three languages end-to-end: English ("en"), Hindi
("hi"), and Hinglish ("hinglish" - Hindi meaning written in Latin script,
the way most people actually text/speak). This module holds the shared
message templates used by services that generate human-readable text
(mainly the Error Checker and the Simple Language Assistant's fallback
note). Field/document/service labels live alongside their own data in
templates.py / checklists.py / branches.py and use the same lang codes.
"""
from typing import Dict

SUPPORTED_LANGUAGES = ("en", "hi", "hinglish")
DEFAULT_LANGUAGE = "en"


def normalize_lang(lang: str) -> str:
    lang = (lang or "").lower().strip()
    return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def pick(translations: Dict[str, str], lang: str) -> str:
    """Pick a translated string, falling back to English if a language is
    missing for a given key (so nothing ever renders blank)."""
    lang = normalize_lang(lang)
    return translations.get(lang) or translations.get("en") or ""


# --- Error Checker message templates -----------------------------------
# Each entry is a template with {field} / {suggestion_field} placeholders
# filled in by validation_service.py. Kept centralised so every language
# stays consistent across all 10 validation rules.

VALIDATION_MESSAGES = {
    "required_field_blank": {
        "en": "{field} is required and is currently empty.",
        "hi": "{field} आवश्यक है और अभी खाली है।",
        "hinglish": "{field} zaroori hai aur abhi khaali hai.",
    },
    "required_field_blank_suggestion": {
        "en": "Please fill in {field} before submitting.",
        "hi": "कृपया सबमिट करने से पहले {field} भरें।",
        "hinglish": "Submit karne se pehle {field} bhariye.",
    },
    "account_number_invalid": {
        "en": "Account number should be 9 to 18 digits with no letters or spaces.",
        "hi": "खाता संख्या 9 से 18 अंकों की होनी चाहिए, बिना अक्षर या स्पेस के।",
        "hinglish": "Account number 9 se 18 digits ka hona chahiye, bina letters ya space ke.",
    },
    "account_number_invalid_suggestion": {
        "en": "Please re-enter the correct account number from your passbook or cheque.",
        "hi": "कृपया अपनी पासबुक या चेक से सही खाता संख्या दोबारा दर्ज करें।",
        "hinglish": "Apni passbook ya cheque se sahi account number dobara daalein.",
    },
    "phone_invalid": {
        "en": "Phone number should be a valid 10-digit mobile number.",
        "hi": "फ़ोन नंबर एक मान्य 10 अंकों का मोबाइल नंबर होना चाहिए।",
        "hinglish": "Phone number ek valid 10-digit mobile number hona chahiye.",
    },
    "phone_invalid_suggestion": {
        "en": "Please enter a 10-digit number starting with 6, 7, 8, or 9.",
        "hi": "कृपया 6, 7, 8, या 9 से शुरू होने वाला 10 अंकों का नंबर दर्ज करें।",
        "hinglish": "6, 7, 8, ya 9 se shuru hone wala 10-digit number daalein.",
    },
    "email_invalid": {
        "en": "This does not look like a valid email address.",
        "hi": "यह एक मान्य ईमेल पता नहीं लगता।",
        "hinglish": "Yeh ek valid email address nahi lag raha.",
    },
    "email_invalid_suggestion": {
        "en": "Please enter an email in the format name@example.com.",
        "hi": "कृपया name@example.com प्रारूप में ईमेल दर्ज करें।",
        "hinglish": "name@example.com jaise format mein email daalein.",
    },
    "pan_invalid": {
        "en": "PAN number should be 10 characters, e.g. ABCDE1234F.",
        "hi": "पैन नंबर 10 अक्षरों का होना चाहिए, जैसे ABCDE1234F।",
        "hinglish": "PAN number 10 characters ka hona chahiye, jaise ABCDE1234F.",
    },
    "pan_invalid_suggestion": {
        "en": "Please double-check your PAN card and re-enter the number.",
        "hi": "कृपया अपना पैन कार्ड दोबारा जाँचें और नंबर फिर से दर्ज करें।",
        "hinglish": "Apna PAN card dobara check karke number phir se daalein.",
    },
    "date_invalid": {
        "en": "Date of birth is not in a recognisable date format.",
        "hi": "जन्म तिथि एक पहचानने योग्य प्रारूप में नहीं है।",
        "hinglish": "Date of birth ek pehchaanne layak format mein nahi hai.",
    },
    "date_invalid_suggestion": {
        "en": "Please use a format like DD-MM-YYYY, e.g. 15-08-1990.",
        "hi": "कृपया DD-MM-YYYY जैसे प्रारूप का उपयोग करें, जैसे 15-08-1990।",
        "hinglish": "DD-MM-YYYY jaisa format use karein, jaise 15-08-1990.",
    },
    "field_mismatch": {
        "en": "{field} and its confirmation do not match.",
        "hi": "{field} और उसकी पुष्टि मेल नहीं खाते।",
        "hinglish": "{field} aur uski confirmation match nahi kar rahi.",
    },
    "field_mismatch_suggestion": {
        "en": "Please re-enter {field} so both entries match exactly.",
        "hi": "कृपया {field} फिर से दर्ज करें ताकि दोनों प्रविष्टियाँ मेल खाएँ।",
        "hinglish": "{field} dobara daalein taaki dono entries match ho jaayein.",
    },
    "missing_consent": {
        "en": "Consent/declaration checkbox has not been accepted.",
        "hi": "सहमति/घोषणा चेकबॉक्स स्वीकार नहीं किया गया है।",
        "hinglish": "Consent/declaration checkbox accept nahi kiya gaya hai.",
    },
    "missing_consent_suggestion": {
        "en": "Please read and accept the declaration before submitting.",
        "hi": "कृपया सबमिट करने से पहले घोषणा पढ़ें और स्वीकार करें।",
        "hinglish": "Submit karne se pehle declaration padhkar accept karein.",
    },
    "missing_signature": {
        "en": "A signature could not be detected on the form.",
        "hi": "फ़ॉर्म पर हस्ताक्षर नहीं मिला।",
        "hinglish": "Form par signature detect nahi hua.",
    },
    "missing_signature_suggestion": {
        "en": "Please sign the form in the designated signature box.",
        "hi": "कृपया निर्धारित हस्ताक्षर बॉक्स में फ़ॉर्म पर हस्ताक्षर करें।",
        "hinglish": "Form par diye gaye signature box mein sign karein.",
    },
    "blank_whitespace": {
        "en": "{field} contains only spaces.",
        "hi": "{field} में केवल स्पेस हैं।",
        "hinglish": "{field} mein sirf space hai.",
    },
    "blank_whitespace_suggestion": {
        "en": "Please enter an actual value for {field}.",
        "hi": "कृपया {field} के लिए वास्तविक मान दर्ज करें।",
        "hinglish": "{field} ke liye asli value daalein.",
    },
}

# --- Simple Language Assistant fallback notes ---------------------------

LANGUAGE_ASSISTANT_NOTES = {
    "no_ai_configured": {
        "en": "No AI provider is configured, so this explanation was produced by a "
              "rule-based phrase simplifier rather than an AI model.",
        "hi": "कोई AI प्रोवाइडर कॉन्फ़िगर नहीं है, इसलिए यह व्याख्या एक नियम-आधारित "
              "सरलीकरण से बनाई गई है, AI मॉडल से नहीं।",
        "hinglish": "Koi AI provider configure nahi hai, isliye yeh explanation ek "
                    "rule-based simplifier se banayi gayi hai, AI model se nahi.",
    },
    "no_phrases_detected": {
        "en": "No known formal banking phrases were detected to simplify further. "
              "The text above is shown as-is.",
        "hi": "आगे सरल बनाने के लिए कोई ज्ञात औपचारिक बैंकिंग वाक्यांश नहीं मिला। "
              "ऊपर दिया गया टेक्स्ट जैसा है वैसा ही दिखाया गया है।",
        "hinglish": "Aur simple banane ke liye koi jaana-pehchaana formal banking "
                    "phrase nahi mila. Upar wala text jaisa hai waisa hi dikhaya gaya hai.",
    },
}

# --- Form Scanner field-status messages ---------------------------------

FORM_SCANNER_MESSAGES = {
    "detected_in_document": {
        "en": "'{label}' was detected in the uploaded document.",
        "hi": "'{label}' अपलोड किए गए दस्तावेज़ में मिला।",
        "hinglish": "'{label}' upload kiye gaye document mein mil gaya.",
    },
    "required_not_found": {
        "en": "'{label}' is required but was not found in the document.",
        "hi": "'{label}' आवश्यक है लेकिन दस्तावेज़ में नहीं मिला।",
        "hinglish": "'{label}' zaroori hai lekin document mein nahi mila.",
    },
    "optional_not_detected": {
        "en": "'{label}' is optional and was not clearly detected.",
        "hi": "'{label}' वैकल्पिक है और स्पष्ट रूप से नहीं मिला।",
        "hinglish": "'{label}' optional hai aur clearly detect nahi hua.",
    },
    "looks_filled": {
        "en": "'{label}' looks filled in.",
        "hi": "'{label}' भरा हुआ लग रहा है।",
        "hinglish": "'{label}' bhara hua lag raha hai.",
    },
    "required_empty": {
        "en": "'{label}' is required and is currently empty.",
        "hi": "'{label}' आवश्यक है और अभी खाली है।",
        "hinglish": "'{label}' zaroori hai aur abhi khaali hai.",
    },
    "optional_empty": {
        "en": "'{label}' is optional and currently empty.",
        "hi": "'{label}' वैकल्पिक है और अभी खाली है।",
        "hinglish": "'{label}' optional hai aur abhi khaali hai.",
    },
    "could_not_check": {
        "en": "Could not be automatically checked (see fallback_reason).",
        "hi": "स्वचालित रूप से जाँच नहीं हो सकी (fallback_reason देखें)।",
        "hinglish": "Automatically check nahi ho paya (fallback_reason dekhein).",
    },
}

# --- Misc shared strings -------------------------------------------------

MISC = {
    "token_disclaimer": {
        "en": "This is a prototype digital queue token generated by Bank Saathi. "
              "It is NOT an official bank-issued token and is not connected to any "
              "real bank branch system.",
        "hi": "यह Bank Saathi द्वारा बनाया गया एक प्रोटोटाइप डिजिटल क्यू टोकन है। "
              "यह कोई आधिकारिक बैंक-जारी टोकन नहीं है और किसी वास्तविक बैंक शाखा "
              "प्रणाली से जुड़ा नहीं है।",
        "hinglish": "Yeh Bank Saathi dwara banaya gaya ek prototype digital queue "
                    "token hai. Yeh koi official bank-issued token nahi hai aur "
                    "kisi real bank branch system se connected nahi hai.",
    },
    "no_errors_found": {
        "en": "No errors found.",
        "hi": "कोई त्रुटि नहीं मिली।",
        "hinglish": "Koi error nahi mila.",
    },
    "checklist_all_ready": {
        "en": "All required documents are ready.",
        "hi": "सभी आवश्यक दस्तावेज़ तैयार हैं।",
        "hinglish": "Sabhi zaroori documents ready hain.",
    },
    "checklist_remaining": {
        "en": "{count} required document(s) remaining",
        "hi": "{count} आवश्यक दस्तावेज़ बाकी हैं",
        "hinglish": "{count} zaroori document(s) baaki hain",
    },
}
