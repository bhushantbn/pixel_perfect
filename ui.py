import streamlit as st
from PIL import Image, ImageChops
import numpy as np
from skimage.metrics import structural_similarity as ssim

st.set_page_config(page_title="Pixel Perfect Comparison", layout="wide")
st.title("🎯 Pixel-Perfect Image Comparison Tool with Highlights")

def highlight_differences(img1, img2):
    # Resize comparison image to match base
    if img1.size != img2.size:
        st.warning(f"Resized comparison image from {img2.size} to match base image size {img1.size}")
        img2 = img2.resize(img1.size)

    # Convert to grayscale for SSIM
    gray1 = np.array(img1.convert("L"))
    gray2 = np.array(img2.convert("L"))

    # Calculate SSIM score and diff map
    score, diff = ssim(gray1, gray2, full=True)
    diff = (1 - diff) * 255
    diff = diff.astype(np.uint8)

    # Create a red highlight image
    red_highlight = np.zeros((*diff.shape, 3), dtype=np.uint8)
    red_highlight[..., 0] = diff  # Red channel

    # Overlay on original for visual effect
    overlay = Image.fromarray(red_highlight).convert("RGB")
    blended = Image.blend(img1.convert("RGB"), overlay, alpha=0.5)

    return score, blended

# Upload UI
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Upload Base Image", type=["png", "jpg", "jpeg"])
with col2:
    file2 = st.file_uploader("Upload Comparison Image", type=["png", "jpg", "jpeg"])

# When both uploaded
if file1 and file2:
    img1 = Image.open(file1).convert("RGB")
    img2 = Image.open(file2).convert("RGB")

    score, highlighted_diff = highlight_differences(img1, img2)

    st.subheader(f"🧠 SSIM Similarity Score: `{score:.4f}`")
    st.image([img1, img2], caption=["Base Image", "Comparison Image"], width=300)
    st.image(highlighted_diff, caption="🔍 Highlighted Differences", use_column_width=True)
