from faster_whisper import WhisperModel
#import torch

audio = r"05output_audio"

model = WhisperModel("large-v3-turbo", device="cuda")  # or "cpu"
segments, info = model.transcribe(
    rf"C:\Users\denys.oligov\Videos\{audio}.mp3",
    language="uk",       # "ru" for Russian; omit to auto-detect
    vad_filter=True
)
text = "".join(s.text for s in segments)

with open(rf"{audio}.txt", "w", encoding="utf-8") as f:
    f.write(text)