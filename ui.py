import streamlit as st
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim

st.set_page_config(page_title="Pixel Perfect Comparison", layout="wide")
st.title("🎯 Sharp Pixel Difference Highlighter")

def highlight_differences(img1, img2):
    # Resize second image to match first
    if img1.size != img2.size:
        st.warning(f"Resizing comparison image from {img2.size} to {img1.size}")
        img2 = img2.resize(img1.size)

    # Convert to grayscale for SSIM comparison
    gray1 = np.array(img1.convert("L"))
    gray2 = np.array(img2.convert("L"))

    # Calculate SSIM and diff map
    score, diff = ssim(gray1, gray2, full=True)
    diff = (1 - diff) > 0.02  # Boolean mask of different pixels (thresholded)

    # Convert original to array for manipulation
    base_array = np.array(img1.convert("RGB")).copy()

    # Mark differing pixels in RED
    base_array[diff] = [255, 0, 0]  # Red highlight

    highlighted_image = Image.fromarray(base_array)
    return score, highlighted_image

# Upload interface
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Upload Base Image", type=["png", "jpg", "jpeg"])
with col2:
    file2 = st.file_uploader("Upload Comparison Image", type=["png", "jpg", "jpeg"])

# If both files are uploaded
if file1 and file2:
    img1 = Image.open(file1).convert("RGB")
    img2 = Image.open(file2).convert("RGB")

    score, diff_image = highlight_differences(img1, img2)

    st.subheader(f"🧠 SSIM Similarity Score: `{score:.4f}`")
    st.image([img1, img2], caption=["Base Image", "Comparison Image"], width=300)
    st.image(diff_image, caption="🟥 Highlighted Pixel Differences", use_column_width=True)
