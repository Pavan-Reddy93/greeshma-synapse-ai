# 🐼 Greeshma Synapse AI – IBM watsonx Proposal Generator

Greeshma Synapse AI is a user-friendly Streamlit app that generates AI-powered proposals using the **IBM watsonx Granite 3-3-8b** language model. You input your agritech startup idea or project concept, and the app returns a detailed, professional proposal.

---

## 🚀 Features

- Accepts user input for idea or concept
- Sends request to IBM watsonx Granite model
- Displays generated proposal
- Clean and minimal UI, ready for cloud deployment
- No image or background dependencies (cloud-compatible)
- 🔐 Credentials can be switched to `.env` for security

---

## 🛠️ Tech Stack

- Python
- Streamlit
- IBM watsonx.ai (Granite Model)
- Requests library

---

## 📦 Installation

```bash
git clone https://github.com/Pavan-Reddy93/greeshma-synapse-ai.git
cd greeshma-synapse-ai
pip install -r requirements.txt
streamlit run app.py
