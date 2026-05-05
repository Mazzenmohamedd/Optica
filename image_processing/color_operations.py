import numpy as np

def adjust_lighting(image, value, channel='R'):
    """Adjusts lighting by increasing or decreasing a specific channel (R, G, B)."""
    if len(image.shape) != 3 or image.shape[2] != 3:
        return image # Not a color RGB image
    
    result = image.copy()
    ch_idx = {'R': 0, 'G': 1, 'B': 2}.get(channel, 0)
    
    result[:, :, ch_idx] = np.clip(result[:, :, ch_idx].astype(np.int16) + value, 0, 255).astype(np.uint8)
    return result

def swap_channels(image, ch1='R', ch2='G'):
    """Swaps two color channels."""
    if len(image.shape) != 3 or image.shape[2] != 3:
        return image
        
    result = image.copy()
    idx1 = {'R': 0, 'G': 1, 'B': 2}.get(ch1, 0)
    idx2 = {'R': 0, 'G': 1, 'B': 2}.get(ch2, 1)
    
    temp = result[:, :, idx1].copy()
    result[:, :, idx1] = result[:, :, idx2]
    result[:, :, idx2] = temp
    return result

def remove_channel(image, channel='R'):
    """Removes a specific color channel by setting it to 0."""
    if len(image.shape) != 3 or image.shape[2] != 3:
        return image
        
    result = image.copy()
    ch_idx = {'R': 0, 'G': 1, 'B': 2}.get(channel, 0)
    result[:, :, ch_idx] = 0
    return result
