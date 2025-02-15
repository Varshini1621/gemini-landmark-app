import streamlit as st
import time
import requests
import json
import base64

# 🎨 UI Customization
st.set_page_config(page_title="Landmark Lens", page_icon="📍", layout="wide")

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "splash"

# 🎬 Splash Screen with Magenta Location Logo & "Landmark Lens"
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
            animation: zoomOut 5s ease-in-out;
            width: 150px;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: black;
            margin-top: 20px;
            animation: zoomOut 5s ease-in-out;
        }
        </style>
        <div class='splash-container'>
            <!-- Magenta Google Maps-like Location Pin -->
            <svg class="logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="150" height="150">
                <path fill="magenta" d="M12 2C7.03 2 4 5.03 4 8c0 3.31 3 6.24 7 9.94C11.39 19.1 12 21 12 21s.61-1.9 1-3.06C17 14.24 20 11.31 20 8c0-2.97-3.03-6-8-6z"/>
            </svg>
            <div class="title">Landmark Lens</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    time.sleep(5)
    st.session_state.page = "login"
    st.rerun()

# 🔑 Login/Register Page with Lavender Background Box
elif st.session_state.page == "login":
    st.markdown(
        """
        <style>
        body {
            background-color: lavender;
        }
        .page-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: lavender;
        }
        .login-title {
            font-size: 3rem;
            font-weight: bold;
            color: black;
            margin-bottom: 20px;
        }
        .login-box {
            background-color: #E6E6FA; /* Slightly darker lavender */
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            width: 350px;
            text-align: center;
        }
        .login-input {
            width: 90%;
            padding: 12px;
            margin: 10px 0;
            border-radius: 8px;
            border: 1px solid #ddd;
            font-size: 18px;
            background-color: white;
        }
        .login-button {
            background-color: magenta;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            width: 100%;
            cursor: pointer;
            margin-top: 10px;
        }
        .login-button:hover {
            background-color: darkmagenta;
        }
        </style>
        <div class='page-container'>
            <div class='login-title'>Landmark Lens</div>
            <div class='login-box'>
        """,
        unsafe_allow_html=True,
    )

    username = st.text_input("👤 Username:", key="username")
    password = st.text_input("🔑 Password:", type="password", key="password")
    
    col1, col2 = st.columns([1, 1])
    
    if col1.button("Login", key="login_button"):
        if username and password:
            st.session_state.page = "main"
            st.rerun()
        else:
            st.error("❌ Please enter username and password!")
    
    if col2.button("Register", key="register_button"):
        st.session_state.page = "register"
        st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)  # Close login-box and page-container

# 🌍 Main Landmark Lens App
elif st.session_state.page == "main":
    st.markdown("<h1 style='text-align: center;'>🌍✨ Landmark Lens 🏛️🔍</h1>", unsafe_allow_html=True)
    
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
            info = get_landmark_info(landmark_name)
            st.markdown(f"### 📖 Information about {landmark_name}")
            st.write(info)
        else:
            st.error("❌ Please enter a landmark name or upload an image.")

    st.markdown("<h3 style='text-align: center;'>🙏 Thank You for Exploring Us! 🌟</h3>", unsafe_allow_html=True)






























