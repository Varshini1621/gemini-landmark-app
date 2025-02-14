import streamlit as st
import requests
import json

# Set Page Config
st.set_page_config(page_title="Landmark Explorer 🌍", page_icon="🏛️", layout="wide")

# Custom CSS for Dark Theme, White Inputs, and Stylish UI
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #121212;
        }
        .stMarkdown h1 {
            color: #FFD700 !important; /* Gold Color */
            font-size: 3rem;
            text-align: center;
        }
        .stMarkdown h2 {
            color: #FFA500 !important; /* Orange Color */
            font-size: 2rem;
        }
        .stMarkdown p {
            color: #E0E0E0;
            font-size: 1.2rem;
        }
        .icon {
            font-size: 60px;
            text-align: center;
            padding: 20px;
        }
        .css-1d391kg {  /* Sidebar */
            background-color: #222 !important;
        }
        .stTextInput>div>div>input, .stFileUploader>div {
            color: white !important; 
            font-size: 1.2rem;
            background-color: #1E1E1E !important;
            border: 2px solid #FF5733;
            padding: 10px;
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #FF5733;
            color: white;
            font-size: 1.5rem;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #FF4500;
        }
    </style>
""", unsafe_allow_html=True)

# Title with Emoji
st.markdown("<h1>🌍 Discover Amazing Landmarks! 🏛️✨</h1>", unsafe_allow_html=True)

# Large Icons & Instructions
st.markdown('<p class="icon">📷 Upload a Landmark Photo OR 🔍 Enter a Landmark Name</p>', unsafe_allow_html=True)

# Input Section
landmark_name = st.text_input("🏛️ **Enter a Landmark Name:**", placeholder="Eiffel Tower, Taj Mahal...")
uploaded_image = st.file_uploader("📷 **Upload a Landmark Image:**", type=["jpg", "png", "jpeg"])

# API Keys (Replace with your actual API keys)
API_KEY = "your_google_gemini_api_key"
VISION_API_KEY = "your_google_vision_api_key"

# Process Image or Text Input
if st.button("🔍 Search"):
    if uploaded_image:
        st.image(uploaded_image, caption="📸 Uploaded Image", use_column_width=True)

        # Vision API Call
        vision_url = f"https://vision.googleapis.com/v1/images:annotate?key={VISION_API_KEY}"
        image_bytes = uploaded_image.read()
        vision_payload = {
            "requests": [
                {
                    "image": {"content": image_bytes.decode('latin-1')},
                    "features": [{"type": "LANDMARK_DETECTION"}],
                }
            ]
        }

        response = requests.post(vision_url, json=vision_payload)
        result = response.json()

        try:
            landmark_detected = result["responses"][0]["landmarkAnnotations"][0]["description"]
            st.success(f"🌍 **Detected Landmark: {landmark_detected}** ✅")
            landmark_name = landmark_detected  # Use detected landmark name
        except (KeyError, IndexError):
            st.error("❌ No landmark detected! Please try another image.")

    if landmark_name:
        # Gemini API Call
        gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
        gemini_payload = {"contents": [{"parts": [{"text": landmark_name}]}]}
        response = requests.post(gemini_url, json=gemini_payload)
        data = response.json()

        try:
            description = data["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown(f"## 🏛️ About **{landmark_name}** ✨")
            st.write(description)
        except KeyError:
            st.error("❌ Unable to fetch landmark information!")

# Thank You Message
st.markdown("<h2>💖 Thank You for Exploring with Us! 🚀🌍</h2>", unsafe_allow_html=True)





