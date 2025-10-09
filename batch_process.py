import os
import cv2
import csv
import glob
from tqdm import tqdm 

# Import your existing functions from your other project files
from vision import load_yolo_model, load_ocr_reader, process_image
# --- Configuration ---
INPUT_FOLDER = "test_images"
OUTPUT_FOLDER = "output"
RESULTS_CSV_PATH = os.path.join(OUTPUT_FOLDER, "results.csv")

def run_batch_processing():
    """
    Main function to run the batch processing workflow.
    It finds all images in the input folder, processes them, saves the annotated
    images to the output folder, and logs all findings to a CSV file.
    """
    # 1. Load models once
    print("Loading models, this might take a moment...")
    model = load_yolo_model()
    reader = load_ocr_reader()
    print("Models loaded successfully.")

    # 2. Ensure output directory exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # 3. Find all image files in the input folder (case-insensitive extensions)
    image_paths = glob.glob(os.path.join(INPUT_FOLDER, '*.[jJ][pP][gG]')) + \
                  glob.glob(os.path.join(INPUT_FOLDER, '*.[pP][nN][gG]')) + \
                  glob.glob(os.path.join(INPUT_FOLDER, '*.[jJ][pP][eE][gG]')) + \
                  glob.glob(os.path.join(INPUT_FOLDER, '*.[wW][eE][bB][pP]'))

    if not image_paths:
        print(f"Error: No images found in the '{INPUT_FOLDER}' directory.")
        return

    print(f"Found {len(image_paths)} images to process.")

    # 4. Open the CSV file to store the detailed results
    with open(RESULTS_CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the descriptive header row
        csv_writer.writerow(['Filename', 'Detected_Text', 'Status', 'Confidence'])

        # 5. Loop through each image with a progress bar
        for img_path in tqdm(image_paths, desc="Processing Images"):
            filename = os.path.basename(img_path)
            
            # Read the image using OpenCV
            image = cv2.imread(img_path)
            if image is None:
                tqdm.write(f"Warning: Could not read image {filename}. Skipping.")
                continue

            # Convert from BGR (OpenCV) to RGB for the processing function
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image using the function from vision.py
            processed_image_rgb, valid_detections, invalid_detections = process_image(image_rgb.copy(), model, reader)
            
            # --- Save the visual output ---
            output_path = os.path.join(OUTPUT_FOLDER, filename)
            # Convert back from RGB to BGR for saving with OpenCV
            processed_image_bgr = cv2.cvtColor(processed_image_rgb, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, processed_image_bgr)

            # --- Log the text output ---
            detections_found = False
            if valid_detections:
                detections_found = True
                for text, confidence in valid_detections:
                    csv_writer.writerow([filename, text, 'VALIDATED', f"{confidence:.2f}"])
            
            if invalid_detections:
                detections_found = True
                for text, confidence in invalid_detections:
                    csv_writer.writerow([filename, text, 'UNCONFIRMED', f"{confidence:.2f}"])
            
            if not detections_found:
                # Log if no plates were detected at all in the image
                csv_writer.writerow([filename, 'N/A', 'NO_PLATE_DETECTED', '0.00'])

    print(f"\n✅ Batch processing complete!")
    print(f"Processed images have been saved in the '{OUTPUT_FOLDER}' directory.")
    print(f"A detailed log has been saved to '{RESULTS_CSV_PATH}'")

if __name__ == "__main__":
    run_batch_processing()