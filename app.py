import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="Gemini Landmark Description App")

# UI: Title and Image Upload
st.title("Gemini Landmark Description App 🌍🏛️")
st.write("Upload an image of a landmark, and we'll describe it for you!")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
    st.write("Processing...")

    # API request to Google Gemini
    api_key = "YOUR_GEMINI_API_KEY"  # Replace with your actual API key
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent?key=" + api_key
    
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": {"text": "Describe the landmark in this image."},
        "image": {"data": uploaded_file.read()}  # Pass image data
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        st.write("**Landmark Description:**")
        st.write(result.get("text", "No description available."))
    else:
        st.error("Error fetching data. Please try again later.")

st.write("🔹 Powered by Google Gemini API")
