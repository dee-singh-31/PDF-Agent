import os
import sys
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
import ollama

def extract_text_from_pdf(pdf_path: str) -> str:
    """Reads digital text from a PDF."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception:
        return ""

def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    """Extracts text layout locally via Tesseract instead of Ollama vision engines."""
    print("📸 Scanned PDF detected. Extracting text layout via local OCR engine...")
    
    # Convert first page to image using your verified poppler path
    pages = convert_from_path(pdf_path, first_page=1, last_page=1, poppler_path="/opt/homebrew/bin")
    if not pages:
        return ""
        
    # Extract string characters visually from the image page
    extracted_text = pytesseract.image_to_string(pages[0])
    return extracted_text

def extract_expiry_date_free(document_text: str):
    """Sends text layout to the standard free text model which avoids the mllama bug."""
    prompt = f"""
    You are an expert document analysis agent.
    Analyze the following text layout and extract the expiration date.
    
    Respond ONLY with a raw JSON object matching this schema:
    {{
        "expiry_date": "YYYY-MM-DD or null if not found",
        "confidence_reasoning": "A short sentence explaining where it was found"
    }}

    Document Text:
    {document_text}
    """

    # Uses the standard llama3.2 text model which is highly stable
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n❌ Error: Please provide the path to a PDF file.")
    else:
        pdf_file_path = sys.argv[1]
        
        if not os.path.exists(pdf_file_path):
            print(f"❌ Error: File '{pdf_file_path}' not found.")
        else:
            print(f"📖 Reading '{pdf_file_path}'...")
            text_content = extract_text_from_pdf(pdf_file_path)
            
            # If standard text extraction fails, fallback to local python OCR
            if not text_content:
                text_content = extract_text_from_scanned_pdf(pdf_file_path)
                
            if not text_content.strip():
                print("❌ Failed to extract any readable text character layouts.")
            else:
                print("🧠 Processing text locally via standard Llama...")
                result = extract_expiry_date_free(text_content)
                print("\n✨ --- Local AI Extraction Results --- ✨")
                print(result)