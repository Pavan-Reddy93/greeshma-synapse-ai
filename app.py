import streamlit as st
import requests
import os

# IBM watsonx credentials
API_KEY = "8sT77w4F4zYkwy9NO8cqqlzY9qoc6tybneUxBL87lgr0"
PROJECT_ID = "c5c2d49f-1292-41c3-a8dc-0009457902eb"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
IAM_URL = "https://iam.cloud.ibm.com/identity/token"
MODEL_ID = "ibm/granite-3-3-8b-instruct"

# Streamlit page setup
st.set_page_config(page_title="🐼 Greeshma Synapse AI", layout="centered")

st.markdown("<h1 style='text-align: center;'>🐼 Greeshma Synapse AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Generate intelligent proposals for any startup or innovation idea</p>", unsafe_allow_html=True)

# User input
prompt = st.text_area("💡 Enter your startup idea or concept below")

# Optional sections
st.markdown("### 📌 Optional Proposal Sections")
include_g2m = st.checkbox("📦 Include Go-to-Market Strategy", value=True)
include_funding = st.checkbox("💰 Include Funding Requirements", value=True)
include_team = st.checkbox("👥 Include Team Roles", value=True)
include_monetization = st.checkbox("📈 Include Monetization Model", value=True)

# Access token fetch
def get_access_token(api_key):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"apikey={api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response = requests.post(IAM_URL, headers=headers, data=data)
    return response.json()["access_token"]

# Call watsonx Granite LLM
def call_granite(prompt, token):
    url = f"{WATSONX_URL}/ml/v1/text/generation?version=2024-05-29"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # Build additional instructions
    sections = []
    if include_g2m:
        sections.append("Include a Go-to-Market Strategy.")
    if include_funding:
        sections.append("Describe possible funding requirements or estimates.")
    if include_team:
        sections.append("Suggest potential team roles or skill sets needed.")
    if include_monetization:
        sections.append("Add ideas for the monetization model.")

    final_prompt = (
        f"Generate a detailed business proposal for the following startup idea:\n\n"
        f"{prompt.strip()}\n\n"
        f"{' '.join(sections)}"
    )

    payload = {
        "model_id": MODEL_ID,
        "input": final_prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 10000,
            "min_new_tokens": 100
        },
        "project_id": PROJECT_ID
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        result = response.json()
        return result["results"][0]["generated_text"]
    except Exception as e:
        return f"Error generating response: {e}"

# Generate button
if st.button("✨ Generate Proposal"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Generating proposal..."):
            token = get_access_token(API_KEY)
            result = call_granite(prompt, token)
            st.success("Proposal generated!")
            st.text_area("📄 Generated Proposal", value=result, height=500)

# Footer
st.markdown("<hr><p style='text-align: center;'>Developed by <b>🐼 Pavanreddy Kasara</b></p>", unsafe_allow_html=True)
