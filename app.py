import streamlit as st
import requests
import json
import base64

# 🎨 UI Customization - Full Page Background & Font Style
st.set_page_config(page_title="Landmark Lens", page_icon="📸", layout="wide")

st.markdown(
    """
    <style>
        /* Full Page Background */
        body {
            background-color: #F5E3C4; /* Oasis Color */
        }

        /* Landmark Lens Title */
        .title {
            font-family: 'Courier New', monospace;
            font-size: 48px;
            text-align: center;
            font-weight: bold;
            color: #2F4F4F; /* Dark Slate Gray */
        }

        /* Input Fields */
        .stTextInput, .stFileUploader {
            color: black; 
            font-size: 20px; 
            font-weight: bold; 
            background-color: #F5F5DC; /* Beige */
        }

        /* Search Button */
        .stButton>button {
            background-color: #FF4500; 
            color: white; 
            font-size: 18px; 
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🔑 API KEYS (Replace with actual keys)
VISION_API_KEY = "AIzaSyDmMQ6qprPCRLR-Ck6d2mCqXDk-ALD3X20"
GEMINI_API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"
SEARCH_API_KEY = "AIzaSyAej50xK52tETJA489DhpQv89S7gsKZDmA"
CX_ID = "e403168ae528340d0"

# 🌍 Title with Stylish Font
st.markdown("<h1 class='title'>🌍 Landmark Lens 🏛️</h1>", unsafe_allow_html=True)
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

# 🖼️ Function to Get Images using Google Custom Search API (Fixed)
def get_landmark_image(place_name):
    search_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": place_name,
        "cx": CX_ID,
        "searchType": "image",
        "num": 1,
        "key": SEARCH_API_KEY
    }

    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        if "items" in result and len(result["items"]) > 0:
            return result["items"][0]["link"]
        else:
            return None
    else:
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
st.markdown("<h3 style='text-align: center; color: black;'>🙏 Thank you for exploring Landmark Lens! 🏛️</h3>", unsafe_allow_html=True)

















