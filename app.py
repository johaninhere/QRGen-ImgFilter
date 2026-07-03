import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import segno
import io
import base64

# ==============================================================================
# 1. PAGE CONFIGURATION & LAYOUT
# ==============================================================================
st.set_page_config(
    page_title="Multi-Studio Workspace", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner interface
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stDeployButton { display: none; }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. WORKSPACE NAVIGATION (SIDEBAR)
# ==============================================================================
st.sidebar.title("🎛️ Workspace Control Hub")
st.sidebar.markdown("---")

studio_mode = st.sidebar.radio(
    "Select Workspace Engine Mode:",
    ["🎨 Advanced Image Studio", "🔮 Universal QR Engine"],
    help="Toggle between high-fidelity image manipulation and dynamic QR generation matrices."
)


# ==============================================================================
# 3. MODE A: ADVANCED IMAGE STUDIO
# ==============================================================================
if studio_mode == "🎨 Advanced Image Studio":
    st.title("🎨 Advanced Image Studio")
    st.caption("Perform high-fidelity structural alterations, custom convolutions, and data-weight optimization.")
    st.markdown("---")
    
    img_file = st.file_uploader("Upload an asset canvas...", type=["jpg", "jpeg", "png"], key="studio_uploader")
    
    if img_file is not None:
        try:
            # Load original image asset
            original_image = Image.open(img_file)
            
            # Sub-panel Configuration inside Sidebar
            st.sidebar.markdown("### ⚙️ Studio Configurations")
            
            # Filter Matrix Selector
            selected_filter = st.sidebar.selectbox(
                "Visual Filter Effect Matrix:",
                [
                    "Original", "Black & White", "Sepia Tone", "Gaussian Blur", 
                    "Contour Sketch", "Vibrant Saturation", "Retro Negative", "Emboss Art"
                ]
            )
            
            # Advanced Manipulation Canvas Tools Accordions
            with st.sidebar.expander("✂️ Dimensional Crop Pipeline", expanded=False):
                w, h = original_image.size
                left_crop = st.slider("Crop Left (px)", 0, w - 1, 0)
                right_crop = st.slider("Crop Right (px)", 0, w - 1, w)
                top_crop = st.slider("Crop Top (px)", 0, h - 1, 0)
                bottom_crop = st.slider("Crop Bottom (px)", 0, h - 1, h)
                
            with st.sidebar.expander("📐 Scale Resize Matrix", expanded=False):
                maintain_aspect = st.checkbox("Maintain Aspect Ratio", value=True)
                if maintain_aspect:
                    resize_ratio = st.slider("Scale Ratio (%)", 10, 200, 100)
                    new_w = int(w * (resize_ratio / 100))
                    new_h = int(h * (resize_ratio / 100))
                    st.caption(f"Target Resolution: {new_w}x{new_h}")
                else:
                    new_w = st.number_input("Target Width (px)", min_value=1, max_value=8000, value=w)
                    new_h = st.number_input("Target Height (px)", min_value=1, max_value=8000, value=h)
                    
            with st.sidebar.expander("💾 Compression & Quality Engine", expanded=False):
                compression_quality = st.slider("Export Quality Profile (1-100)", 1, 100, 85)
                
            # --- START PROCESSING CORE PIPELINE ---
            # 1. Handle Structural Cropping safely
            if left_crop < right_crop and top_crop < bottom_crop:
                processed_image = original_image.crop((left_crop, top_crop, right_crop, bottom_crop))
            else:
                st.error("❌ Spatial Integrity Violation: Crop boundary markers intersect invalid areas.")
                processed_image = original_image

            # 2. Handle Resizing
            processed_image = processed_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # 3. Apply Selected High-Fidelity Filters
            if selected_filter == "Black & White":
                processed_image = ImageOps.grayscale(processed_image)
            elif selected_filter == "Sepia Tone":
                gray = ImageOps.grayscale(processed_image)
                processed_image = ImageOps.colorize(gray, "#704214", "#C0B283")
            elif selected_filter == "Gaussian Blur":
                processed_image = processed_image.filter(ImageFilter.GaussianBlur(radius=5))
            elif selected_filter == "Contour Sketch":
                processed_image = processed_image.filter(ImageFilter.CONTOUR)
            elif selected_filter == "Vibrant Saturation":
                enhancer = ImageEnhance.Color(processed_image)
                processed_image = enhancer.enhance(2.5)  # Boost color saturation
            elif selected_filter == "Retro Negative":
                # Ensure image is in RGB mode prior to inversion processing
                if processed_image.mode in ("RGBA", "P"):
                    processed_image = processed_image.convert("RGB")
                processed_image = ImageOps.invert(processed_image)
            elif selected_filter == "Emboss Art":
                processed_image = processed_image.filter(ImageFilter.EMBOSS)

            # --- RENDER SIDE-BY-SIDE PIPELINE CORES ---
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📸 Original Canvas State")
                st.image(original_image, use_container_width=True, caption=f"Original Dimensions: {w}x{h}")
                
            with col2:
                st.markdown(f"### ✨ Processed Matrix: {selected_filter}")
                st.image(processed_image, use_container_width=True, caption=f"New Dimensions: {new_w}x{new_h}")
                
            st.markdown("---")
            
            # 4. Save to temporary byte array stream to evaluate weight and generate download payload
            buffer = io.BytesIO()
            # Convert to RGB if saving as JPEG to respect compression sliders optimally if desired, 
            # but we default to PNG fallback or JPEG based on original payload properties.
            img_format = "JPEG" if original_image.format in ["JPEG", "JPG"] else "PNG"
            
            processed_image.save(buffer, format=img_format, quality=compression_quality)
            byte_payload = buffer.getvalue()
            optimized_size_kb = len(byte_payload) / 1024
            
            # Performance Optimization Metrics Layout Panel
            st.markdown("### 📊 Live Optimization Profiler Metrics")
            m_col1, m_col2 = st.columns(2)
            m_col1.metric("Resulting Format Target", img_format)
            m_col2.metric("Computed In-Memory Data Weight", f"{optimized_size_kb:.2f} KB")
            
            st.download_button(
                label="📥 Export Optimized Filtered Asset",
                data=byte_payload,
                file_name=f"studio_output.{img_format.lower()}",
                mime=f"image/{img_format.lower()}",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"⚠️ Internal Processing Core Crash intercepted: {str(e)}")
            st.warning("Please modify parameter controls to return the operational pipeline state into nominal ranges.")
    else:
        st.info("💡 Standby: Upload a valid visual file structure configuration to ignite engine pipelines.")


# ==============================================================================
# 4. MODE B: UNIVERSAL QR ENGINE
# ==============================================================================
elif studio_mode == "🔮 Universal QR Engine":
    st.title("🔮 Universal QR Engine")
    st.caption("Encapsulate raw string streams, web redirects, or complete Base64 asset blocks inside QR matrices.")
    st.markdown("---")
    
    # 3 Structural Pipeline Configuration Modes
    qr_pipeline_type = st.tabs(["🔤 Text to QR Pipeline", "🔗 Link to QR Pipeline", "🖼️ Image to QR Asset Matrix"])
    
    # Core Matrix Styling overrides shared globally
    st.sidebar.markdown("### 🎨 QR Structural Palette")
    qr_color = st.sidebar.color_picker("Matrix Foreground Color (Dark):", "#000000")
    bg_color = st.sidebar.color_picker("Matrix Canvas Base Color (Light):", "#FFFFFF")
    qr_scale = st.sidebar.slider("Matrix Element Scale Resolution Modifier:", 1, 20, 10)
    
    payload_data = None
    
    # Text Input System Tab
    with qr_pipeline_type[0]:
        st.markdown("### Raw Literal String Serialization")
        raw_text_input = st.text_area("Input Raw Paragraph Block Data:", placeholder="Enter localized notes, metadata, or logs here...")
        if raw_text_input.strip() != "":
            payload_data = raw_text_input

    # Link Input System Tab
    with qr_pipeline_type[1]:
        st.markdown("### Absolute Target URL Navigation Engine")
        url_input = st.text_input("Input Target Destination Web Link Link URI:", placeholder="https://www.example.com")
        if url_input.strip() != "":
            if not (url_input.startswith("http://") or url_input.startswith("https://")):
                st.warning("⚠️ Formatting Alert: Standard protocol headers (http:// or https://) are recommended for dynamic device redirects.")
            payload_data = url_input

    # Image-to-QR High Capacity Matrix Tab
    with qr_pipeline_type[2]:
        st.markdown("### High Capacity Data Uri Matrix Injection (Base64)")
        st.caption("Warning: Large payload weights can cause extreme structural density scales inside generated matrices.")
        uploaded_qr_asset = st.file_uploader("Upload Image to Encode directly inside matrix:", type=["jpg", "png", "jpeg"], key="qr_asset_uploader")
        
        if uploaded_qr_asset is not None:
            try:
                # Execution protection layer block for encoding binary data blocks directly
                bytes_data = uploaded_qr_asset.read()
                if len(bytes_data) > 50 * 1024: # Warn if greater than 50KB due to QR version limit bounds
                    st.warning("⚠️ High Volume Data Warning: Images over 50KB might exceed maximum capacities for a standard QR matrix grid array.")
                
                # Encode binary asset block directly to Base64 String format structure
                base64_encoded = base64.b64encode(bytes_data).decode('utf-8')
                mime_type = uploaded_qr_asset.type
                # Synthesize standard browser read Data-URI payload block string element
                payload_data = f"data:{mime_type};base64,{base64_encoded}"
                st.success(f"Successfully serialized asset into raw base64 data string payload block. Length: {len(payload_data)} characters.")
            except Exception as e:
                st.error(f"❌ Structural Failure Encoded Engine Flagged on conversion routine: {str(e)}")

    # Matrix Compilation Core Processing Block Execution Gate
    st.markdown("---")
    if payload_data:
        if st.button("✨ Execute Matrix Grid Synthesis", use_container_width=True):
            # Containment Shield around generation steps to catch payload sizing limits overflow flags gracefully
            try:
                # Segment compilation block execution initialization
                compiled_qr = segno.make(payload_data)
                
                # Output buffering matrix stream
                qr_buffer = io.BytesIO()
                compiled_qr.save(qr_buffer, kind="png", scale=qr_scale, dark=qr_color, light=bg_color)
                qr_output_bytes = qr_buffer.getvalue()
                
                # Screen Rendering Canvas Elements
                st.markdown("### 🎯 Resultant Matrix Generation Structure Output")
                c_center1, c_center2, c_center3 = st.columns([1, 2, 1])
                with c_center2:
                    st.image(qr_output_bytes, caption="Generated Matrix Signature Field Core", use_container_width=True)
                
                # File Export Action Gateway Block
                st.download_button(
                    label="📥 Download Compiled QR Code Grid Matrix Asset",
                    data=qr_output_bytes,
                    file_name="universal_qr_matrix.png",
                    mime="image/png",
                    use_container_width=True
                )
            except segno.errors.DataOverflowError:
                st.error("❌ High Density Matrix Processing Error: The uploaded payload exceeds standard capacity bounds for standard QR configurations. Please reduce your text sizes or drastically shrink your input image file size.")
            except Exception as e:
                st.error(f"⚠️ Synthesis Intercept Core Crash Handler Exception Caught: {str(e)}")
    else:
        st.info("💡 Standby: Provide target string values, hyperlink blocks, or serialized images inside configuration parameters above.")
