import fitz  # for PDF
import docx  # for DOCX
import os

def clean_text(text):
    # Remove multiple spaces and newlines, convert to lowercase
    return ' '.join(text.replace('\n', ' ').replace('\r', '').split()).lower()

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return clean_text(text)

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return clean_text(full_text)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return clean_text(f.read())

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("❌ Unsupported file type: " + ext)