import re
# Define the required license plate pattern: XX00XX0000
PLATE_PATTERN = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$")

# Mappings for correcting common OCR errors based on visual similarity
MAPPING_NUM_TO_ALPHA = {
    '0': 'O', 
    '1': 'I', 
    '5': 'S', 
    '8': 'B', 
    '6': 'G', 
    '7': 'T'
}
MAPPING_ALPHA_TO_NUM = {
    'O': '0', 
    'I': '1', 
    'S': '5', 
    'B': '8', 
    'G': '6', 
    'T': '7', 
    'Z': '2', 
    'D': '0', 
    'L': '1'
}
# Define colors for drawing bounding boxes and labels
VALID_BOX_COLOR = (0, 255, 0)      # Green for valid plates
INVALID_BOX_COLOR = (0, 0, 255)    # Red for unconfirmed plates
LABEL_BACKGROUND_COLOR = (0, 0, 0) # Black
LABEL_TEXT_COLOR = (255, 255, 255) # White
# This file will hold all your static variables, patterns, and settings.