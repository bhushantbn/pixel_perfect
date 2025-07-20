import streamlit as st
from PIL import Image
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os

def compare_images(img1_np, img2_np):
    gray1 = cv2.cvtColor(img1_np, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2_np, cv2.COLOR_RGB2GRAY)
    score, diff = ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")
    return score, diff

st.set_page_config(page_title="Pixel Perfect Comparison", layout="wide")
st.title("🧪 Pixel-Perfect Image Comparison Tool")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Upload Base Image", type=["png", "jpg", "jpeg"], key="file1")
with col2:
    file2 = st.file_uploader("Upload Comparison Image", type=["png", "jpg", "jpeg"], key="file2")

if file1 and file2:
    image1 = Image.open(file1).convert("RGB")
    image2 = Image.open(file2).convert("RGB")
    img1_np = np.array(image1)
    img2_np = np.array(image2)

    if img1_np.shape != img2_np.shape:
        st.error("Uploaded images must have the same dimensions!")
    else:
        score, diff = compare_images(img1_np, img2_np)
        st.markdown(f"### 🧠 Structural Similarity Index (SSIM): `{score:.4f}`")

        st.image([image1, image2], caption=["Base Image", "Comparison Image"], width=300)
        st.image(diff, caption="🔍 Difference Image", use_column_width=True)