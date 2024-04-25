import streamlit as st

def main():
    st.title("Text to PDF Converter")

    # Add text input field
    text_input = st.text_area("Enter your text here:")

    # Add a button to trigger PDF generation
    if st.button("Generate PDF"):
        # Call function to process text and generate PDF
        pdf_path = generate_pdf(text_input)

        # Display download button for the generated PDF
        download_button = st.download_button(label="Download PDF", data=open("output.pdf", "rb").read(), file_name="output.pdf")
        st.markdown(download_button, unsafe_allow_html=True)

from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def translate_text(text, target_language='es'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def create_pdf(english_text, spanish_text, filename='output.pdf'):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']

    translated_table_data = [
        [Paragraph(english_text, style_normal), Paragraph(spanish_text, style_normal)]
    ]

    table = Table(translated_table_data, colWidths=[300, 300])
    table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                               ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                               ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black),
                               ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                               ('FONTSIZE', (0, 0), (-1, -1), 10),
                               ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                               ]))
    
    doc.build([table])


def generate_pdf(english_text):
    spanish_text = translate_text(english_text)
    create_pdf(english_text, spanish_text)
    st.write("PDF Created!")

if __name__ == "__main__":
    main()
