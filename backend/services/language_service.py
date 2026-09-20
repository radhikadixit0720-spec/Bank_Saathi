"""
Simple Language Assistant service.

If AI_PROVIDER_API_KEY (see config/settings.py) is configured, this module
is where a real LLM call would be made to produce the simplified
explanation. Since no key is required to run Bank Saathi, a deterministic,
rule-based fallback (backend/data/phrasebook.py) is used instead - it is a
genuine working feature, not a stub, and every response clearly reports
which method produced it via the `method` field.

The phrasebook itself only recognises English formal-banking phrases (that
is the input this feature is designed for - simplifying bank notices/forms,
which are almost always issued in English). The `note` and `method` fields
returned to the user, however, are shown in whichever of English / Hindi /
Hinglish the user has selected, via backend/data/i18n.py.
"""
import re
from typing import Dict

from backend.config.settings import settings
from backend.data.i18n import LANGUAGE_ASSISTANT_NOTES, normalize_lang, pick
from backend.data.phrasebook import apply_phrasebook


def _rule_based_simplify(text: str) -> str:
    simplified = apply_phrasebook(text)

    # Light readability clean-up: split long sentences on semicolons, and
    # shorten common bureaucratic connectors.
    simplified = re.sub(r"\s*;\s*", ". ", simplified)
    simplified = re.sub(r"\.{2,}", ".", simplified)
    simplified = re.sub(r"\s{2,}", " ", simplified).strip()
    return simplified


def _call_ai_provider(text: str) -> str:
    """Placeholder for a real LLM call. Intentionally not implemented with
    a hard-coded/fake response - wire this up to the Anthropic API (or
    another provider) using settings.AI_PROVIDER_API_KEY /
    settings.AI_PROVIDER_MODEL when available."""
    raise NotImplementedError(
        "AI_PROVIDER_API_KEY is set, but no AI provider client is wired up "
        "yet in services/language_service.py._call_ai_provider(). Implement "
        "the API call there to enable AI-generated simplifications."
    )


def simplify_text(text: str, lang: str = "en") -> Dict:
    lang = normalize_lang(lang)
    text = text.strip()

    if settings.AI_PROVIDER_API_KEY:
        try:
            explanation = _call_ai_provider(text)
            return {
                "original_text": text,
                "simple_explanation": explanation,
                "method": "ai_provider",
                "note": "",
            }
        except NotImplementedError:
            pass  # fall through to rule-based fallback below

    simplified = _rule_based_simplify(text)
    changed = simplified.strip().lower() != text.strip().lower()

    return {
        "original_text": text,
        "simple_explanation": simplified if changed else (
            f"{text}\n\n({pick(LANGUAGE_ASSISTANT_NOTES['no_phrases_detected'], lang)})"
        ),
        "method": "rule_based_fallback",
        "note": pick(LANGUAGE_ASSISTANT_NOTES["no_ai_configured"], lang),
    }
