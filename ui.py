import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="Pixel Perfect Comparison", layout="wide")
st.title("🎯 Sharp Pixel Difference Highlighter")

def highlight_differences(img1, img2):
    # Resize second image to match the first
    if img1.size != img2.size:
        st.warning(f"Resizing comparison image from {img2.size} to match {img1.size}")
        img2 = img2.resize(img1.size)

    # Convert images to RGB arrays
    arr1 = np.array(img1.convert("RGB"))
    arr2 = np.array(img2.convert("RGB"))

    # Boolean mask: where any of the RGB channels differ
    diff_mask = np.any(arr1 != arr2, axis=-1)

    # Create a copy of the base image to highlight
    highlighted = arr1.copy()

    # Mark differing pixels in RED
    highlighted[diff_mask] = [255, 0, 0]

    # Calculate similarity score (based on unchanged pixels)
    total_pixels = diff_mask.size
    changed_pixels = np.count_nonzero(diff_mask)
    similarity_score = 1 - (changed_pixels / total_pixels)

    return similarity_score, Image.fromarray(highlighted)

# Upload section
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

    st.subheader(f"🧠 Pixel Similarity Score: `{score:.4f}`")
    st.image([img1, img2], caption=["Base Image", "Comparison Image"], width=300)
    st.image(diff_image, caption="🟥 Highlighted Pixel Differences", use_column_width=True)
