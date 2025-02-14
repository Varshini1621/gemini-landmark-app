import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# 🎨 UI Customization
st.set_page_config(page_title="Landmark Lens", page_icon="📸", layout="wide")
st.markdown(
    """
    <style>
        body { background-color: #FFDAB9; }
        .stTextInput, .stFileUploader { color: black; font-size: 20px; font-weight: bold; }
        .stButton>button { background-color: #FF4500; color: white; font-size: 18px; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🔑 API KEYS (Replace with your actual keys)
VISION_API_KEY = "AIzaSyDmMQ6qprPCRLR-Ck6d2mCqXDk-ALD3X20"
GEMINI_API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"
SEARCH_API_KEY = "AIzaSyAej50xK52tETJA489DhpQv89S7gsKZDmA"
CX_ID = "e403168ae528340d0"

# 🌍 Title & Emoji
st.markdown("<h1 style='text-align: center; color: black;'>🌍 Landmark Lens 🏛️</h1>", unsafe_allow_html=True)
st.write("🔎 **Enter a landmark/place name** OR 📷 **Upload an image** to get details!")

# 📍 User Inputs
landmark_name = st.text_input("📌 Enter a Landmark Name:", "")
uploaded_image = st.file_uploader("📸 Upload an Image of a Landmark:", type=["jpg", "jpeg", "png"])

# 🔍 Function to Detect Landmark in Image
def detect_landmark(image_bytes):
    vision_url = f"https://vision.googleapis.com/v1/images:annotate?key={VISION_API_KEY}"
    img_base64 = base64.b64encode(image_bytes).decode()
    
    request_data = {
        "requests": [{
            "image": {"content": img_base64},
            "features": [{"type": "LANDMARK_DETECTION"}]
        }]
    }

    response = requests.post(vision_url, json=request_data)
    result = response.json()
    
    try:
        landmark_name = result["responses"][0]["landmarkAnnotations"][0]["description"]
        return landmark_name
    except:
        return None

# 🏛️ Function to Get Landmark Info from Gemini API
def get_landmark_info(place_name):
    gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    request_data = {"contents": [{"parts": [{"text": f"Give a detailed description about {place_name}"}]}]}
    
    response = requests.post(gemini_url, json=request_data)
    result = response.json()
    
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "⚠️ No information found for this place."

# 🖼️ Function to Get Images using Google Custom Search API
def get_landmark_image(place_name):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={place_name}&cx={CX_ID}&searchType=image&key={SEARCH_API_KEY}"
    response = requests.get(search_url)
    result = response.json()
    
    try:
        image_url = result["items"][0]["link"]
        return image_url
    except:
        return None

# 🚀 Process Input
if st.button("🔍 Search"):
    if uploaded_image:
        image_bytes = uploaded_image.read()
        detected_landmark = detect_landmark(image_bytes)
        
        if detected_landmark:
            st.success(f"✅ Detected Landmark: {detected_landmark}")
            landmark_name = detected_landmark
        else:
            st.error("❌ No landmark detected! Try another image.")
    
    if landmark_name:
        # 🔹 Fetch Landmark Info
        info = get_landmark_info(landmark_name)
        st.markdown(f"### 📖 Information about {landmark_name}")
        st.write(info)
        
        # 🔹 Fetch Landmark Image
        landmark_image = get_landmark_image(landmark_name)
        if landmark_image:
            st.image(landmark_image, caption=f"📍 {landmark_name}", use_column_width=True)
        else:
            st.warning("⚠️ No images found for this place.")
    else:
        st.error("❌ Please enter a landmark name or upload an image.")

# 🎉 Thank You Message
st.markdown("<h3 style='text-align: center; color: black;'>🙏 Thank you for using Landmark Lens! 🏛️</h3>", unsafe_allow_html=True)








