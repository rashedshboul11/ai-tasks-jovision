import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from openpyxl import Workbook


def detect_fingers_from_binary(binary_image):
    """Detect which fingers are holding the object from the extracted right-half binary image."""
    # Convert PIL image to NumPy array
    if not isinstance(binary_image, np.ndarray):
        binary_image = np.array(binary_image)

    height, width = binary_image.shape  # Now this works!

    # Divide into 5 equal vertical regions (one per finger)
    region_width = width // 5

    fingers = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    finger_status = {}

    for i, finger in enumerate(fingers):
        # Extract the region corresponding to each finger
        finger_region = binary_image[:, i * region_width: (i + 1) * region_width]

        # Count white pixels (pressure points)
        white_pixel_count = np.sum(finger_region == 255)

        # Determine if the finger is pressing
        threshold = 700
        finger_status[finger] = 1 if white_pixel_count > threshold else 0

    return finger_status

def apply_otsu_thresholding(pil_image):
    """
    Apply Otsu's thresholding method to a PIL Image object.

    Parameters:
    pil_image (PIL.Image): Grayscale PIL Image object

    Returns:
    tuple: (binary PIL Image after thresholding, threshold value used)
    """
    # Ensure the image is grayscale
    if pil_image.mode != 'L':
        pil_image = pil_image.convert('L')

    # Convert PIL Image to numpy array for OpenCV processing
    img_array = np.array(pil_image)

    # Apply Otsu's thresholding
    ret, binary_mask = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert numpy array back to PIL Image
    binary_image = Image.fromarray(binary_mask)

    return binary_image, ret


def detect_pressure(img):
    #return true if there is pressure in any of the fingers
    #img = get_sensor_data('./task3-images/000121.jpg')
    width, height = img.size

    return img.getpixel((width-1, height-1))[1] > 200


def get_sensor_data(img_path):
    # returns an image of sensor data
    img = Image.open(img_path)
    width, height = img.size
    sensor_data = Image.new("RGB", (width//2, height))

    for x in range(width//2, width):
        for y in range(height):
            sensor_data.putpixel((x - width//2,y), img.getpixel((x,y)))
    sensor_data.convert('L')
    return sensor_data




def main():
    directory = './task3-images'
    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Thumb", "Index", "Middle", "Ring", "Pinky"])
    for img_name in os.listdir(directory):
        if not img_name.lower().endswith('jpg'):  # Skip non-image files
            continue
        file_path = os.path.join(directory, img_name)
        img = get_sensor_data(file_path)
        if detect_pressure(img):
            binary_img, thre = apply_otsu_thresholding(img.convert('L'))
            finger_stat = detect_fingers_from_binary(binary_img)
            ws.append([img_name, finger_stat['Thumb'], finger_stat['Index'], finger_stat['Middle'],
                        finger_stat['Ring'], finger_stat['Pinky']])
            print(img.size,file_path,finger_stat)
    wb.save('results.xlsx')

if __name__ == '__main__':
    main()

