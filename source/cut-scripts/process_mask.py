import os
from PIL import Image, ImageOps

def process_image():
    # Find the .png image with "_LightingModel" in its name
    folder_path = os.getcwd()  # Get current working directory
    target_image = None
    
    for file in os.listdir(folder_path):
        if file.endswith(".png") and "_LightingModel" in file:
            target_image = file
            break
    
    if not target_image:
        print("No image with '_LightingModel' in its name found in the current folder.")
        return
    
    # Open the image
    image_path = os.path.join(folder_path, target_image)
    image = Image.open(image_path)
    
    # Convert the image to grayscale (desaturate)
    grayscale_image = ImageOps.grayscale(image)
    
    # Apply binary contrast (thresholding)
    binary_image = grayscale_image.point(lambda x: 0 if x < 128 else 255, '1')
    
    # Save the processed image
    output_path = os.path.join(folder_path, "binary_" + target_image)
    binary_image.save(output_path)
    print(f"Processed image saved as {output_path}")

if __name__ == "__main__":
    process_image()
