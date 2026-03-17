# rag.py
import os
import chromadb
from sentence_transformers import SentenceTransformer
from data_loader import load_compatibility_data, load_qa_data

embedder = SentenceTransformer('all-MiniLM-L6-v2')

# ✅ FIX 1: Use absolute path so db/ is always found
#    This puts the db/ folder in the SAME folder as rag.py itself
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db")

# ✅ FIX 2: PersistentClient — no .persist() needed in new ChromaDB
client = chromadb.PersistentClient(path=DB_PATH)
compat_collection = client.get_or_create_collection("compatibility")
qa_collection     = client.get_or_create_collection("astrology_qa")


def build_index():
    """Build ChromaDB index from your datasets. Only runs once."""

    # --- Compatibility index ---
    if compat_collection.count() == 0:
        print("🔄 Indexing compatibility data...")
        docs = load_compatibility_data([
            os.path.join(BASE_DIR, "data", "train.jsonl"),
            os.path.join(BASE_DIR, "data", "val.jsonl")
        ])

        BATCH = 500
        for i in range(0, len(docs), BATCH):
            batch = docs[i:i+BATCH]
            texts = [d["text"] for d in batch]
            embs  = embedder.encode(texts).tolist()
            compat_collection.add(
                documents=texts,
                embeddings=embs,
                ids=[f"compat_{i+j}" for j in range(len(batch))]
            )
            print(f"  Indexed {min(i+BATCH, len(docs))}/{len(docs)}")
        print("✅ Compatibility index built!")
    else:
        print(f"✅ Compatibility index loaded ({compat_collection.count()} docs)")

    # --- Q&A index ---
    if qa_collection.count() == 0:
        print("🔄 Indexing Q&A data...")
        docs = load_qa_data(os.path.join(BASE_DIR, "data", "astrology.json"))
        texts = [d["text"] for d in docs]
        embs  = embedder.encode(texts).tolist()
        qa_collection.add(
            documents=texts,
            embeddings=embs,
            ids=[f"qa_{i}" for i in range(len(docs))]
        )
        print("✅ Q&A index built!")
    else:
        print(f"✅ Q&A index loaded ({qa_collection.count()} docs)")


def retrieve(query: str, sign1: str = "", sign2: str = "",
             topic: str = "", top_k: int = 3) -> str:
    """Smart retrieval — searches both collections, returns best context."""

    enriched_query = f"{sign1} {sign2} {topic} {query}".strip()
    emb = embedder.encode([enriched_query]).tolist()

    compat_results = compat_collection.query(
        query_embeddings=emb, n_results=top_k
    )["documents"][0]

    qa_results = qa_collection.query(
        query_embeddings=emb, n_results=2
    )["documents"][0]

    context_parts = ["=== Compatibility Knowledge ==="]
    context_parts.extend(compat_results)
    context_parts.append("\n=== General Astrology Knowledge ===")
    context_parts.extend(qa_results)

    # Also search Reddit collection if available
    try:
        reddit_col = client.get_collection("reddit_astrology")
        reddit_results = reddit_col.query(
            query_embeddings=emb, n_results=2
        )["documents"][0]
        context_parts.append("\n=== Community Discussions ===")
        context_parts.extend(reddit_results)
    except:
        pass

    return "\n\n".join(context_parts)
