import whisper
import json
import os

model = whisper.load_model("large-v2")

audios = os.listdir("audios")

for audio in audios:
    print(f"Processing audio file: {audio}")
    if "_" in audio:
        number = audio.split("_")[0]
        title = audio.split("_")[1][:-4]  # Remove the .mp3 extension
        print(f"Number: {number}, Title: {title}")
        result = model.transcribe(
            audio=f"audios/{audio}",
            language="en",
            task="transcribe",
            word_timestamps=False,
        )
        chunks = []

        for segment in result["segments"]:
            chunk = {
                "number": number,
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"],
            }
            chunks.append(chunk)

        chunks_with_metadata = {"chunks": chunks, "text": result["text"]}

        with open(f"json/{audio}.json", "w", encoding="utf-8") as f:
            json.dump(chunks_with_metadata, f)
