from PIL import Image
import pytesseract
import os

path = input("Enter the full path of the image: ").strip()

if not os.path.isfile(path):
    print("Error: The file does not exist. Please check the path.")
else:
    try:
        # Open image
        im = Image.open(path)

        # Perform OCR
        text = pytesseract.image_to_string(im)

        # Print extracted text
        print("\nExtracted Text:\n")
        print(text)

    except Exception as e:
        print(f"Error processing the image: {e}")
