import streamlit as st
import requests
import json

# Define your API key
API_KEY = "AIzaSyAa34bcboGH5vOLBqIbXJhUWW4A8m2CGco"

# Google Gemini API Endpoint
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={AIzaSyAa34bcboGH5vOLBqIbXJhUWW4A8m2CGco}"

headers = {
    "Content-Type": "application/json"
}

# Example data you are sending
data = {
    "contents": [{"parts": [{"text": "Eiffel Tower"}]}]  # Modify based on your app logic
}

# Debugging: Print the JSON data before sending
print("Sending data:", json.dumps(data, indent=2))

# Make the API request
try:
    response = requests.post(url, json=data, headers=headers)
    response_json = response.json()

    # Debugging: Print the API response
    print("Response:", json.dumps(response_json, indent=2))

except Exception as e:
    print("Error making API request:", e)

# Display result in Streamlit
st.write(response_json)

