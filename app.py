# pip install streamlit opencv-python pillow numpy

import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.title("🖼️ Image Enhancer Tool")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    st.subheader("Original Image")
    st.image(img_array, use_column_width=True)

    # Convert to OpenCV format
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # -------------------------------
    # 1. Sharpening to "Unblur"
    kernel_sharpen = np.array([[0, -1, 0],
                               [-1, 5,-1],
                               [0, -1, 0]])
    sharpened = cv2.filter2D(img_cv, -1, kernel_sharpen)

    # -------------------------------
    # 2. Auto Brightness and Contrast
    def automatic_brightness_contrast(image, clip_hist_percent=1):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray],[0],None,[256],[0,256])
        hist_size = len(hist)

        accumulator = []
        accumulator.append(float(hist[0]))
        for index in range(1, hist_size):
            accumulator.append(accumulator[index -1] + float(hist[index]))

        maximum = accumulator[-1]
        clip_hist_percent *= (maximum/100.0)
        clip_hist_percent /= 2.0

        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1

        maximum_gray = hist_size -1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1

        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha

        auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return auto_result

    bright_contrast = automatic_brightness_contrast(sharpened)

    # -------------------------------
    # 3. Auto White Balance (Color Correction)
    result = cv2.cvtColor(bright_contrast, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(result)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    final_lab = cv2.merge((cl, a, b))
    final_bgr = cv2.cvtColor(final_lab, cv2.COLOR_LAB2BGR)
    final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

    # -------------------------------
    # Show enhanced image
    st.subheader("Enhanced Image ✨")
    st.image(final_rgb, use_column_width=True)

    # Download button
    result_image = Image.fromarray(final_rgb)
    st.download_button("Download Enhanced Image", data=result_image.tobytes(), file_name="enhanced.png", mime="image/png")
