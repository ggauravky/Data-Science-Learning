import whisper
import json

model = whisper.load_model("medium")


result=model.transcribe(audio="audio/sample.mp3", language="hi", task="transcribe" , word_timestamps=False)

# print(result["segments"])
chunks = []

for segment in result["segments"]:
    chunk = {
        "start": segment["start"],
        "end": segment["end"],
        "text": segment["text"]
    }
    chunks.append(chunk)

print(chunks)

with open("output.json", "w") as f:
    json.dump(chunks, f)