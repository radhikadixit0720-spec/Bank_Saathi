"""
Rule-based phrase substitutions used as the offline fallback for the
Simple Language Assistant when no AI provider API key is configured (see
services/language_service.py). This is a real, working feature on its own
- not a placeholder - it just uses pattern replacement instead of an LLM.

Keys are lowercase phrases/regex-free substrings commonly found in formal
banking language; values are their plain-language equivalents.
"""
from typing import List, Tuple

# Ordered so longer/more specific phrases are checked before shorter ones.
PHRASE_MAP: List[Tuple[str, str]] = [
    ("please furnish proof of residential address", "Please provide a document that shows where you live."),
    ("kindly furnish", "Please provide"),
    ("please furnish", "Please provide"),
    ("proof of residential address", "a document that shows where you live"),
    ("proof of identity", "a document that proves who you are"),
    ("permanent account number", "PAN card number"),
    ("know your customer", "identity verification (KYC)"),
    ("in the event of", "if"),
    ("prior to", "before"),
    ("subsequent to", "after"),
    ("aforementioned", "mentioned above"),
    ("undersigned", "the person signing this"),
    ("hereby declare", "confirm"),
    ("hereby", "by this document"),
    ("duly filled", "completely filled"),
    ("duly signed", "properly signed"),
    ("shall be required to", "must"),
    ("shall be liable", "will be responsible"),
    ("is liable to", "may have to"),
    ("in lieu of", "instead of"),
    ("at the earliest", "as soon as possible"),
    ("kindly note", "please note"),
    ("with immediate effect", "starting now"),
    ("as per the extant guidelines", "according to current rules"),
    ("extant guidelines", "current rules"),
    ("statutory requirement", "legal requirement"),
    ("non-compliance", "not following the rules"),
    ("indemnify", "protect from financial loss"),
    ("nomination facility", "option to name someone to receive your funds"),
    ("cheque book requisition", "request for a new chequebook"),
    ("requisition slip", "request form"),
    ("outstanding dues", "unpaid amount"),
    ("account holder", "person who owns the account"),
    ("joint holder", "co-owner of the account"),
    ("minor account", "bank account for a child"),
    ("standing instruction", "automatic recurring payment"),
    ("demand draft", "a bank-issued payment order"),
    ("net banking", "online banking"),
    ("statement of account", "account statement"),
    ("branch manager", "branch in-charge"),
]


def apply_phrasebook(text: str) -> str:
    """Apply a naive, deterministic phrase substitution. This never
    fabricates meaning - it only swaps known formal phrases for their
    simple equivalents and leaves everything else untouched."""
    result = text
    lowered = text.lower()
    for formal, simple in PHRASE_MAP:
        if formal in lowered:
            # case-insensitive replace, preserving the rest of the string
            start = lowered.find(formal)
            while start != -1:
                result = result[:start] + simple + result[start + len(formal):]
                lowered = result.lower()
                start = lowered.find(formal, start + len(simple))
    return result
