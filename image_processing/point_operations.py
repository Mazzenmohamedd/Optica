import numpy as np

def add_value(image, value):
    #Add constant value to the image
    return np.clip(image.astype(np.int16) + value, 0, 255).astype(np.uint8)

def subtract_value(image, value):
    #Subtract constant value from the image
    return np.clip(image.astype(np.int16) - value, 0, 255).astype(np.uint8)

def divide_value(image, value):
    #Divide image by a constant value
    if value == 0:
        return image.copy()
    return np.clip(image.astype(np.float32) / value, 0, 255).astype(np.uint8)

def complement_image(image):
    #Compute complement (negative)
    return 255 - image
