# pip install pdfplumber
# pip install python-docx
# pip install streamlit

import streamlit as st
import pdfplumber
from docx import Document

# App title
st.title("PDF to Word Converter")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Create a Word document
    doc = Document()

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)

    # Save the Word document
    output_filename = "converted.docx"
    doc.save(output_filename)

    # Download link
    with open(output_filename, "rb") as file:
        st.download_button(
            label="Download Word File",
            data=file,
            file_name="converted.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
