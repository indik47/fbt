import json
import os
import sys
from typing import Optional

import requests


def load_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def save_text_file(file_path: str, content: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def call_ollama(model: str, prompt: str, host: str = "http://localhost:11434", stream: bool = False,) -> str: 
    url = f"{host}/api/generate" 
    payload = {"model": model,"prompt": prompt,"stream": stream,}
    resp = requests.post(url, json=payload, timeout=600)
    resp.raise_for_status()

    if stream:
        # Not used by default, but kept for completeness
        result_chunks = []
        for line in resp.iter_lines():
            if not line:
                continue
            try:
                obj = json.loads(line)
                if "response" in obj:
                    result_chunks.append(obj["response"])
                if obj.get("done"):
                    break
            except json.JSONDecodeError:
                continue
        return "".join(result_chunks)
    else:
        obj = resp.json()
        # When stream=False, Ollama returns the full response in one JSON
        return obj.get("response", "")


def build_prompt(transcript_text: str, user_instruction: str) -> str:
    # Modify this template as needed. Keep it simple and editable.
    return (
        "Ти мій асистент, який допомагає робити підсумки робочого зідзвону.\n"
        "Текст транскрипції робочого зідзвону наданий нижче.\n\n"
        f"Інструкція: {user_instruction}\n\n"
        "Транскрипція:\n"
        f"{transcript_text}\n\n"
        "Поверни тільки структурований результат."
    )


def main(argv: Optional[list] = None) -> int:
    # ===== User-configurable settings =====
    # Default model (already downloaded per user)
    model = "qwen2.5:7b"
    #model = "llama3.2:3b"

    # Set the base name of your transcript file (matches transcribe.py)
    audio_basename = "07output_audio"

    # Folder and file paths
    videos_dir = r"C:\Users\denys.oligov\Videos"
    transcript_path = os.path.join(videos_dir, f"{audio_basename}.txt")
    output_path = os.path.join(videos_dir, f"{audio_basename}_structured.txt")

    # Instruction you can modify as needed
    user_instruction = (
        "Вихідний формат: аналіз тезисно (bullet points), валідація, декомпозиція"
    )
    # =====================================

    # Allow overriding transcript path and/or instruction via CLI (optional)
    args = argv if argv is not None else sys.argv[1:]
    if len(args) >= 1:
        transcript_path = args[0]
    if len(args) >= 2:
        user_instruction = args[1]
    if len(args) >= 3:
        output_path = args[2]

    if not os.path.exists(transcript_path):
        print(f"Transcript not found: {transcript_path}")
        return 1

    print(f"Reading transcript: {transcript_path}")
    transcript_text = load_text_file(transcript_path)

    prompt = build_prompt(transcript_text, user_instruction)
    print(f"Calling Ollama model '{model}'...")
    try:
        response_text = call_ollama(model=model, prompt=prompt, stream=False)
    except requests.RequestException as e:
        print(f"Error contacting Ollama: {e}")
        return 2

    print("Writing structured output...")
    save_text_file(output_path, response_text)
    print(f"Done. Output saved to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


