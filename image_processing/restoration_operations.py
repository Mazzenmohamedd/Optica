import cv2
import numpy as np

def add_salt_and_pepper_noise(image, prob=0.05):
    #Add salt and pepper noise
    output = np.copy(image)
    
    # Salt mode
    num_salt = np.ceil(prob * image.size * 0.5)
    coords = [np.random.randint(0, i, int(num_salt)) for i in image.shape]
    output[tuple(coords)] = 255

    # Pepper mode
    num_pepper = np.ceil(prob * image.size * 0.5)
    coords = [np.random.randint(0, i, int(num_pepper)) for i in image.shape]
    output[tuple(coords)] = 0
    return output

def remove_sp_average(image, kernel_size=3):
    #Remove salt and pepper noise using average filter
    return cv2.blur(image, (kernel_size, kernel_size))

def remove_sp_median(image, kernel_size=3):
    #Remove salt and pepper noise using median filter
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.medianBlur(image, kernel_size)

def remove_sp_outlier(image, threshold=0.2):
    #Remove salt and pepper noise using outlier method
    mean_filtered = cv2.blur(image, (3, 3))        
    #Convert to int16 to avoid overflow
    diff = np.abs(image.astype(np.int16) - mean_filtered.astype(np.int16))    
    thresh_val = int(threshold * 255)
    mask = diff > thresh_val
    
    result = np.where(mask, mean_filtered, image)
    return result.astype(np.uint8)

def add_gaussian_noise(image, mean=0, var=0.01):
    #Add Gaussian noise
    row, col = image.shape[:2]
    ch = image.shape[2] if len(image.shape) == 3 else 1
    
    sigma = var ** 0.5
    if ch == 1 and len(image.shape) == 2:
        gauss = np.random.normal(mean, sigma, (row, col))
        gauss = gauss.reshape(row, col)
    else:
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        
    noisy = image.astype(np.float32) + gauss * 255
    return np.clip(noisy, 0, 255).astype(np.uint8)

def remove_gaussian_averaging(image, mean=0, var=0.01, num_images=10):
    #Remove Gaussian noise by averaging multiple noisy images
    avg_image = np.zeros_like(image, dtype=np.float32)
    for _ in range(num_images):
        noisy = add_gaussian_noise(image, mean, var)
        avg_image += noisy
        
    avg_image = avg_image / num_images
    return np.clip(avg_image, 0, 255).astype(np.uint8)

def remove_gaussian_average_filter(image, kernel_size=3):
    #Remove Gaussian noise using average filter
    return cv2.blur(image, (kernel_size, kernel_size))
