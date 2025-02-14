import streamlit as st
import requests
import json
from PIL import Image
import io

# Define API key
API_KEY = "AIzaSyDR6XAorj_e9h020_ULOXR3Gjko7TwHHUE"

# Define API URL for text-based landmark recognition
TEXT_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

# Define API URL for image-based recognition (replace with actual API if available)
IMAGE_URL = "your_image_recognition_api_here"

headers = {
    "Content-Type": "application/json"
}

# Title
st.title("🌍 Gemini Landmark Recognition App")

# Option selection
option = st.radio("Choose Input Method:", ["Enter Landmark Name", "Upload Photo"])

# ---- TEXT INPUT OPTION ----
if option == "Enter Landmark Name":
    query = st.text_input("Enter a landmark name (e.g., Taj Mahal, Great Wall of China, Machu Picchu):")
    
    if st.button("Get Landmark Info") and query:
        data = {
            "contents": [
                {"parts": [{"text": query}]}
            ]
        }
        
        try:
            response = requests.post(TEXT_URL, json=data, headers=headers)
            response_json = response.json()

            if "candidates" in response_json:
                generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(f"### 🏛️ Landmark Info for: **{query}**")
                st.write(generated_text)  # Display AI-generated landmark description
            else:
                st.error("No response received. Please try again.")

        except Exception as e:
            st.error(f"Error making API request: {e}")

# ---- IMAGE UPLOAD OPTION ----
elif option == "Upload Photo":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Analyze Image"):
            # Convert image to bytes
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="JPEG")
            img_data = img_bytes.getvalue()

            # API request payload (Modify based on API requirements)
            data = {
                "image": img_data  # Ensure this matches the expected API format
            }
            
            try:
                response = requests.post(IMAGE_URL, files={"file": img_data}, headers=headers)
                response_json = response.json()

                # Extract and display result
                if "description" in response_json:
                    st.markdown(f"### 📸 Landmark Detected: **{response_json['description']}**")
                else:
                    st.error("No landmark detected. Try another image.")

            except Exception as e:
                st.error(f"Error making API request: {e}")

