import os
import json

def merge_json_chunks(json_dir="jsons", chunk_group_size=5):
    json_files = [f for f in os.listdir(json_dir) if f.endswith(".json")]
    
    for json_file in json_files:
        file_path = os.path.join(json_dir, json_file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        original_chunks = content.get("chunks", [])
        merged_chunks = []

        for i in range(0, len(original_chunks), chunk_group_size):
            group = original_chunks[i:i + chunk_group_size]
            if not group:
                continue
            
            merged_chunk = {
                "number": group[0].get("number", ""),
                "title": group[0].get("title", ""),
                "start": group[0]["start"],
                "end": group[-1]["end"],
                "text": " ".join(c.get("text", "").strip() for c in group if c.get("text"))
            }
            merged_chunks.append(merged_chunk)

        content["chunks"] = merged_chunks

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)

        print(f"Processed {json_file}: Merged {len(original_chunks)} chunks -> {len(merged_chunks)} chunks.")

if __name__ == "__main__":
    merge_json_chunks()
