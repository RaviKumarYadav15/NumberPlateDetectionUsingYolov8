# 🚗 License Plate Recognition System (YOLO + EasyOCR)

A complete, production-ready **Automatic Number Plate Recognition (ANPR)** system that detects license plates using **YOLO** and reads them with **EasyOCR**.  
Supports **images, videos, webcam**, and includes **OCR correction**, **confidence scoring**, **batch processing**, and a **Streamlit UI**.


---

## ⭐ Overview

This project includes:

- Custom-trained YOLO (Roboflow → Google Colab → Ultralytics → best.pt)
- Real-time detection + OCR
- Smart character correction for Indian license plates
- Streamlit-based frontend
- Batch processing support

---

## 🌟 Features

### 🔍 Detection & Reading
- YOLO-based number plate detection  
- EasyOCR for text extraction  
- Regex-based format validation (Indian Standard: **XX00XX0000**)  
- Automatic OCR correction (0↔O, 1↔I, 5↔S, 8↔B)

### 💻 Input Modes
- Image upload  
- Webcam (real-time)
- Video input  
- Batch folder processing

### 📊 Extras
- Detection confidence %  
- OCR confidence %  
- Adjustable thresholds  
- Clean UI with real-time updates  

---

## 🚀 Quick Demo (Optional)

Add your Colab link here when available:




## 📁 Project Structure

license-plate-recognition/
│
├── app.py                # Streamlit UI for image & webcam ANPR detection
├── vision.py             # YOLOv11 detection + EasyOCR recognition pipeline
├── utils.py              # Helper functions (cleanup, normalization, correction)
├── config.py             # Constants, regex patterns, colors
├── batch_process.py      # Bulk folder-based processing
│
├── bestV11.pt            # Custom-trained YOLOv11 model
├── oldBest.pt            # Previous older model version
│
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
│
├── test_images/          # Example test images
├── uploads/              # Temporary uploaded files (Streamlit)
├── output/               # Batch processing output & logs
│
└── venv/                 # Virtual environment (ignored in Git)

---

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.8+
- `pip`
- `git`

---

1️⃣ Clone this repository**

git clone <your-repository-url>
cd license-plate-recognition


2️⃣ Create a Virtual Environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate


3️⃣ Install Dependencies
pip install -r requirements.txt


4️⃣ Validate Installation
python -c "import streamlit, cv2, easyocr, ultralytics; print('Setup OK!')"


🎯 Usage
Run Streamlit App
streamlit run app.py


Now open in browser:
http://localhost:8501



📸 Image Mode
-->Upload an image
-->Click Process Image
View:

-->Detection bounding boxes

-->OCR text

-->Confidence values

-->Corrected plate format

🎥 Webcam / Video Mode

-->Enable webcam mode in sidebar

-->Adjust frame size for speed

-->Click Start Detection

🗂️ Batch Processing
python batch_process.py --input test_images/ --output output/


-->All results (annotated images + text) will be stored in the output folder.


🔧 Configuration
Edit config.py for custom settings.

Indian License Plate Format
XX00XX0000

-->First 2: Letters
-->Next 2: Numbers
-->Next 2: Letters
-->Next 4: Numbers

OCR Auto-Corrections
Misread	Correct
0 → O	O → 0
1 → I	I → 1
5 → S	S → 5
8 → B	B → 8


📊 Model Details

Detection Model: YOLOv11 (trained on Roboflow)
OCR Engine: EasyOCR
Trained on Indian number plate datasets
Exported as bestV11.pt

🧪 Training Process Summary
Dataset created and annotated on Roboflow.

Training on Google Colab:

from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(data="data.yaml", epochs=50, imgsz=640)


Download trained weights:
from google.colab import files
files.download('/content/runs/train/exp/weights/best.pt')


Rename to:
bestV11.pt


Place in project root.

🐛 Troubleshooting
-->Model Not Loading

-->Confirm bestV11.pt exists in project root

-->Ensure correct filename in config.py

-->Webcam Not Working

-->Check system permissions

-->Try switching camera index:

cv2.VideoCapture(1)

-->Slow Performance

-->Lower webcam frame width

## Use YOLO nano models (yolov8n, yolov11n)

### Run on GPU if possible

🤝 Contributing

Pull requests are welcome.

To contribute:
git checkout -b feature-name
# Make changes
git commit -m "Add awesome feature"
git push

📄 License

This project is licensed under the MIT License.
🙏 Acknowledgments

Ultralytics YOLO
EasyOCR
Roboflow
Streamlit

❤️ Support

If you like this project, give it a ⭐ on GitHub!
