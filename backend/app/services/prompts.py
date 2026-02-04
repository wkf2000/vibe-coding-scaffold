ENRICH_SYSTEM_PROMPT = (
    "You generate structured metadata for operational text. "
    "Return ONLY valid JSON matching the provided schema. No markdown."
)

ENRICH_USER_PROMPT = """Text:
{text}

Return JSON with:
- summary (1-2 sentences)
- category: incident|request|question|update|other
- priority: P0|P1|P2|P3
- tags: 3-8 strings
- action_items: 0-5 strings
"""
