"""Rebuild Mike's RAG memory from the 3 case_law PDFs."""

from pathlib import Path

from pypdf import PdfReader

from agents.mike import Mike

CASE_LAW_FILES = [
    ("policeact.pdf", "The Police Act, 1861", "India"),
    ("policemanual.pdf", "Indian Police Manual", "India"),
    ("tenants.pdf", "NY Tenant Case Law", "New York"),
]


def read_pdf_text(pdf_path: Path) -> str:
    """Extract all text from a PDF file."""
    reader = PdfReader(str(pdf_path))
    pages_text = []
    for page in reader.pages:
        pages_text.append(page.extract_text() or "")
    return "\n".join(pages_text)


def main() -> None:
    print("=" * 60)
    print("MIKE ROSS - REBUILDING CASE LAW MEMORY")
    print("=" * 60)

    project_root = Path(__file__).resolve().parent
    case_law_dir = project_root / "data" / "case_law"

    mike = Mike()

    if mike.vectorstore is None:
        raise RuntimeError("Mike vectorstore did not initialize; cannot load memory.")

    # Rebuild memory so RAG is based on only the three target PDFs.
    print("\nClearing existing memory collection...")
    existing = mike.vectorstore.get(include=[])
    existing_ids = existing.get("ids", [])
    if existing_ids:
        mike.vectorstore.delete(ids=existing_ids)
    print(f"Memory collection cleared. Removed {len(existing_ids)} chunks.")

    loaded_sources = []
    for filename, source_name, jurisdiction in CASE_LAW_FILES:
        pdf_path = case_law_dir / filename
        print(f"\nLoading: {source_name}")
        print(f"Path: {pdf_path}")

        if not pdf_path.exists():
            raise FileNotFoundError(f"Missing required file: {pdf_path}")

        full_text = read_pdf_text(pdf_path)
        print(f"Extracted {len(full_text):,} characters")

        mike.add_to_memory(full_text, source=source_name, jurisdiction=jurisdiction)
        loaded_sources.append({"source": source_name, "jurisdiction": jurisdiction})

    final_count = mike.vectorstore._collection.count()
    print("\n" + "=" * 60)
    print("LOAD COMPLETE")
    print(f"Loaded sources: {[item['source'] for item in loaded_sources]}")
    print(f"Total chunks in memory: {final_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
