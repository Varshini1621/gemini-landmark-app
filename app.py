import streamlit as st
import requests
import json

# Define your API key (replace with your actual key)
API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"

# Define the API URL
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

# ✅ Correct request format for Gemini API
data = {
    "contents": [
        {"parts": [{"text": "Tell me about the Eiffel Tower"}]}
    ]
}

# Debugging: Print JSON before sending
print("Sending data:", json.dumps(data, indent=2))

# Make API request
try:
    response = requests.post(url, json=data, headers=headers)
    response_json = response.json()

    # Debugging: Print API response
    print("Response:", json.dumps(response_json, indent=2))

except Exception as e:
    print("Error making API request:", e)
    response_json = {"error": str(e)}

# Display result in Streamlit
st.write(response_json)


