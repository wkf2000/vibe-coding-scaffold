import os
import httpx
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="GenAI Service Demo", layout="centered")
st.title("GenAI Service Demo")
st.caption("Fast validation UI for /v1/enrich")

text = st.text_area("Input text", height=220, placeholder="Paste an incident, ticket, email, or spec...")
locale = st.text_input("Locale", value="en-US")
request_id = st.text_input("Request ID (optional)", value="")

if st.button("Enrich", type="primary"):
    if not text.strip():
        st.error("Please enter text.")
    else:
        headers = {}
        if request_id.strip():
            headers["x-request-id"] = request_id.strip()

        try:
            resp = httpx.post(
                f"{BACKEND_URL}/v1/enrich",
                json={"text": text, "locale": locale},
                headers=headers,
                timeout=30,
            )
            st.write("Status:", resp.status_code)
            st.json(resp.json())
        except Exception as e:
            st.error(f"Request failed: {e}")
