# Load Indian Police documents into Mike's RAG memory.
print("Starting import...")

try:
    from agents.mike import Mike
    print("Mike imported")
except Exception as e:
    print(f"Mike import failed: {e}")
    exit()

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("Text splitter imported")
except Exception as e:
    print(f"Text splitter import failed: {e}")
    exit()

try:
    from pypdf import PdfReader
    print("PDF reader imported")
except Exception as e:
    print(f"PDF reader import failed: {e}")
    exit()

import os

print("\n" + "=" * 60)
print("MIKE ROSS - LOADING INDIAN POLICE MODULE")
print("=" * 60)

# Initialize Mike
print("\nInitializing Mike...")
mike = Mike()
print("Mike initialized")

def load_pdf_to_mike(pdf_path: str, source_name: str):
    # Extract text from PDF and load into Mike's vector memory
    print(f"\nProcessing: {source_name}")
    print(f"   Path: {pdf_path}")

    if not os.path.exists(pdf_path):
        print("   File not found")
        return False

    reader = PdfReader(pdf_path)
    full_text = ""
    total_pages = len(reader.pages)
    print(f"   Total pages: {total_pages}")

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
            full_text += text
        except Exception as e:
            print(f"   Page {i+1} extraction failed: {e}")

    print(f"   Extracted {len(full_text):,} characters")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = text_splitter.create_documents(
        texts=[full_text],
        metadatas=[{"source": source_name, "jurisdiction": "India"}]
    )

    if mike.vectorstore is None:
        print("   Creating new vector store...")
        from langchain_chroma import Chroma
        mike.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=mike.embeddings,
            persist_directory=mike.memory_path
        )
    else:
        print("   Adding to existing vector store...")
        mike.vectorstore.add_documents(chunks)

    print(f"   Added {len(chunks)} chunks to memory")
    return True

print("\n" + "-" * 40)
print("LOADING INDIAN POLICE DOCUMENTS")
print("-" * 40)

load_pdf_to_mike(
    pdf_path="./data/case_law/policeact.pdf",
    source_name="The Police Act, 1861"
)

load_pdf_to_mike(
    pdf_path="./data/case_law/policemanual.pdf",
    source_name="Indian Police Manual"
)

print("\n" + "=" * 60)
print("LOADING COMPLETE")
print("=" * 60)
