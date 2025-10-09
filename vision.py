import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import easyocr

# Import from our custom modules
from config import PLATE_PATTERN, VALID_BOX_COLOR, INVALID_BOX_COLOR, LABEL_BACKGROUND_COLOR, LABEL_TEXT_COLOR
from utils import correct_plate_format, format_plate_text


@st.cache_resource
def load_yolo_model(model_path="best.pt"):
    """Loads the YOLOv8 model from the specified path."""
    return YOLO(model_path)

@st.cache_resource
def load_ocr_reader(lang_list=['en']):
    """Loads the EasyOCR reader for the specified languages."""
    return easyocr.Reader(lang_list)

def recognize_plate(plate_crop, reader):
    """
    Performs OCR on a cropped plate image, corrects the text, and validates it.
    This function is protected by multiple checks to prevent crashes.
    """
    # 1. Fast check for completely empty images
    if plate_crop.size == 0:
        return "", "", 0.0

    # Enlarge image for better OCR accuracy on small plates
    plate_resized = cv2.resize(plate_crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # 2. Robust safety net for any unexpected OCR errors
    try:
        ocr_result = reader.readtext(plate_resized, detail=1, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    except Exception as e:
        # If any error occurs, return empty results to prevent a crash
        return "", "", 0.0

    if not ocr_result:
        return "", "", 0.0

    raw_text = "".join([res[1] for res in ocr_result]).upper().replace(" ", "")
    scores = [res[2] for res in ocr_result]
    avg_confidence = np.mean(scores) if scores else 0.0

    corrected_text = correct_plate_format(raw_text)

    # 3. Validate the corrected text against the plate pattern
    if PLATE_PATTERN.match(corrected_text):
        formatted_text = format_plate_text(corrected_text)
        return formatted_text, raw_text, avg_confidence
    else:
        # Return the raw text if it doesn't match the valid format
        return "", raw_text, avg_confidence

def process_image(image, model, reader):
    """Detects plates in an image, runs recognition, and draws the results."""
    valid_detections = []
    invalid_detections = []
    
    results = model(image)
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            plate_img = image[y1:y2, x1:x2]
            
            # Efficiently skip tiny, invalid detections before OCR
            if plate_img.shape[0] < 10 or plate_img.shape[1] < 10:
                continue
            
            final_text, raw_text, confidence = recognize_plate(plate_img, reader)
            
            if final_text or raw_text:
                if final_text:
                    # Valid plate found
                    valid_detections.append((final_text, confidence))
                    display_text = f"{final_text} ({confidence:.0%})"
                    box_color = VALID_BOX_COLOR
                else:
                    # Unconfirmed plate (doesn't match pattern)
                    invalid_detections.append((raw_text, confidence))
                    display_text = f"Unconfirmed: {raw_text} ({confidence:.0%})"
                    box_color = INVALID_BOX_COLOR
                
                # --- Draw Bounding Box and Label ---
                # Calculate adaptive font size and thickness
                box_width = x2 - x1
                font_scale = max(0.5, box_width / 280)
                thickness = max(1, int(font_scale * 2))

                # Draw the main bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)
                
                # Get text size to draw a filled background rectangle
                (w, h), _ = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                label_y1 = max(y1 - h - 10, 0)
                
                # Draw the black background for the text
                cv2.rectangle(image, (x1, label_y1), (x1 + w + 10, y1), LABEL_BACKGROUND_COLOR, cv2.FILLED)
                
                # Put the text on the image
                cv2.putText(image, display_text, (x1 + 5, y1 - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, LABEL_TEXT_COLOR, thickness)

    return image, valid_detections, invalid_detections