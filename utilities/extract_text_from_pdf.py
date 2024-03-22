import fitz
import sys
import os

def extract_text_from_pdf(pdf_path, output_file_path):
    doc = fitz.open(pdf_path)
    
    all_text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        all_text += page.get_text()
    
    doc.close()
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(all_text)

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/your/document.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_file_name = "extracted_text.txt"
    output_file_path = os.path.join(os.getcwd(), output_file_name)
    
    extract_text_from_pdf(pdf_path, output_file_path)

    print(f"Extracted text has been written to {output_file_path}")
