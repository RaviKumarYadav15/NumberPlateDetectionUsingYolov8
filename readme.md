# License Plate Recognition System 🚗

A comprehensive Automated Number Plate Recognition (ANPR) system that combines YOLOv11 for license plate detection and EasyOCR for text extraction. This system can process images, videos, and live webcam feeds to accurately detect and read license plates in real-time.

![License Plate Recognition](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)
![YOLO](https://img.shields.io/badge/YOLO-v11-orange.svg)

## 🌟 Features

- **🎯 High Accuracy Detection**: Custom-trained YOLOv11 model for precise license plate detection
- **📄 Multi-format Support**: Process images (JPG, JPEG, PNG, WEBP), videos, and live webcam feeds
- **⚡ Real-time Processing**: Live detection through webcam with adjustable performance settings
- **🔧 Smart OCR Correction**: Automatic correction of common OCR misreadings using intelligent pattern matching
- **📊 Confidence Scoring**: Visual confidence percentages for each detected license plate
- **🔄 Batch Processing**: Efficiently process multiple images in bulk operations
- **🎨 User-friendly Interface**: Clean, intuitive Streamlit web interface with real-time preview

## 🚀 Live Demo

Try the system online with Google Colab:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1LQEOARGJrsXjzyxdBp48xbIu3DlUuR2S?usp=sharing)

## 📁 Project Structure
license-plate-recognition/
│
├── app.py # Streamlit UI for image & webcam ANPR detection
├── vision.py # YOLOv11 detection + EasyOCR recognition pipeline
├── utils.py # Helper functions (cleanup, normalization, correction)
├── config.py # Constants, regex patterns, colors
├── batch_process.py # Bulk folder-based processing
│
├── bestV11.pt # Custom-trained YOLOv11 model
├── oldBest.pt # Previous older model version
│
├── requirements.txt # Python dependencies
├── README.md # Documentation
│
├── test_images/ # Example test images
├── uploads/ # Temporary uploaded files (Streamlit)
├── output/ # Batch processing output & logs
│
└── venv/ # Virtual environment (ignored in Git)


## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.8** or higher
- **pip** (Python package manager)
- **Git** (for cloning repository)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd license-plate-recognition

2. Create Virtual Environment (Recommended)
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Verify Installation
python -c "import streamlit, cv2, easyocr, ultralytics; print('All dependencies installed successfully!')"


Required Dependencies

Package	Version	Purpose
streamlit	≥1.28.0	Web application framework
ultralytics	≥8.0.0	YOLO object detection
opencv-python	≥4.5.0	Computer vision operations
numpy	≥1.21.0	Numerical computations
easyocr	≥1.6.0	Optical Character Recognition


🎯 Usage Guide
Running the Application
Start the Streamlit Application
streamlit run app.py

Access the Web Interface
Open your web browser and navigate to: http://localhost:8501

Using Different Modes
📷 Image Processing Mode
Click "Choose an image" to upload your image
Click "Process Image" to analyze the image
View results with bounding boxes and confidence scores

🎥 Webcam/Video Mode
Enable "Enable Webcam / Video Mode" in sidebar
Check "Start Webcam Detection" to begin live processing
Adjust "Max Frame Width" slider for performance optimization

📁 Batch Processing Mode
python batch_process.py --input test_images/ --output output/


🔧 Configuration
License Plate Format
The system is optimized for Indian license plate format: XX00XX0000

Position	Type	Example
1-2	Alphabets	KA
3-4	Numbers	01
5-6	Alphabets	AB
7-10	Numbers	1234
Intelligent OCR Correction
Number to Letter Corrections:

0 → O (Zero to Capital O)
1 → I (One to Capital I)
5 → S (Five to Capital S)
8 → B (Eight to Capital B)

Letter to Number Corrections:
O → 0 (Capital O to Zero)
I → 1 (Capital I to One)
S → 5 (Capital S to Five)
B → 8 (Capital B to Eight)

📊 Model Specifications
Component	Technology	Purpose
Detection Model	YOLOv11 (Custom-trained)	License plate localization
OCR Engine	EasyOCR + English model	Text extraction from plates
Validation	Regex pattern matching	Format verification
Confidence	Adjustable threshold	Result reliability scoring

🐛 Troubleshooting Guide
Common Issues & Solutions
Model Loading Errors

text
Error: Ensure 'bestV11.pt' exists in project root
Solution: Download model file or check file path

Webcam Access Issues
Error: Unable to read from webcam/video
Solution: Check camera permissions and try different camera index

Performance Optimization
Issue: Slow processing on low-end systems
Solution: Reduce frame width in webcam settings

Dependency Conflicts
Error: Module not found or version conflict
Solution: Recreate virtual environment and reinstall dependencies
Performance Tips
For CPU systems: Set max frame width to 640px

For better accuracy: Use high-resolution images (1080p+)

For batch processing: Process during low system usage periods

🤝 Contributing
We welcome contributions! Here's how you can help:
Report Bugs: Open an issue with detailed description
Suggest Features: Share your ideas for improvements
Code Contributions: Submit pull requests for new features or bug fixes
Documentation: Help improve documentation and examples

Development Setup
# Fork and clone the repository
git clone <your-fork-url>
cd license-plate-recognition

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
# Submit pull request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
YOLO Team - For the excellent object detection framework
EasyOCR Developers - For robust text recognition capabilities
Streamlit Team - For the intuitive web application framework
OpenCV Community - For comprehensive computer vision tools

📞 Support
For questions, issues, or support:
Check the troubleshooting section above
Review existing GitHub issues
Create a new issue with detailed description
Provide system specifications and error logs

Note: This system is optimized for Indian license plates. For other countries, modify the pattern in config.py and consider retraining the detection model for optimal performance.

Happy Coding! 🚀
