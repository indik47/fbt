import os
import re

def cleanup_images():
    folder_path = os.getcwd()
    keep_pattern = re.compile(r"HighresScreenshot\d{5}(_LightingModel)?\.png")

    for file in os.listdir(folder_path):
        if file.endswith(".png") and not keep_pattern.match(file):
            os.remove(os.path.join(folder_path, file))
            print(f"Deleted: {file}")

if __name__ == "__main__":
    cleanup_images()