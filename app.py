import streamlit as st
import requests
import json

# Define your API key
API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"

# Define the API URL
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

# User input for dynamic query
query = st.text_input("Enter a landmark name:", "Eiffel Tower")

if st.button("Get Landmark Info"):
    data = {
        "contents": [
            {"parts": [{"text": query}]}
        ]
    }

    # Make API request
    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()

        # ✅ Extracting the generated text
        if "candidates" in response_json:
            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown(generated_text)  # Display the result in Markdown format
        else:
            st.error("No response received. Please try again.")

    except Exception as e:
        st.error(f"Error making API request: {e}")

