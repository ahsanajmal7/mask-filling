# pip install pdfplumber
# pip install python-docx

import pdfplumber
from docx import Document

# Function to convert PDF to Word
def convert_pdf_to_word(pdf_path, word_path):
    # Create a Word document
    doc = Document()

    # Open and extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)
    
    # Save the Word file
    doc.save(word_path)
    print("Conversion complete!")

# Example usage
convert_pdf_to_word("example.pdf", "converted.docx")
