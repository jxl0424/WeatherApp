import re

_PATTERNS = [
    r"ignore\s+(previous|prior|above|all)\s+(instructions?|rules?|directives?|context)",
    r"disregard\s+(the\s+)?(system|previous|above)",
    r"you\s+are\s+now\b",
    r"forget\s+(your|the|all)\s+(instructions?|rules?|prompt|context)",
    r"new\s+instructions",
    r"developer\s+mode",
    r"jailbreak",
    r"\bDAN\b",
    r"prompt\s+injection",
    r"reveal\s+(your|the)\s+(system\s+)?prompt",
    r"repeat\s+(your|the)\s+(system\s+)?instructions",
    r"override\s+(your|the)\s+(instructions?|rules?|system)",
    r"pretend\s+(you\s+are|to\s+be)\s+(?!uncertain|unsure)",
    r"ignore\s+all\s+previous",
    r"act\s+as\s+(?:if\s+)?(?:you\s+(?:are|were)\s+)?(?:a\s+)?(?:different|new|another|unrestricted)",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in _PATTERNS]

REFUSAL = "I can only help with weather and travel questions."


def is_likely_injection(text: str) -> bool:
    return any(p.search(text) for p in _COMPILED)
