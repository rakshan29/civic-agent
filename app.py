import streamlit as st
from backend import triage_citizen_issue

st.set_page_config(page_title="Civic Agent", page_icon="🏛️", layout="wide")

st.title("🏛️ Civic Agent: Localized AI Triage Agent")
st.caption("Empowering communities with real-time AI issue routing & municipal classification.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Submit Citizen Issue")
    issue_input = st.text_area("Describe the issue in detail:", placeholder="e.g. Open drain overflow near the public clinic...", height=120)
    location_input = st.text_input("Location / Ward Number:", value="Ward 12")
    submit_btn = st.button("Submit & Route Issue", type="primary")

with col2:
    st.subheader("AI Agent Dispatch Output")
    if submit_btn and issue_input.strip():
        with st.spinner("Agent classifying & parsing JSON schema..."):
            try:
                result = triage_citizen_issue(issue_input, location_input)
                
                # Render badges
                urgency_color = "red" if result.urgency_level in ["CRITICAL", "HIGH"] else "orange"
                st.markdown(f"**Category:** `{result.category}`")
                st.markdown(f"**Urgency:** :{urgency_color}[{result.urgency_level}]")
                st.markdown(f"**Target Department Webhook:** `{result.department_webhook}`")
                
                st.write("**Extracted Entities:**", ", ".join(result.extracted_entities))
                st.success(f"**Generated Citizen Response:**\n{result.community_response}")
                
            except Exception as e:
                st.error(f"Error executing agent pipeline: {e}")
    else:
        st.info("Fill out the citizen issue form on the left and click submit.")
