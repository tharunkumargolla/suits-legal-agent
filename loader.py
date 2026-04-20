from agents.mike import Mike
from pypdf import PdfReader
import os

print("📚 MIKE ROSS - LOADING INTO EIDETIC MEMORY")
print("=" * 50)

mike = Mike()

# Path to your PDF
pdf_path = "./data/case_law/tenants.pdf"  # Adjust name if different

if not os.path.exists(pdf_path):
    print(f"❌ PDF not found at {pdf_path}")
    print("Check the file name and location")
    exit()

# Extract text from PDF
print(f"📄 Reading: {pdf_path}")
reader = PdfReader(pdf_path)
full_text = ""
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    full_text += text
    print(f"   Read page {i+1}")

print(f"\n✅ Extracted {len(full_text)} characters")

# Load into Mike's memory
print("\n🧠 Memorizing...")
mike.add_to_memory(full_text, source="NY Tenant Case Law")

print("\n" + "=" * 50)
print("✅ MIKE HAS MEMORIZED THE CASE")
print("He can now recall this when researching tenant issues")