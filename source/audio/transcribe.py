from faster_whisper import WhisperModel
from tqdm import tqdm
# ... existing code ...
audio = r"07output_audio"

model = WhisperModel("large-v3-turbo", device="cuda")  # or "cpu"

# Find audio duration for progress approximation (requires pydub or librosa, here we do a fallback to segment count)
segments_generator, info = model.transcribe(
    rf"C:\Users\denys.oligov\Videos\{audio}.mp3",
    language="uk",       # "ru" for Russian; omit to auto-detect
    vad_filter=True
)

segments = []
print("Transcription in progress...")
# No total? tqdm will display spinner only
for seg in tqdm(segments_generator, desc="Transcribing", unit="segment"):
    segments.append(seg)
text = "".join(s.text for s in segments)

print(text)
with open(rf"C:\Users\denys.oligov\Videos\{audio}.txt", "w", encoding="utf-8") as f:
    f.write(text)
