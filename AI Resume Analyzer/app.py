import streamlit as st
from PIL import Image
import os
import tempfile
from resume_analyzer import analyze_resume_text
from extract_text_easyocr import extract_text_easyocr  

# Set page config
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .report-title {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 20px;
        font-weight: bold;
        color: #2E7D32;
        margin-top: 15px;
    }
    .suggestion {
        background-color: #FFF9C4;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .score-high {
        color: #2E7D32;
        font-weight: bold;
    }
    .score-medium {
        color: #FF9800;
        font-weight: bold;
    }
    .score-low {
        color: #D32F2F;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and get instant feedback on how well it matches job requirements!")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose a resume (PNG, JPG, PDF)",
        type=["png", "jpg", "jpeg", "pdf"],
        accept_multiple_files=False
    )
    
    st.markdown("---")
    st.markdown("### Customize Analysis")
    job_role = st.selectbox(
        "Target Job Role",
        ["Data Scientist", "Machine Learning Engineer", "Data Analyst", "Software Engineer"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This tool analyzes your resume for:")
    st.markdown("- 📊 Skills match")
    st.markdown("- 🎓 Education qualifications")
    st.markdown("- 💼 Relevant experience")
    st.markdown("- ✨ Resume quality")

# Main content area
if uploaded_file is not None:
    # Save uploaded file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    # Show processing message
    with st.spinner("Analyzing your resume..."):
        # Step 1: Extract text
        extracted_text = extract_text_easyocr(tmp_path)
        
        if not extracted_text.strip():
            st.error("Could not extract text from the uploaded file. Please try a clearer image.")
            st.stop()
        
        # Step 2: Analyze text
        report, visual_summary = analyze_resume_text(extracted_text)
        
        # Clean up temp file
        os.unlink(tmp_path)
    
    # Display results in expandable sections
    st.markdown(f'<div class="report-title">Resume Analysis Report for {job_role}</div>', unsafe_allow_html=True)
    
    # Visual summary
    st.image("resume_analysis_summary.png", use_column_width=True)
    
    # Detailed report
    with st.expander("📊 Detailed Analysis", expanded=True):
        # Skills section
        st.markdown('<div class="section-title">1️⃣ Skills Match</div>', unsafe_allow_html=True)
        st.write(report.split("2️⃣ Education Match:")[0].split("1️⃣ Skills Match:")[1].strip())
        
        # Education section
        st.markdown('<div class="section-title">2️⃣ Education Match</div>', unsafe_allow_html=True)
        st.write(report.split("3️⃣ Experience Match:")[0].split("2️⃣ Education Match:")[1].strip())
        
        # Experience section
        st.markdown('<div class="section-title">3️⃣ Experience Match</div>', unsafe_allow_html=True)
        st.write(report.split("4️⃣ Resume Quality Check:")[0].split("3️⃣ Experience Match:")[1].strip())
        
        # Quality section
        st.markdown('<div class="section-title">4️⃣ Resume Quality Check</div>', unsafe_allow_html=True)
        st.write(report.split("5️⃣ Final Fit Score:")[0].split("4️⃣ Resume Quality Check:")[1].strip())
        
        # Final score
        st.markdown('<div class="section-title">5️⃣ Final Fit Score</div>', unsafe_allow_html=True)
        final_score_part = report.split("5️⃣ Final Fit Score:")[1].strip()
        score_value = int(final_score_part.split("%")[0])
        
        if score_value >= 80:
            score_class = "score-high"
        elif score_value >= 60:
            score_class = "score-medium"
        else:
            score_class = "score-low"
        
        st.markdown(f'<div class="{score_class}">Final Fit Score: {score_value}%</div>', unsafe_allow_html=True)
        st.write(final_score_part.split(str(score_value) + "%")[1].strip())
    
    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        with open("resume_analysis_report.txt", "rb") as f:
            st.download_button(
                label="📥 Download Text Report",
                data=f,
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )
    with col2:
        with open("resume_analysis_summary.png", "rb") as f:
            st.download_button(
                label="📥 Download Visual Summary",
                data=f,
                file_name="resume_analysis_summary.png",
                mime="image/png"
            )
    
    # Show raw extracted text (optional)
    with st.expander("🔍 View Extracted Text"):
        st.text_area("Text extracted from your resume:", extracted_text, height=300)

else:
    # Show instructions when no file is uploaded
    st.info("👈 Please upload your resume to get started")
    st.markdown("""
    ### How It Works:
    1. Upload your resume (PNG/JPG/PDF)
    2. Select your target job role
    3. Get instant analysis with:
        - Skills matching score
        - Education verification
        - Experience evaluation
        - Resume quality check
    4. Download your full report
    
    ### Tips for Best Results:
    - Use clear, high-quality images
    - Ensure text is readable (no handwriting)
    - Upload the most recent version of your resume
    """)