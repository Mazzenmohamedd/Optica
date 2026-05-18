import numpy as np
import cv2

def add_images(image1, image2, alpha):
    if image1.shape != image2.shape:
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
    blended = alpha * image1.astype(np.float32) + (1.0 - alpha) * image2.astype(np.float32)
    return np.clip(blended, 0, 255).astype(np.uint8)

def subtract_value(image, value):
    #Subtract constant value from the image
    return np.clip(image.astype(np.int16) - value, 0, 255).astype(np.uint8)

def divide_value(image, value):
    #Divide image by a constant value
    if value == 0:
        return image.copy()
    return np.clip(image.astype(np.float32) / value, 0, 255).astype(np.uint8)

def complement_image(image):
    #complement (negative)
    return 255 - image
