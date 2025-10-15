import streamlit as st
import cv2
import os
import tempfile
import numpy as np

# Import your custom functions from other files
from vision import load_yolo_model, load_ocr_reader, process_image
from utils import save_uploaded_file

# ====================================================
# --- Page Configuration and Model Loading ---
# ====================================================
st.set_page_config(page_title="License Plate Recognition", layout="wide")
st.title("License Plate Detection & Recognition 🚗")
st.info("Upload an image or use webcam/video mode to detect license plates.")

try:
    model = load_yolo_model()
    reader = load_ocr_reader()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# ====================================================
# --- Session State Initialization ---
# ====================================================
if 'img_path' not in st.session_state:
    st.session_state.img_path = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'valid_detections' not in st.session_state:
    st.session_state.valid_detections = []
if 'invalid_detections' not in st.session_state:
    st.session_state.invalid_detections = []

# ====================================================
# --- File Uploader (Image Mode) ---
# ====================================================
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    st.session_state.img_path = save_uploaded_file(uploaded_file)
    st.session_state.processed_image = None
    st.session_state.valid_detections = []
    st.session_state.invalid_detections = []

if st.session_state.img_path:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")
        st.image(st.session_state.img_path, use_container_width=True)

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
            st.image(st.session_state.processed_image, use_container_width=True)

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
# ====================================================
# --- Video / Webcam Support ---
# ====================================================
st.sidebar.header("🎥 Video / Webcam Settings")
use_webcam = st.sidebar.checkbox("Enable Webcam / Video Mode")

if use_webcam:
    st.warning("Webcam detection is experimental; may be slower than image mode.")
    run_webcam = st.checkbox("Start Webcam Detection")
    if run_webcam:
        frame_window = st.image([])  # Placeholder for frames
        cap = cv2.VideoCapture(0)  # 0 = default webcam, replace with file path for video

        # Optional: user-controlled frame resizing for speed
        max_width = st.sidebar.slider("Max Frame Width", 320, 1280, 640, step=64)

        while run_webcam:
            ret, frame = cap.read()
            if not ret:
                st.error("Unable to read from webcam/video.")
                break

            # Resize frame for faster processing
            height, width = frame.shape[:2]
            if width > max_width:
                scale = max_width / width
                frame = cv2.resize(frame, (int(width*scale), int(height*scale)))

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_frame, valid, invalid = process_image(frame_rgb, model, reader)
            
            # Display processed frame
            frame_window.image(processed_frame, channels="RGB", use_container_width=True)

        cap.release()