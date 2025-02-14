import streamlit as st
import requests
import base64
import json

# Google Cloud Vision API Key
VISION_API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"
VISION_URL = f"https://vision.googleapis.com/v1/images:annotate?key={VISION_API_KEY}"

# Google Gemini API Key
GEMINI_API_KEY = "AIzaSyDmMQ6qprPCRLR-Ck6d2mCqXDk-ALD3X20"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

# Streamlit UI with a peach background
st.markdown(
    """
    <style>
        body { background-color: #FFDAB9; }  /* Peach Background */
        .title { text-align: center; font-size: 40px; color: black; font-weight: bold; }
        .input-text, .upload-label { color: black; font-size: 20px; font-weight: bold; }
        .emoji { font-size: 30px; text-align: center; }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown('<p class="title">📸 Landmark Lens 🌍</p>', unsafe_allow_html=True)

# Text Input for Landmarks
st.markdown('<p class="input-text">📝 Enter a Landmark Name:</p>', unsafe_allow_html=True)
landmark_query = st.text_input("Enter a landmark", "")

# File Upload
st.markdown('<p class="upload-label">📤 Upload an Image:</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

def encode_image(image):
    return base64.b64encode(image.read()).decode("utf-8")

# Process Image Upload
landmark_name = None
if uploaded_file:
    image_data = encode_image(uploaded_file)
    
    # Call Google Vision API
    vision_payload = {
        "requests": [
            {
                "image": {"content": image_data},
                "features": [{"type": "LANDMARK_DETECTION"}]
            }
        ]
    }

    response = requests.post(VISION_URL, json=vision_payload)
    vision_result = response.json()

    try:
        landmark_name = vision_result["responses"][0]["landmarkAnnotations"][0]["description"]
        st.success(f"🏛️ Detected Landmark: {landmark_name}")
    except (KeyError, IndexError):
        st.warning("⚠️ No landmark detected! Trying alternative search...")

# Use text input if no landmark detected from image
if not landmark_name and landmark_query:
    landmark_name = landmark_query

if landmark_name:
    # Call Gemini API for detailed information
    gemini_payload = {
        "contents": [{"parts": [{"text": f"Provide a detailed description of {landmark_name}, including its history, significance, and interesting facts."}]}]
    }

    response = requests.post(GEMINI_URL, json=gemini_payload)
    gemini_result = response.json()

    try:
        description = gemini_result["candidates"][0]["content"]["parts"][0]["text"]
    






