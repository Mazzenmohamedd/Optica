import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io

# Import custom modules
from image_processing import point_operations as po
from image_processing import color_operations as co
from image_processing import histogram_operations as ho
from image_processing import neighborhood_operations as no
from image_processing import restoration_operations as ro
from image_processing import segmentation_operations as so
from image_processing import edge_morphology_operations as emo

# first Streamlit command
st.set_page_config(page_title="Optica | Image Processing", layout="wide", initial_sidebar_state="expanded")

def inject_custom_css():
    st.markdown("""
    <style>
        /* Base Application Background */
        .stApp {
            background: linear-gradient(135deg, #0a1628 0%, #0d2137 100%) !important;
            color: #ffffff !important;
        }
        
        /* Sidebar Glassmorphism */
        [data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            color: #00c9a7 !important;
            font-weight: 600 !important;
        }
        
        p, span, label {
            color: rgba(255, 255, 255, 0.85) !important;
        }
        
        /* Glass Panels for inputs & widgets */
        div[data-baseweb="select"] > div, 
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: white !important;
        }
        
        /* Selectbox dropdown items */
        div[data-baseweb="popover"] > div {
            background-color: #0a1628 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
        }
        div[data-baseweb="popover"] li {
            color: white !important;
        }
        div[data-baseweb="popover"] li:hover {
            background-color: rgba(0, 201, 167, 0.2) !important;
        }
        
        /* Buttons Glassmorphism & Hover */
        .stButton>button, .stDownloadButton>button {
            background-color: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(0, 201, 167, 0.5) !important;
            border-radius: 12px !important;
            color: white !important;
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover, .stDownloadButton>button:hover {
            border-color: #00c9a7 !important;
            box-shadow: 0 0 15px rgba(0, 201, 167, 0.6) !important;
            color: #00c9a7 !important;
            background-color: rgba(0, 201, 167, 0.1) !important;
        }
        
        /* File Uploader styling */
        [data-testid="stFileUploadDropzone"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 2px dashed rgba(0, 201, 167, 0.4) !important;
            border-radius: 20px !important;
            padding: 3rem !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stFileUploadDropzone"]:hover {
            border-color: #00c9a7 !important;
            background-color: rgba(0, 201, 167, 0.05) !important;
            box-shadow: 0 0 20px rgba(0, 201, 167, 0.2) !important;
        }
        
        /* Images rounded corners */
        img {
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Custom hr */
        hr {
            border-color: rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Slider Color */
        .stSlider [data-testid="stTickBar"] > div {
            background-color: rgba(255,255,255,0.2) !important;
        }
        
    </style>
    """, unsafe_allow_html=True)

def plot_histogram(image, title):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_alpha(0.0) 
    ax.patch.set_alpha(0.0)  
    
    if len(image.shape) == 3:
        colors = ('r', 'g', 'b')
        for i, color in enumerate(colors):
            hist, _ = np.histogram(image[:, :, i], bins=256, range=(0, 256))
            ax.plot(hist, color=color, alpha=0.8)
    else:
        hist, _ = np.histogram(image, bins=256, range=(0, 256))
        ax.plot(hist, color='#00c9a7', alpha=0.8)
        
    ax.set_title(title, color='white', pad=15)
    ax.set_xlim([0, 256])
    ax.grid(True, alpha=0.1)
    
    for spine in ax.spines.values():
        spine.set_color((1.0, 1.0, 1.0, 0.2))
        
    ax.tick_params(colors=(1.0, 1.0, 1.0, 0.7))
    return fig

