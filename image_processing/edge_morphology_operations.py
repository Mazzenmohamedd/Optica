import cv2
import numpy as np

def sobel_edge_detection(image):
    #Applies edge detection
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()
        
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Combine the two
    magnitude = cv2.magnitude(sobelx, sobely)
    return cv2.convertScaleAbs(magnitude)

def dilate_image(image, kernel_size=3):
    #Applies morphological dilation
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

def erode_image(image, kernel_size=3):
    #Applies morphological erosion
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

def open_image(image, kernel_size=3):
    #Applies morphological opening 
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def boundary_extraction_internal(image, kernel_size=3):
    #Internal boundary
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    eroded = cv2.erode(image, kernel, iterations=1)
    return cv2.subtract(image, eroded)

def boundary_extraction_external(image, kernel_size=3):
    #External boundary
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated = cv2.dilate(image, kernel, iterations=1)
    return cv2.subtract(dilated, image)

def morphological_gradient(image, kernel_size=3):
    #Morphological gradient
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
