import streamlit as st
from PIL import (
    Image,
    ImageOps,
    ImageFilter,
    ImageEnhance
)

import segno
import io
import os
import base64

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------

st.set_page_config(
    page_title="Creative Studio",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Creative Studio")
st.markdown(
"""
A production-ready workspace combining

- 🎨 Advanced Image Studio
- 🔮 Universal QR Engine

---
"""
)

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

st.sidebar.title("🧭 Workspace")

mode = st.sidebar.radio(
    "Choose Workspace",
    [
        "🎨 Advanced Image Studio",
        "🔮 Universal QR Engine"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("🎨 QR Styling")

qr_dark = st.sidebar.color_picker(
    "QR Line Color",
    "#000000"
)

qr_light = st.sidebar.color_picker(
    "QR Background",
    "#FFFFFF"
)

# -------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------

def image_bytes(image, quality=95):
    """
    Convert PIL image to PNG/JPEG bytes.
    """

    buffer = io.BytesIO()

    try:

        if image.mode == "RGBA":
            image.save(
                buffer,
                format="PNG"
            )

        else:
            image.save(
                buffer,
                format="JPEG",
                quality=quality
            )

        buffer.seek(0)

        return buffer

    except Exception as e:

        st.error(
            f"Image conversion failed.\n\n{e}"
        )

        return None


def image_size_kb(buffer):

    try:

        return len(buffer.getvalue()) / 1024

    except Exception:

        return 0


def apply_filter(image, selected):

    try:

        if selected == "Original":
            return image

        elif selected == "Black & White":
            return ImageOps.grayscale(image)

        elif selected == "Sepia Tone":

            gray = ImageOps.grayscale(image)

            return ImageOps.colorize(
                gray,
                "#704214",
                "#C0B283"
            )

        elif selected == "Gaussian Blur":

            return image.filter(
                ImageFilter.GaussianBlur(radius=5)
            )

        elif selected == "Contour Sketch":

            return image.filter(
                ImageFilter.CONTOUR
            )

        elif selected == "Vibrant Saturation":

            enhancer = ImageEnhance.Color(image)

            return enhancer.enhance(2.2)

        elif selected == "Retro Negative":

            if image.mode == "RGBA":

                rgb = image.convert("RGB")

                return ImageOps.invert(rgb)

            return ImageOps.invert(image)

        elif selected == "Emboss Art":

            return image.filter(
                ImageFilter.EMBOSS
            )

        return image

    except Exception as e:

        st.warning(
            f"Filter processing failed:\n{e}"
        )

        return image


def crop_image(
    image,
    left,
    top,
    right,
    bottom
):

    try:

        w, h = image.size

        return image.crop(
            (
                left,
                top,
                w - right,
                h - bottom
            )
        )

    except Exception as e:

        st.warning(
            f"Cropping failed:\n{e}"
        )

        return image


def resize_image(
    image,
    width,
    height
):

    try:

        return image.resize(
            (width, height)
        )

    except Exception as e:

        st.warning(
            f"Resize failed:\n{e}"
        )

        return image


def image_to_base64(upload):

    try:

        data = upload.read()

        encoded = base64.b64encode(
            data
        ).decode()

        mime = upload.type

        return f"data:{mime};base64,{encoded}"

    except Exception as e:

        st.warning(
            f"Base64 encoding failed:\n{e}"
        )

        return None


def build_qr(payload):

    try:

        qr = segno.make(
            payload,
            error="H"
        )

        buffer = io.BytesIO()

        qr.save(
            buffer,
            kind="png",
            scale=10,
            dark=qr_dark,
            light=qr_light
        )

        buffer.seek(0)

        return buffer

    except Exception as e:

        st.warning(
            f"QR generation failed:\n{e}"
        )

        return None

# =======================================================
# MODE A
# =======================================================

if mode == "🎨 Advanced Image Studio":

    st.header("🎨 Advanced Image Studio")

    uploaded = st.file_uploader(
        "Upload Image",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    if uploaded is not None:

        try:

            original = Image.open(uploaded)

        except Exception as e:

            st.error(
                f"Unable to open image.\n\n{e}"
            )

            st.stop()

        st.markdown("---")

        st.subheader("🎛 Filter Controls")

        filter_name = st.selectbox(
            "Choose Filter",
            [
                "Original",
                "Black & White",
                "Sepia Tone",
                "Gaussian Blur",
                "Contour Sketch",
                "Vibrant Saturation",
                "Retro Negative",
                "Emboss Art"
            ]
        )

        processed = apply_filter(
            original,
            filter_name
        )
