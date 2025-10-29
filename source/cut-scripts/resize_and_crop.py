import os
from PIL import Image

def resize_and_crop_power_of_two():
    # Find the masked image
    folder_path = os.getcwd()
    masked_image_name = None
    
    for file in os.listdir(folder_path):
        if file.startswith("masked_") and file.endswith(".png"):
            masked_image_name = file
            break
    
    if not masked_image_name:
        print("No masked image found in the current folder.")
        return
    
    # Open the masked image
    masked_image_path = os.path.join(folder_path, masked_image_name)
    image = Image.open(masked_image_path).convert("RGBA")

    # Get the bounding box of the non-transparent parts
    bbox = image.getbbox()
    if not bbox:
        print("The image is fully transparent.")
        return
    
    # Crop the image to the bounding box with padding
    left, upper, right, lower = bbox
    padding = 5
    left = max(0, left - padding)
    upper = max(0, upper - padding)
    right = min(image.width, right + padding)
    lower = min(image.height, lower + padding)
    
    cropped_image = image.crop((left, upper, right, lower))

    # Find the closest power of 2 dimensions
    def closest_power_of_two(x):
        return 1 << (x - 1).bit_length()

    new_width = closest_power_of_two(cropped_image.width)
    new_height = closest_power_of_two(cropped_image.height)

    # Ensure new dimensions are at least the size of the cropped image
    if new_width < cropped_image.width:
        new_width *= 2
    if new_height < cropped_image.height:
        new_height *= 2

    # Create a new image with the required size and paste the cropped image centered
    new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    offset_x = (new_width - cropped_image.width) // 2
    offset_y = (new_height - cropped_image.height) // 2
    new_image.paste(cropped_image, (offset_x, offset_y))
    
    # Save the resized and cropped image
    output_path = os.path.join(folder_path, "resized_" + masked_image_name)
    new_image.save(output_path, format="PNG")
    print(f"Resized and cropped image saved as {output_path}")

if __name__ == "__main__":
    resize_and_crop_power_of_two()
