import streamlit as st
import cv2

# Import from our custom modules
from utils import save_uploaded_file
from vision import load_yolo_model, load_ocr_reader, process_image

# --- Page Configuration ---
st.set_page_config(page_title="License Plate Recognition", layout="wide")
st.title("License Plate Detection & Recognition 🚗")
st.info("Upload an image, then click 'Process Image' to detect license plates.")

# --- Model Loading ---
# Load models once and cache them
model = load_yolo_model()
reader = load_ocr_reader()

# --- Session State Initialization ---
# Initialize session state variables to avoid errors
if 'img_path' not in st.session_state:
    st.session_state.img_path = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'valid_detections' not in st.session_state:
    st.session_state.valid_detections = None
if 'invalid_detections' not in st.session_state:
    st.session_state.invalid_detections = None

# --- File Uploader and Main Logic ---
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

# If a new file is uploaded, save it and reset previous results
if uploaded_file:
    st.session_state.img_path = save_uploaded_file(uploaded_file)
    # Reset previous processing results when a new image is uploaded
    st.session_state.processed_image = None
    st.session_state.valid_detections = None
    st.session_state.invalid_detections = None

# Only display the content if an image has been uploaded
if st.session_state.img_path:
    # --- Display Layout ---
    col1, col2 = st.columns(2)
    
    # Display the original image and the process button in the first column
    with col1:
        st.image(st.session_state.img_path, caption="Uploaded Image", width=400)
        
        # The button that triggers the processing
        if st.button("Process Image", type="primary"):
            with st.spinner('⚙️ Processing image... Please wait.'):
                image = cv2.imread(st.session_state.img_path)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Run processing and store results in session state
                processed_image_rgb, valid_detections, invalid_detections = process_image(image_rgb.copy(), model, reader)
                
                st.session_state.processed_image = processed_image_rgb
                st.session_state.valid_detections = valid_detections
                st.session_state.invalid_detections = invalid_detections

    # Display the results in the second column ONLY after processing is done
    if st.session_state.processed_image is not None:
        with col2:
            st.image(st.session_state.processed_image, caption="Processed Image", width=400)
        
        # Display the text results below the images
        if st.session_state.valid_detections:
            st.success("✅ Validated License Plate(s) Found:")
            for text, confidence in st.session_state.valid_detections:
                st.write(f"### **{text}** (Confidence: {confidence:.0%})")
        
        if st.session_state.invalid_detections:
            st.warning("⚠️ Unconfirmed Reading(s):")
            st.write("The following were detected but could not be validated after correction.")
            for text, confidence in st.session_state.invalid_detections:
                st.write(f"- `{text}` (Confidence: {confidence:.0%})")

        if not st.session_state.valid_detections and not st.session_state.invalid_detections:
            st.info("No license plates were detected in the image.")