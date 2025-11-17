import os
from config import MAPPING_NUM_TO_ALPHA, MAPPING_ALPHA_TO_NUM

def save_uploaded_file(uploaded_file, folder="uploads"):
    """Saves the uploaded file to a specified folder and returns its path."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def format_plate_text(plate_text):
    """Formats a 10-character plate string into 'XX XX XX XXXX' for better readability."""
    if len(plate_text) == 10:
        return f"{plate_text[:2]} {plate_text[2:4]} {plate_text[4:6]} {plate_text[6:]}"
    return plate_text

def correct_plate_format(ocr_text):
    """
    Corrects common OCR errors for a 10-character string to match the plate format.
    """
    if len(ocr_text) != 10:
        return ""
    corrected_chars = list(ocr_text)
    # Positions 0, 1, 4, 5 must be letters
    for i in [0, 1, 4, 5]:
        char = corrected_chars[i]
        if char.isdigit() and char in MAPPING_NUM_TO_ALPHA:
            corrected_chars[i] = MAPPING_NUM_TO_ALPHA[char]
        else:
            corrected_chars[i] = char.upper()

    # Positions 2, 3, 6, 7, 8, 9 must be numbers
    for i in [2, 3, 6, 7, 8, 9]:
        char = corrected_chars[i].upper()
        if char.isalpha() and char in MAPPING_ALPHA_TO_NUM:
            corrected_chars[i] = MAPPING_ALPHA_TO_NUM[char]
            
    return "".join(corrected_chars)
