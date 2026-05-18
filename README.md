# Optica: Your Image Processing Toolkit

Optica is a comprehensive, interactive image processing application built with Python and Streamlit to explore, analyze, and apply various fundamental and advanced image processing techniques in real-time.

---

## 🌟 Features

This application implements a vast array of image processing operations categorized into seven core modules:

### 1. Point Operations
- **Addition:** Add a constant value to image intensities.
- **Subtraction:** Subtract a constant value from image intensities.
- **Division:** Divide image intensities by a constant value.
- **Complement:** Compute the negative (inverse) of the image.

### 2. Color Image Operations
- **Adjust Lighting:** Increase or decrease the intensity on specific RGB channels independently.
- **Swap Channels:** Swap any two color channels (e.g., Red to Green).
- **Eliminate Channel:** Completely isolate or remove the Red, Green, or Blue channel.

### 3. Image Histogram
- **Histogram Stretching:** Enhance contrast by stretching the range of intensity values.
- **Histogram Equalization:** Improve image contrast using cumulative distribution functions.
- *Includes real-time, interactive histogram plotting mapped to the original and processed image.*

### 4. Neighborhood Processing
- **Linear Filters:** Average (Blur) filter, Laplacian filter (Edge enhancement).
- **Non-Linear Filters:** Maximum filter, Minimum filter, Median filter, and Mode filter.

### 5. Image Restoration and Noise Removal
- **Salt & Pepper Noise:** Inject noise and restore the image using Average, Median, or Outlier filters.
- **Gaussian Noise:** Inject statistical Gaussian noise and restore it using Average filtering or Image Averaging (combining multiple noisy frames).
- *Displays a specialized 3-column comparative view: `Original | Noisy | Restored`.*

### 6. Image Segmentation
- **Global Thresholding:** Manual binary thresholding using a user-defined slider.
- **Otsu's Thresholding:** Automatic threshold calculation algorithm.
- **Adaptive Thresholding:** Localized thresholding calculated dynamically based on neighborhood blocks.

### 7. Edge Detection and Morphology
- **Sobel Edge Detection:** Highlight structural boundaries using X and Y gradients.
- **Morphological Operations:** Dilation, Erosion, Opening.
- **Boundary Extraction:** Internal and External boundaries.
- **Morphological Gradient:** Difference between Dilation and Erosion.

---
## Usage & Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/Mazzenmohamedd/Optica.git
   cd Optica
   ```
   
2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **To launch the Optica workspace, run this command in your terminal**:
   ```bash
   streamlit run app.py
   ```
