import streamlit as st
import requests

API_KEY = "8sT77w4F4zYkwy9NO8cqqlzY9qoc6tybneUxBL87lgr0"
PROJECT_ID = "c5c2d49f-1292-41c3-a8dc-0009457902eb"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
IAM_URL = "https://iam.cloud.ibm.com/identity/token"
MODEL_ID = "ibm/granite-3-3-8b-instruct"


st.set_page_config(page_title="🐼 Greeshma Synapse AI", layout="centered")

st.markdown("<h1 style='text-align: center;'>🐼 Greeshma Synapse AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Startup Blueprint Generator</h4>", unsafe_allow_html=True)
st.markdown("Transform your raw startup idea into a detailed, investor-ready proposal using IBM watsonx.")


startup_name = st.text_input("🏷️ Enter your Startup Name (optional)")
prompt = st.text_area("💡 Describe your startup idea")

st.markdown("### 📌 Optional Sections to Include")
include_g2m = st.checkbox("📦 Go-to-Market Strategy", value=True)
include_funding = st.checkbox("💰 Funding Requirements", value=True)
include_team = st.checkbox("👥 Team Roles & Skills", value=True)
include_monetization = st.checkbox("📈 Monetization Model", value=True)

def get_access_token(api_key):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"apikey={api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response = requests.post(IAM_URL, headers=headers, data=data)
    return response.json().get("access_token")

def call_granite(prompt, token):
    url = f"{WATSONX_URL}/ml/v1/text/generation?version=2024-05-29"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    sections = []
    if include_g2m:
        sections.append("Include a detailed Go-to-Market Strategy.")
    if include_funding:
        sections.append("Outline possible funding requirements and estimates.")
    if include_team:
        sections.append("Describe the core team roles and skill sets needed.")
    if include_monetization:
        sections.append("Propose a monetization model suited to this idea.")

    # Final Prompt Construction
    final_prompt = (
        f"Generate a professional startup blueprint for the following idea:\n\n"
        f"Startup Name: {startup_name if startup_name else 'N/A'}\n"
        f"Idea: {prompt.strip()}\n\n"
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
        return f" Error generating response: {e}"


if st.button(" Generate Proposal"):
    if prompt.strip() == "":
        st.warning("Please enter your startup idea.")
    else:
        with st.spinner("Generating your startup blueprint..."):
            token = get_access_token(API_KEY)
            output = call_granite(prompt, token)
            st.success("Startup Blueprint Generated!")
            st.text_area("Blueprint Output", value=output, height=500)

st.markdown("<hr><p style='text-align: center;'>Developed by <b>🐼 Pavanreddy Kasara</b> | Powered by IBM watsonx</p>", unsafe_allow_html=True)
