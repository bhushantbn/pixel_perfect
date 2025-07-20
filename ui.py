import streamlit as st
from PIL import Image, ImageChops
import numpy as np
from skimage.metrics import structural_similarity as ssim

st.set_page_config(page_title="Pixel Perfect Comparison", layout="wide")
st.title("🧪 Pixel-Perfect Image Comparison Tool")

def compare_images(img1, img2):
    gray1 = np.array(img1.convert("L"))
    gray2 = np.array(img2.convert("L"))
    score, diff = ssim(gray1, gray2, full=True)
    diff_img = Image.fromarray((1 - diff) * 255).convert("L")
    return score, diff_img

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Upload Base Image", type=["png", "jpg", "jpeg"])
with col2:
    file2 = st.file_uploader("Upload Comparison Image", type=["png", "jpg", "jpeg"])

if file1 and file2:
    img1 = Image.open(file1).convert("RGB")
    img2 = Image.open(file2).convert("RGB")

    if img1.size != img2.size:
        st.error("Images must be the same size!")
    else:
        score, diff_image = compare_images(img1, img2)
        st.subheader(f"🧠 SSIM Score: `{score:.4f}`")

        st.image([img1, img2], caption=["Base Image", "Comparison Image"], width=300)
        st.image(diff_image, caption="🔍 Difference Image (highlighted)", use_column_width=True)
