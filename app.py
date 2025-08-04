import streamlit as st
import requests
import os

# IBM watsonx credentials (Replace with yours directly or use environment variables)
API_KEY = "8sT77w4F4zYkwy9NO8cqqlzY9qoc6tybneUxBL87lgr0"
PROJECT_ID = "c5c2d49f-1292-41c3-a8dc-0009457902eb"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
IAM_URL = "https://iam.cloud.ibm.com/identity/token"
MODEL_ID = "ibm/granite-3-3-8b-instruct"

# Page configuration
st.set_page_config(page_title="🐼 Greeshma Synapse AI", layout="centered")

# Header
st.markdown("<h1 style='text-align: center;'>🐼 Greeshma Synapse AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Generate AI-powered proposals for agritech ideas</p>", unsafe_allow_html=True)

# User Input
prompt = st.text_area("💡 Enter your startup idea or concept below")

# Access token function
def get_access_token(api_key):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"apikey={api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response = requests.post(IAM_URL, headers=headers, data=data)
    return response.json()["access_token"]

# Call IBM watsonx Granite model
def call_granite(prompt, token):
    url = f"{WATSONX_URL}/ml/v1/text/generation?version=2024-05-29"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
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

# Generate Proposal Button
if st.button("✨ Generate Proposal"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Generating proposal..."):
            token = get_access_token(API_KEY)
            result = call_granite(prompt, token)
            st.success("Proposal generated!")
            st.text_area("📄 Generated Proposal", value=result, height=400)

# Footer
st.markdown("<hr><p style='text-align: center;'>Developed by <b>🐼 Pavanreddy Kasara</b></p>", unsafe_allow_html=True)
