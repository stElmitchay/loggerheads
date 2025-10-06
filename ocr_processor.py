"""
OCR processor for extracting text from screenshots.
Uses pytesseract to perform optical character recognition on captured images.
"""

import pytesseract
from PIL import Image
import os


def extract_text_from_image(image_path):
    """
    Extract text from an image file using OCR.

    Args:
        image_path (str): Path to the image file

    Returns:
        str: Extracted text from the image, or empty string if extraction fails
    """
    try:
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return ""

        # Open the image
        image = Image.open(image_path)

        # Perform OCR
        text = pytesseract.image_to_string(image)

        return text.strip()

    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""


def process_screenshot_batch(screenshot_dir):
    """
    Process all screenshots in a directory and extract text from each.

    Args:
        screenshot_dir (str): Directory containing screenshot files

    Returns:
        dict: Dictionary mapping image filenames to extracted text
    """
    results = {}

    if not os.path.exists(screenshot_dir):
        print(f"Screenshot directory not found: {screenshot_dir}")
        return results

    # Get all image files (png, jpg, jpeg)
    image_extensions = ('.png', '.jpg', '.jpeg')
    image_files = [f for f in os.listdir(screenshot_dir)
                   if f.lower().endswith(image_extensions)]

    for image_file in image_files:
        image_path = os.path.join(screenshot_dir, image_file)
        text = extract_text_from_image(image_path)
        results[image_file] = text
        print(f"Processed {image_file}: {len(text)} characters extracted")

    return results
