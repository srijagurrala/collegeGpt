from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from PyPDF2 import PdfReader  # Ensure you have PyPDF2 installed
import os

def create_search_index(index_dir):
    # Create the data directory if it doesn't exist
    if not os.path.exists('data'):
        os.mkdir('data')

    # Create the index directory if it doesn't exist
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
    index = create_in(index_dir, schema)

    # Index PDF files
    pdf_dir = 'data/pdfs'
    writer = index.writer()
    
    # Check if the pdf directory exists before indexing
    if not os.path.exists(pdf_dir):
        print(f"PDF directory '{pdf_dir}' does not exist.")
        return

    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    print(f"Found {len(pdf_files)} PDF files to index.")

    for filename in pdf_files:
        pdf_path = os.path.join(pdf_dir, filename)
        try:
            with open(pdf_path, 'rb') as f:
                reader = PdfReader(f)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:  # Check if page_text is not None
                        text += page_text + "\n"  # Add a newline to separate pages
                if text:  # Only index if there's text
                    writer.add_document(title=filename, content=text)
                    print(f"Indexed '{filename}' with {len(text)} characters.")
                else:
                    print(f"No extractable text in '{filename}'.")
        except Exception as e:
            print(f"Error reading '{filename}': {e}")

    writer.commit()
    print(f"Indexed {len(pdf_files)} PDF files.")
