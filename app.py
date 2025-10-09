import streamlit as st
import cv2
import os
import tempfile
import numpy as np

# Import your custom functions from other files
from vision import load_yolo_model, load_ocr_reader, process_image

def save_uploaded_file(uploaded_file):
    """Saves the uploaded file to a temporary directory and returns the path."""
    try:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

# --- Page Configuration and Model Loading ---
st.set_page_config(page_title="License Plate Recognition", layout="wide")
st.title("License Plate Detection & Recognition 🚗")
st.info("Upload an image, then click 'Process Image' to detect license plates.")

try:
    model = load_yolo_model()
    reader = load_ocr_reader()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# --- Session State Initialization ---
if 'img_path' not in st.session_state:
    st.session_state.img_path = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'valid_detections' not in st.session_state:
    st.session_state.valid_detections = []
if 'invalid_detections' not in st.session_state:
    st.session_state.invalid_detections = []

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    st.session_state.img_path = save_uploaded_file(uploaded_file)
    st.session_state.processed_image = None
    st.session_state.valid_detections = []
    st.session_state.invalid_detections = []

# --- Main Application Logic ---
if st.session_state.img_path:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")
        st.image(st.session_state.img_path, use_column_width=True)

        if st.button("Process Image", type="primary", use_container_width=True):
            with st.spinner('⚙️ Processing image... Please wait.'):
                image = cv2.imread(st.session_state.img_path)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                processed_rgb, valid, invalid = process_image(image_rgb.copy(), model, reader)

                st.session_state.processed_image = processed_rgb
                st.session_state.valid_detections = valid
                st.session_state.invalid_detections = invalid

    with col2:
        st.subheader("Processed Image & Results")
        if st.session_state.processed_image is not None:
            st.image(st.session_state.processed_image, use_column_width=True)

            if st.session_state.valid_detections:
                st.success("✅ Validated License Plate(s) Found:")
                for text, conf in st.session_state.valid_detections:
                    st.write(f"### **{text}** (Confidence: {conf:.0%})")

            if st.session_state.invalid_detections:
                st.warning("⚠️ Unconfirmed Reading(s):")
                st.write("The following were detected but could not be validated.")
                for text, conf in st.session_state.invalid_detections:
                    st.write(f"- `{text}` (Confidence: {conf:.0%})")

            if not st.session_state.valid_detections and not st.session_state.invalid_detections:
                st.info("No license plates were detected in the image.")
        else:
            st.info("Click 'Process Image' to see the results.")
