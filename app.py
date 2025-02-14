import streamlit as st
import requests
import base64
import json

# 🔑 Google Cloud Vision API Key
VISION_API_KEY = "AIzaSyDmMQ6qprPCRLR-Ck6d2mCqXDk-ALD3X20"
VISION_URL = f"https://vision.googleapis.com/v1/images:annotate?key={VISION_API_KEY}"

# 🔑 Google Gemini API Key
GEMINI_API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

# 🎨 Streamlit UI Design
st.markdown(
    """
    <style>
        body { background-color: #FFDAB9; } /* Peach Background */
        .title { text-align: center; font-size: 40px; color: black; font-weight: bold; }
        .input-text, .upload-label { color: black; font-size: 20px; font-weight: bold; }
        .emoji { font-size: 30px; text-align: center; }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown('<p class="title">📸 Landmark Lens 🌍</p>', unsafe_allow_html=True)

# 📝 Text Input for Landmarks
st.markdown('<p class="input-text">📝 Enter a Landmark Name:</p>', unsafe_allow_html=True)
landmark_query = st.text_input("Enter a landmark", "")

# 📤 File Upload
st.markdown('<p class="upload-label">📤 Upload an Image:</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

def encode_image(image):
    """Encodes image to Base64 for API requests."""
    return base64.b64encode(image.read()).decode("utf-8")

landmark_name = None
image_desc = None

if uploaded_file:
    image_data = encode_image(uploaded_file)

    # 🔍 Google Vision API Request
    vision_payload = {
        "requests": [
            {
                "image": {"content": image_data},
                "features": [
                    {"type": "LANDMARK_DETECTION"},
                    {"type": "LABEL_DETECTION"},
                    {"type": "WEB_DETECTION"}  # Web Entities as backup
                ]
            }
        ]
    }

    try:
        vision_response = requests.post(VISION_URL, json=vision_payload)
        vision_result = vision_response.json()

        # ✅ First Try: Landmark Detection
        if "responses" in vision_result and "landmarkAnnotations" in vision_result["responses"][0]:
            landmark_name = vision_result["responses"][0]["landmarkAnnotations"][0]["description"]
            st.success(f"🏛️ Detected Landmark: {landmark_name}")

        # 🔄 Second Try: Web Detection (Backup)
        elif "webDetection" in vision_result["responses"][0]:
            web_entities = vision_result["responses"][0]["webDetection"].get("webEntities", [])
            if web_entities:
                landmark_name = web_entities[0]["description"]
                st.info(f"🌍 Suggested Landmark: {landmark_name}")

        # ❌ No Landmark Found
        else:
            st.warning("⚠️ No landmark detected! Trying AI-based analysis...")

    except Exception as e:
        st.error(f"🚨 Error with Vision API: {e}")

# 📸 Gemini AI Fallback for Image Analysis
if not landmark_name and uploaded_file:
    gemini_payload = {
        "contents": [{"parts": [{"inline_data": {"mime_type": "image/jpeg", "data": image_data}}]}]
    }

    try:
        response = requests.post(GEMINI_URL, json=gemini_payload)
        gemini_result = response.json()

        if "candidates" in gemini_result:
            image_desc = gemini_result["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown("### 🔍 AI Image Analysis Result:")
            st.write(image_desc)
        else:
            st.error("🚨 Gemini AI could not analyze the image.")

    except Exception as e:
        st.error(f"🚨 Gemini API Error: {e}")

# 🏛️ Fetch Landmark Information
final_query = landmark_name if landmark_name else landmark_query

if final_query:
    gemini_payload = {
        "contents": [{"parts": [{"text": f"Give a detailed history and information about {final_query}."}]}]
    }

    try:
        response = requests.post(GEMINI_URL, json=gemini_payload)
        gemini_result = response.json()

        if "candidates" in gemini_result:
            description = gemini_result["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown(f"### 🏰 About {final_query}:")
            st.write(description)
        else:
            st.error("🚨 Could not retrieve landmark details.")

    except Exception as e:
        st.error(f"🚨 Error fetching landmark information: {e}")

# 🎉 End Note
st.markdown('<p class="emoji">😊🌍✨</p>', unsafe_allow_html=True)
st.markdown("### Thank You for Using **Landmark Lens**! 🎉")








