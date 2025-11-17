import streamlit as st
import cv2
import os
import tempfile
import numpy as np

from vision import load_yolo_model, load_ocr_reader, process_image
from utils import save_uploaded_file

# --------------------------------------
# Page Config & Model Loading
# --------------------------------------
st.set_page_config(page_title="License Plate Recognition", layout="wide")
st.title("License Plate Detection & Recognition 🚗")

try:
    model = load_yolo_model()
    reader = load_ocr_reader()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# --------------------------------------
# Session State
# --------------------------------------
for key in ["img_path", "processed_image", "valid_detections", "invalid_detections"]:
    if key not in st.session_state:
        st.session_state[key] = None if key == "img_path" else []

# --------------------------------------
# Image Upload Mode
# --------------------------------------
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
            with st.spinner("Processing image..."):
                image = cv2.imread(st.session_state.img_path)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                processed, valid, invalid = process_image(image_rgb, model, reader)

                st.session_state.processed_image = processed
                st.session_state.valid_detections = valid
                st.session_state.invalid_detections = invalid

    with col2:
        st.subheader("Processed Image & Results")
        if st.session_state.processed_image is not None:
            st.image(st.session_state.processed_image, use_container_width=True)

            if st.session_state.valid_detections:
                st.success("Validated License Plate(s):")
                for text, conf in st.session_state.valid_detections:
                    st.write(f"### **{text}** (Confidence: {conf:.0%})")

            if st.session_state.invalid_detections:
                st.warning("Unconfirmed Reading(s):")
                for text, conf in st.session_state.invalid_detections:
                    st.write(f"- `{text}` (Confidence: {conf:.0%})")

            if not st.session_state.valid_detections and not st.session_state.invalid_detections:
                st.info("No license plates detected.")
        else:
            st.info("Click 'Process Image' to continue.")

# --------------------------------------
# Webcam / Video Mode
# --------------------------------------
st.sidebar.header("🎥 Video / Webcam Settings")
use_webcam = st.sidebar.checkbox("Enable Webcam / Video Mode")

if use_webcam:
    st.warning("Webcam detection may be slower depending on your system.")
    run_webcam = st.checkbox("Start Webcam Detection")

    if run_webcam:
        frame_window = st.image([])
        cap = cv2.VideoCapture(0)

        max_width = st.sidebar.slider("Max Frame Width", 320, 1280, 640, step=64)

        while run_webcam:
            ret, frame = cap.read()
            if not ret:
                st.error("Unable to read from webcam.")
                break

            h, w = frame.shape[:2]
            if w > max_width:
                scale = max_width / w
                frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_frame, valid, invalid = process_image(rgb, model, reader)

            frame_window.image(processed_frame, channels="RGB", use_container_width=True)

        cap.release()
