import io
import pdfplumber
import docx
import sys
import os
import traceback

def extract_text_pdf(file_path):
    print(f"Testing PDF extraction from: {file_path}")
    try:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
            print(f"File size: {len(file_bytes)} bytes")
            
            with io.BytesIO(file_bytes) as f_bytes:
                try:
                    with pdfplumber.open(f_bytes) as pdf:
                        print(f"PDF has {len(pdf.pages)} pages")
                        text = ""
                        for i, page in enumerate(pdf.pages):
                            try:
                                page_text = page.extract_text()
                                print(f"Page {i+1}: Extracted {len(page_text) if page_text else 0} characters")
                                if page_text:
                                    print(f"First 50 chars: {page_text[:50]}...")
                                text += page_text if page_text else ""
                            except Exception as e:
                                print(f"Error extracting text from page {i+1}: {str(e)}")
                                print(traceback.format_exc())
                        print(f"Extracted total of {len(text)} characters from PDF")
                        if text:
                            print(f"First 100 chars of extracted text: {text[:100]}...")
                        return text
                except Exception as e:
                    print(f"Error opening PDF with pdfplumber: {str(e)}")
                    print(traceback.format_exc())
                    return None
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        print(traceback.format_exc())
        return None

def extract_text_docx(file_path):
    print(f"Testing DOCX extraction from: {file_path}")
    try:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
            print(f"File size: {len(file_bytes)} bytes")
            
            with io.BytesIO(file_bytes) as f_bytes:
                try:
                    doc = docx.Document(f_bytes)
                    paragraphs = [para.text for para in doc.paragraphs]
                    print(f"DOCX has {len(paragraphs)} paragraphs")
                    text = "\n".join(paragraphs)
                    print(f"Extracted {len(text)} characters from DOCX")
                    if text:
                        print(f"First 100 chars of extracted text: {text[:100]}...")
                    return text
                except Exception as e:
                    print(f"Error processing DOCX with python-docx: {str(e)}")
                    print(traceback.format_exc())
                    return None
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        print(traceback.format_exc())
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_extraction.py <file_path>")
        return
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    print(f"File exists: {file_path}")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    
    if file_path.lower().endswith('.pdf'):
        result = extract_text_pdf(file_path)
        print(f"PDF extraction result: {'Success' if result else 'Failed'}")
    elif file_path.lower().endswith('.docx'):
        result = extract_text_docx(file_path)
        print(f"DOCX extraction result: {'Success' if result else 'Failed'}")
    else:
        print(f"Unsupported file format: {file_path}")

if __name__ == '__main__':
    main()