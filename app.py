import streamlit as st
import requests
import json
import base64
import time

# 🎨 UI Customization
st.set_page_config(page_title="Landmark Lens", page_icon="📸", layout="wide")

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "splash"

# 🎬 Splash Screen
if st.session_state.page == "splash":
    st.markdown(
        """
        <style>
        @keyframes zoomOut {
            from { transform: scale(1); opacity: 1; }
            to { transform: scale(1.5); opacity: 0; }
        }
        .splash-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: lavender;
        }
        .logo {
            animation: zoomOut 4s ease-in-out;
            width: 120px;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: black;
            margin-top: 20px;
            animation: zoomOut 4s ease-in-out;
        }
        </style>
        <div class='splash-container'>
            <!-- Magenta Google Maps-like Location Pin -->
            <svg class="logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="120" height="120">
                <path fill="magenta" d="M12 2C7.03 2 4 5.03 4 8c0 3.31 3 6.24 7 9.94C11.39 19.1 12 21 12 21s.61-1.9 1-3.06C17 14.24 20 11.31 20 8c0-2.97-3.03-6-8-6z"/>
            </svg>
            <div class="title">Landmark Lens</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    time.sleep(4)
    st.session_state.page = "main"
    st.rerun()

# 🌍 Main Landmark Lens App
elif st.session_state.page == "main":
    # Inject Custom CSS for Background & Styling
    st.markdown(
        """
        <style>
            [data-testid="stAppViewContainer"] {
                background-color: lavender !important;
            }

            .title {
                text-align: center;
                font-size: 50px;
                font-weight: bold;
                color: black;
                font-family: 'Playfair Display', serif !important;
                margin-bottom: 20px;
            }

            div[data-baseweb="input"] > div {
                background-color: #F5F5DC !important; /* Beige */
                color: black !important;
                font-size: 18px !important;
                font-weight: bold !important;
                border: 2px solid #A52A2A !important; /* Brown */
                padding: 10px !important;
                border-radius: 8px !important;
            }

            .stButton > button {
                background-color: #4682B4 !important; /* Steel Blue */
                color: white !important;
                font-size: 18px !important;
                font-weight: bold !important;
                border-radius: 10px !important;
                padding: 12px 24px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 🌍 Title
    st.markdown('<div class="title">🌍✨ Landmark Lens 🏛️🔍</div>', unsafe_allow_html=True)

    # 📍 User Inputs
    st.write("🔎 **Enter a landmark/place name** OR 📷 **Upload an image** to get details!")
    landmark_name = st.text_input("📌 Enter a Landmark Name:")
    uploaded_image = st.file_uploader("📸 Upload an Image of a Landmark:", type=["jpg", "jpeg", "png"])

    # 🔑 API KEYS (Replace with actual keys)
    VISION_API_KEY = "AIzaSyDmMQ6qprPCRLR-Ck6d2mCqXDk-ALD3X20"
    GEMINI_API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"
    SEARCH_API_KEY = "AIzaSyAej50xK52tETJA489DhpQv89S7gsKZDmA"
    CX_ID = "e403168ae528340d0"

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
            return result["responses"][0]["landmarkAnnotations"][0]["description"]
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
        search_url = "https://www.googleapis.com/customsearch/v1"
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
    st.markdown("<h3 style='text-align: center;'>🙏 Thank You for Exploring Us! 🌟</h3>", unsafe_allow_html=True)
































