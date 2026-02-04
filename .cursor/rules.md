# Cursor Rules (Project)

- First write a concise plan, then implement.
- Prefer small patches; avoid sweeping refactors.
- If you add an endpoint: add schemas + logs + at least one pytest.
- If you add an integration: add timeout/retries + error handling; never log secrets.
