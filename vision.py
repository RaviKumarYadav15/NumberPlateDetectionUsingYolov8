import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import easyocr

from config import (
    PLATE_PATTERN, 
    VALID_BOX_COLOR, 
    INVALID_BOX_COLOR, 
    LABEL_BACKGROUND_COLOR, 
    LABEL_TEXT_COLOR
)
from utils import correct_plate_format, format_plate_text


@st.cache_resource
def load_yolo_model(model_path="bestV11.pt"):
    return YOLO(model_path)


@st.cache_resource
def load_ocr_reader(lang_list=['en']):
    return easyocr.Reader(lang_list)


def recognize_plate(plate_crop, reader):
    if plate_crop.size == 0:
        return "", "", 0.0

    plate_resized = cv2.resize(
        plate_crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC
    )

    try:
        ocr_result = reader.readtext(
            plate_resized,
            detail=1,
            allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )
    except:
        return "", "", 0.0

    if not ocr_result:
        return "", "", 0.0

    raw_text = "".join([res[1] for res in ocr_result]).upper().replace(" ", "")
    scores = [res[2] for res in ocr_result]
    avg_confidence = np.mean(scores) if scores else 0.0

    corrected_text = correct_plate_format(raw_text)

    if PLATE_PATTERN.match(corrected_text):
        formatted = format_plate_text(corrected_text)
        return formatted, raw_text, avg_confidence
    else:
        return "", raw_text, avg_confidence


def process_image(image, model, reader):
    valid_detections = []
    invalid_detections = []

    results = model(image)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            plate_img = image[y1:y2, x1:x2]

            if plate_img.shape[0] < 10 or plate_img.shape[1] < 10:
                continue

            final_text, raw_text, confidence = recognize_plate(plate_img, reader)

            if final_text or raw_text:
                if final_text:
                    valid_detections.append((final_text, confidence))
                    display_text = f"{final_text} ({confidence:.0%})"
                    color = VALID_BOX_COLOR
                else:
                    invalid_detections.append((raw_text, confidence))
                    display_text = f"Unconfirmed: {raw_text} ({confidence:.0%})"
                    color = INVALID_BOX_COLOR

                box_width = x2 - x1
                font_scale = max(0.5, box_width / 280)
                thickness = max(1, int(font_scale * 2))

                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

                (tw, th), _ = cv2.getTextSize(
                    display_text,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    thickness
                )
                label_y1 = max(y1 - th - 10, 0)

                cv2.rectangle(
                    image,
                    (x1, label_y1),
                    (x1 + tw + 10, y1),
                    LABEL_BACKGROUND_COLOR,
                    cv2.FILLED
                )

                cv2.putText(
                    image,
                    display_text,
                    (x1 + 5, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    LABEL_TEXT_COLOR,
                    thickness
                )

    return image, valid_detections, invalid_detections
