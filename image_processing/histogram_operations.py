import cv2
import numpy as np

def histogram_stretching(image):
    #Applies histogram stretching 
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()
        
    min_val = np.min(gray)
    max_val = np.max(gray)
    
    if max_val == min_val:
        return gray
        
    #Stretching formula: (pixel - min) * 255 / (max - min)
    stretched = ((gray - min_val) * (255.0 / (max_val - min_val))).astype(np.uint8)
    return stretched

def histogram_equalization(image):
    #Applies histogram equalization 
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()
        
    equalized = cv2.equalizeHist(gray)
    return equalized