def main():
    inject_custom_css()
    
    if 'uploaded_image' not in st.session_state:
        st.session_state['uploaded_image'] = None

    if st.session_state['uploaded_image'] is None:
        st.markdown("<div style='margin-top: 6rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 4rem;'>Optica</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-bottom: 3rem;'>Explore. Process. Analyze.</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png", "webp", "bmp"])
            if uploaded_file is not None:
                st.session_state['uploaded_image'] = uploaded_file.getvalue()
                st.rerun()
                
    else:
        # Main App View
        st.markdown("<h1>Optica</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.1em; margin-bottom: 2rem;'>Explore. Process. Analyze.</p>", unsafe_allow_html=True)
        
        if st.sidebar.button("Upload New Image"):
            st.session_state['uploaded_image'] = None
            st.rerun()
            
        st.sidebar.markdown("### Control Panel")
        
        # Read image from session state
        image = Image.open(io.BytesIO(st.session_state['uploaded_image']))
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image_np = np.array(image)
        
        # Category Selection
        category = st.sidebar.selectbox(
            "Select Category",
            [
                "Point Operations",
                "Color Operations",
                "Image Histogram",
                "Neighborhood Processing",
                "Image Restoration",
                "Image Segmentation",
                "Edge Detection & Morphology"
            ]
        )
        
        st.sidebar.markdown("---")
        
        processed_image = None
        noisy_image = None
        
        # ---------------------------------------------------------
        # 1. Point Operations
        # ---------------------------------------------------------
        if category == "Point Operations":
            st.sidebar.markdown("#### Point Operations")
            operation = st.sidebar.selectbox("Operation", ["Addition", "Subtraction", "Division", "Complement"])
            
            if operation in ["Addition", "Subtraction"]:
                value = st.sidebar.slider("Intensity Value", 0, 255, 50)
                if operation == "Addition":
                    processed_image = po.add_value(image_np, value)
                else:
                    processed_image = po.subtract_value(image_np, value)
                    
            elif operation == "Division":
                value = st.sidebar.slider("Divisor Value", 1, 10, 2)
                processed_image = po.divide_value(image_np, value)
                
            elif operation == "Complement":
                processed_image = po.complement_image(image_np)
                
        # ---------------------------------------------------------
        # 2. Color Operations
        # ---------------------------------------------------------
        elif category == "Color Operations":
            st.sidebar.markdown("#### Color Operations")
            operation = st.sidebar.selectbox("Operation", ["Adjust Lighting", "Swap Channels", "Eliminate Channel"])
            
            if operation == "Adjust Lighting":
                channel = st.sidebar.selectbox("Target Channel", ["Red (R)", "Green (G)", "Blue (B)"])
                ch_key = channel[0] 
                value = st.sidebar.slider("Lighting Value", -255, 255, 50)
                processed_image = co.adjust_lighting(image_np, value, channel=ch_key)
                
            elif operation == "Swap Channels":
                ch1 = st.sidebar.selectbox("Channel 1", ["Red (R)", "Green (G)", "Blue (B)"], index=0)
                ch2 = st.sidebar.selectbox("Channel 2", ["Red (R)", "Green (G)", "Blue (B)"], index=1)
                processed_image = co.swap_channels(image_np, ch1=ch1[0], ch2=ch2[0])
                
            elif operation == "Eliminate Channel":
                channel = st.sidebar.selectbox("Channel to Remove", ["Red (R)", "Green (G)", "Blue (B)"])
                processed_image = co.remove_channel(image_np, channel=channel[0])
                
        # ---------------------------------------------------------
        # 3. Image Histogram
        # ---------------------------------------------------------
        elif category == "Image Histogram":
            st.sidebar.markdown("#### Histogram Processing")
            operation = st.sidebar.selectbox("Operation", ["Histogram Stretching", "Histogram Equalization"])
            
            if operation == "Histogram Stretching":
                processed_image = ho.histogram_stretching(image_np)
            elif operation == "Histogram Equalization":
                processed_image = ho.histogram_equalization(image_np)
                
        # ---------------------------------------------------------
        # 4. Neighborhood Processing
        # ---------------------------------------------------------
        elif category == "Neighborhood Processing":
            st.sidebar.markdown("#### Spatial Filters")
            filter_type = st.sidebar.selectbox("Filter Class", ["Linear Filters", "Non-Linear Filters"])
            
            if filter_type == "Linear Filters":
                operation = st.sidebar.selectbox("Operation", ["Average Filter", "Laplacian Filter"])
            else:
                operation = st.sidebar.selectbox("Operation", ["Maximum Filter", "Minimum Filter", "Median Filter", "Mode Filter"])
            
            if operation != "Laplacian Filter":
                kernel_size = st.sidebar.slider("Kernel Size", 3, 11, 3, step=2)
                
            if operation == "Average Filter":
                processed_image = no.average_filter(image_np, kernel_size)
            elif operation == "Laplacian Filter":
                processed_image = no.laplacian_filter(image_np)
            elif operation == "Maximum Filter":
                processed_image = no.max_filter(image_np, kernel_size)
            elif operation == "Minimum Filter":
                processed_image = no.min_filter(image_np, kernel_size)
            elif operation == "Median Filter":
                processed_image = no.median_filter(image_np, kernel_size)
            elif operation == "Mode Filter":
                st.sidebar.warning("Warning: Mode filter may take a few seconds on high-res images.")
                processed_image = no.mode_filter(image_np, kernel_size)
                
        # ---------------------------------------------------------
        # 5. Image Restoration
        # ---------------------------------------------------------
        elif category == "Image Restoration":
            st.sidebar.markdown("#### Noise & Restoration")
            noise_type = st.sidebar.selectbox("Noise Type", ["Salt & Pepper Noise", "Gaussian Noise"])
            
            if noise_type == "Salt & Pepper Noise":
                prob = st.sidebar.slider("Noise Probability", 0.01, 0.2, 0.05)
                noisy_image = ro.add_salt_and_pepper_noise(image_np, prob)
                
                removal_method = st.sidebar.selectbox("Removal Filter", ["Average Filter", "Median Filter", "Outlier Method"])
                if removal_method == "Average Filter":
                    k_size = st.sidebar.slider("Kernel Size", 3, 7, 3, step=2)
                    processed_image = ro.remove_sp_average(noisy_image, k_size)
                elif removal_method == "Median Filter":
                    k_size = st.sidebar.slider("Kernel Size", 3, 7, 3, step=2)
                    processed_image = ro.remove_sp_median(noisy_image, k_size)
                elif removal_method == "Outlier Method":
                    threshold = st.sidebar.slider("Threshold Factor", 0.0, 1.0, 0.2)
                    processed_image = ro.remove_sp_outlier(noisy_image, threshold)
                    
            elif noise_type == "Gaussian Noise":
                var = st.sidebar.slider("Noise Variance", 0.01, 0.1, 0.01)
                noisy_image = ro.add_gaussian_noise(image_np, 0, var)
                
                removal_method = st.sidebar.selectbox("Removal Method", ["Image Averaging", "Average Filter"])
                if removal_method == "Image Averaging":
                    num_images = st.sidebar.slider("Images to Average", 2, 30, 10)
                    processed_image = ro.remove_gaussian_averaging(image_np, 0, var, num_images)
                elif removal_method == "Average Filter":
                    k_size = st.sidebar.slider("Kernel Size", 3, 7, 3, step=2)
                    processed_image = ro.remove_gaussian_average_filter(noisy_image, k_size)
                    
        # ---------------------------------------------------------
        # 6. Image Segmentation
        # ---------------------------------------------------------
        elif category == "Image Segmentation":
            st.sidebar.markdown("#### Segmentation")
            operation = st.sidebar.selectbox("Thresholding Method", ["Global Thresholding", "Otsu (Automatic)", "Adaptive Thresholding"])
            
            if operation == "Global Thresholding":
                thresh_val = st.sidebar.slider("Threshold Value", 0, 255, 127)
                processed_image = so.global_thresholding(image_np, thresh_val)
            elif operation == "Otsu (Automatic)":
                processed_image = so.otsu_thresholding(image_np)
            elif operation == "Adaptive Thresholding":
                block_size = st.sidebar.slider("Block Size", 3, 21, 11, step=2)
                c_val = st.sidebar.slider("C Value", 0, 10, 2)
                processed_image = so.adaptive_thresholding(image_np, block_size, c_val)
                
        # ---------------------------------------------------------
        # 7. Edge Detection & Morphology
        # ---------------------------------------------------------
        elif category == "Edge Detection & Morphology":
            st.sidebar.markdown("#### Edge & Morphology")
            operation = st.sidebar.selectbox("Operation", [
                "Sobel Edge Detection", 
                "Morphological Dilation", 
                "Morphological Erosion", 
                "Morphological Opening",
                "Boundary Extraction (Internal)",
                "Boundary Extraction (External)",
                "Morphological Gradient"
            ])
            
            if operation != "Sobel Edge Detection":
                kernel_size = st.sidebar.slider("Kernel Size", 3, 11, 3, step=2)
                
            if operation == "Sobel Edge Detection":
                processed_image = emo.sobel_edge_detection(image_np)
            elif operation == "Morphological Dilation":
                processed_image = emo.dilate_image(image_np, kernel_size)
            elif operation == "Morphological Erosion":
                processed_image = emo.erode_image(image_np, kernel_size)
            elif operation == "Morphological Opening":
                processed_image = emo.open_image(image_np, kernel_size)
            elif operation == "Boundary Extraction (Internal)":
                processed_image = emo.boundary_extraction_internal(image_np, kernel_size)
            elif operation == "Boundary Extraction (External)":
                processed_image = emo.boundary_extraction_external(image_np, kernel_size)
            elif operation == "Morphological Gradient":
                processed_image = emo.morphological_gradient(image_np, kernel_size)
        
        # ---------------------------------------------------------
        # DISPLAY SECTION
        # ---------------------------------------------------------
        st.markdown("### Results View")
        
        # Handle 3-column layout for restoration, 2-column for others
        if category == "Image Restoration" and noisy_image is not None:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(image_np, use_container_width=True)
                st.markdown("<p style='text-align: center; color: #00c9a7; font-weight: bold;'>Original</p>", unsafe_allow_html=True)
            with col2:
                st.image(noisy_image, use_container_width=True)
                st.markdown("<p style='text-align: center; color: #f43f5e; font-weight: bold;'>Noisy</p>", unsafe_allow_html=True)
            with col3:
                if processed_image is not None:
                    st.image(processed_image, use_container_width=True)
                    st.markdown("<p style='text-align: center; color: #3b82f6; font-weight: bold;'>Restored</p>", unsafe_allow_html=True)
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.image(image_np, use_container_width=True)
                st.markdown("<p style='text-align: center; color: #00c9a7; font-weight: bold;'>Original Image</p>", unsafe_allow_html=True)
                
                # Plot Histogram for original if needed
                if category == "Image Histogram":
                    st.pyplot(plot_histogram(image_np, "Original Histogram"))
                    
            with col2:
                if processed_image is not None:
                    st.image(processed_image, use_container_width=True)
                    st.markdown("<p style='text-align: center; color: #3b82f6; font-weight: bold;'>Processed Image</p>", unsafe_allow_html=True)
                    
                    # Plot Histogram for processed if needed
                    if category == "Image Histogram":
                        st.pyplot(plot_histogram(processed_image, "Processed Histogram"))
                else:
                    st.info("Select an operation and parameters to view the result.")

if __name__ == "__main__":
    main()
