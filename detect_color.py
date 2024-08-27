import cv2
import numpy as np


image_path = r'/home/amirali/Desktop/amirali/n1.jpg'  # Paste your path here

def get_color_at_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
        image = param
        color = image[y, x]
        print(f"Clicked at ({x}, {y}), Color (BGR): {color}")


image = cv2.imread(image_path)

if image is None:
    raise ValueError(f"Could not open or find the image: {image_path}")


cv2.namedWindow('Image')
cv2.setMouseCallback('Image', get_color_at_click, param=image)


cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#
