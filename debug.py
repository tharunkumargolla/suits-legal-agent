from agents.mike import Mike

print("🔍 DEBUGGING MIKE'S MEMORY")
print("=" * 50)

mike = Mike()

# Check if vectorstore exists
print(f"Vectorstore loaded: {mike.vectorstore is not None}")

if mike.vectorstore:
    # Try a direct search
    query = "landlord selling building tenant lease"
    print(f"\nSearching for: '{query}'")
    
    docs = mike.vectorstore.similarity_search(query, k=3)
    
    print(f"Found {len(docs)} documents")
    
    for i, doc in enumerate(docs, 1):
        print(f"\n--- Document {i} ---")
        print(f"Content preview: {doc.page_content[:300]}...")
        print(f"Source: {doc.metadata.get('source', 'unknown')}")
else:
    print("❌ No vectorstore - memory failed to load")