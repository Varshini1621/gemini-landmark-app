import streamlit as st
import requests
import base64
import json

# 🔑 Replace with your API Keys
GEMINI_API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"
VISION_API_KEY = "AIzaSyDmMQ6qprPCRLR-Ck6d2mCqXDk-ALD3X20"

# API Endpoints
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
VISION_URL = f"https://vision.googleapis.com/v1/images:annotate?key={VISION_API_KEY}"

# Function to detect landmarks from an image using Google Vision API
def detect_landmark(image_data):
    request_payload = {
        "requests": [
            {
                "image": {"content": image_data},
                "features": [{"type": "LANDMARK_DETECTION"}],
            }
        ]
    }

    response = requests.post(VISION_URL, json=request_payload)
    result = response.json()

    if "responses" in result and "landmarkAnnotations" in result["responses"][0]:
        landmark_info = result["responses"][0]["landmarkAnnotations"][0]
        return landmark_info["description"], landmark_info.get("locations", [{}])[0].get("latLng", {})
    else:
        return "No landmark detected!", {}

# Function to fetch landmark details using Google Gemini API
def get_landmark_info(landmark_name):
    request_payload = {
        "contents": [
            {"parts": [{"text": f"Give me detailed information about {landmark_name}."}]}
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_URL, headers=headers, json=request_payload)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Error fetching data. Please check your API key and settings."

# Streamlit UI
st.title("🌍 Landmark Recognition App")

# Input Option: Text or Image
option = st.radio("Choose Input Type:", ["Enter Landmark Name", "Upload an Image"])

if option == "Enter Landmark Name":
    landmark_name = st.text_input("Enter Landmark Name:")
    if st.button("Get Info"):
        if landmark_name:
            info = get_landmark_info(landmark_name)
            st.write(f"### 📍 {landmark_name}")
            st.write(info)
        else:
            st.warning("Please enter a landmark name!")

elif option == "Upload an Image":
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        if st.button("Detect Landmark"):
            landmark_name, location = detect_landmark(image_base64)
            st.write(f"**Landmark Detected:** {landmark_name}")
            if location:
                st.write(f"📍 Location: {location}")


