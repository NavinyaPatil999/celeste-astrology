import json

def load_compatibility_data(paths=["data/train.jsonl", "data/val.jsonl"]):
    docs = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                row = json.loads(line.strip())

                combined = (
                    f"{row['instruction']} "
                    f"{row['input']} "
                    f"Answer: {row['output']}"
                )

                docs.append({
                    "text": combined,
                    "instruction": row["instruction"],
                    "input": row["input"],
                    "output": row["output"]
                })

    print(f"✅ Loaded {len(docs)} compatibility examples")
    return docs


def load_qa_data(path="data/astrology.json"):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)["json"]

    docs = []
    for item in data:
        q = item.get("pregunta", "")
        a = item.get("respuesta", "")

        docs.append({
            "text": f"Q: {q} A: {a}",
            "question": q,
            "answer": a
        })

    print(f"✅ Loaded {len(docs)} Q&A pairs")
    return docs