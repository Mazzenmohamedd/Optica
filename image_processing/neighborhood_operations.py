import cv2
import numpy as np
from scipy import ndimage

def average_filter(image, kernel_size=3):
    #Apply average filter
    return cv2.blur(image, (kernel_size, kernel_size))

def laplacian_filter(image):
    #Apply Laplacian filter 
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    # Convert back to uint8
    abs_laplacian = cv2.convertScaleAbs(laplacian)
    return abs_laplacian

def max_filter(image, kernel_size=3):
    #Apply maximum filter
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

def min_filter(image, kernel_size=3):
    #Apply minimum filter
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

def median_filter(image, kernel_size=3):
    #Apply median filter       
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.medianBlur(image, kernel_size)

def mode_filter(image, kernel_size=3):
    #Apply mode filter
    def mode_func(x):
        values, counts = np.unique(x, return_counts=True)
        return values[np.argmax(counts)]
    
    if len(image.shape) == 3:
        result = np.zeros_like(image)
        for i in range(3):
            result[:, :, i] = ndimage.generic_filter(image[:, :, i], mode_func, size=kernel_size)
        return result
    else:
        return ndimage.generic_filter(image, mode_func, size=kernel_size)
