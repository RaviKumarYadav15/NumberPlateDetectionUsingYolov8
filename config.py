import re

# Pattern: XX00XX0000 (Indian License Plate Format)
PLATE_PATTERN = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$")

# Common OCR mistake corrections
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
    'L': '1'
}

# Colors for annotation
VALID_BOX_COLOR = (0, 255, 0)
INVALID_BOX_COLOR = (0, 0, 255)
LABEL_BACKGROUND_COLOR = (0, 0, 0)
LABEL_TEXT_COLOR = (255, 255, 255)
