import streamlit as st
import requests
import json
import base64

# Google Vision API Key (Replace with your actual API Key)
API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"
VISION_API_URL = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"

st.title("Landmark Recognition App")

# Choose between text input and image upload
option = st.radio("Choose Input Method:", ["Enter Landmark Name", "Upload an Image"])

if option == "Enter Landmark Name":
    query = st.text_input("Enter the landmark name:")

    if st.button("Get Info"):
        if query:
            url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            data = {"contents": [{"parts": [{"text": query}]}]}
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                st.write(response.json())
            else:
                st.error("Failed to retrieve data!")

elif option == "Upload an Image":
    uploaded_file = st.file_uploader("Upload an image of a landmark", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        vision_payload = {
            "requests": [
                {
                    "image": {"content": encoded_image},
                    "features": [{"type": "LANDMARK_DETECTION"}]
                }
            ]
        }

        response = requests.post(VISION_API_URL, json=vision_payload)
        result = response.json()

        if "responses" in result and "landmarkAnnotations" in result["responses"][0]:
            landmark = result["responses"][0]["landmarkAnnotations"][0]["description"]
            st.success(f"Landmark detected: {landmark}")
        else:
            st.error("No landmark detected!")

