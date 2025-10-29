import os
from PIL import Image

def apply_opacity_mask():
    # Find the binary image
    folder_path = os.getcwd()
    binary_image_name = None
    target_image_name = None
    
    for file in os.listdir(folder_path):
        if file.startswith("binary_") and file.endswith(".png"):
            binary_image_name = file
        elif file.startswith("HighresScreenshot") and file.endswith(".png") and len(file) == len("HighresScreenshot00000.png"):
            target_image_name = file
    
    if not binary_image_name:
        print("No binary image found in the current folder.")
        return
    
    if not target_image_name:
        print("No HighresScreenshot image with 5 digits found in the current folder.")
        return
    
    # Open the binary image and target image
    binary_image_path = os.path.join(folder_path, binary_image_name)
    target_image_path = os.path.join(folder_path, target_image_name)
    
    binary_image = Image.open(binary_image_path).convert("L")  # Ensure binary image is grayscale
    target_image = Image.open(target_image_path).convert("RGBA")  # Ensure target image is in RGBA mode
    
    # Create an alpha mask from the binary image
    alpha_mask = binary_image.point(lambda x: 255 if x == 255 else 0, 'L')
    
    # Apply the alpha mask to the target image
    target_image.putalpha(alpha_mask)
    
    # Save the resulting image
    output_path = os.path.join(folder_path, "masked_" + target_image_name)
    target_image.save(output_path, format="PNG")
    print(f"Masked image saved as {output_path}")

if __name__ == "__main__":
    apply_opacity_mask()