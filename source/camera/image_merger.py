from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk, filedialog
from tkinter import ttk


def add_text_overlay(image, text):
    # Create a blank image for the text overlay
    overlay = Image.new(mode="RGBA", size=image.size, color=(0, 0, 0, 0))

    # Get a drawing context
    draw = ImageDraw.Draw(overlay)

    # Set the font and text color
    font = ImageFont.truetype("arial.ttf", size=40)
    color = (255, 255, 255)

    # Draw the text on the overlay
    text_size = draw.textsize(text, font=font)
    x = 10
    y = 10
    draw.text((x, y), text, fill=color, font=font)

    # Combine the image and overlay
    result = Image.alpha_composite(image.convert("RGBA"), overlay)

    return result.convert("RGB")


def choose_images():
    # Open a file dialog to select the images
    root = Tk()
    root.withdraw()
    image_paths = filedialog.askopenfilenames(title="Select images")

    # Filter out non-image files
    image_paths = [path for path in image_paths if path.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # Ensure that there are exactly two images selected
    if len(image_paths) != 2:
        raise ValueError("Please select exactly two images")

    # Load the source images
    image1 = Image.open(image_paths[0])
    image2 = Image.open(image_paths[1])

    # Ensure that the images have the same dimensions
    if image1.size != image2.size:
        raise ValueError("Images must have the same dimensions")

    # Add text overlay to each image
    image1 = add_text_overlay(image1, "Image 1")
    image2 = add_text_overlay(image2, "Image 2")

    # Create a new image to hold the merged result
    result = Image.new(mode="RGB", size=(image1.width, image1.height * 2))

    # Paste the first image at the top of the result image
    result.paste(im=image1, box=(0, 0))

    # Paste the second image at the bottom of the result image
    result.paste(im=image2, box=(0, image1.height))

    # Save the merged image
    result.save("merged_image.jpg")

    # Display the merged image
    result.show()


# Create a GUI window with a themed button and label
root = Tk()
style = ttk.Style()
style.theme_use('default')

label = ttk.Label(root, text="Click the button to choose two images to merge")
label.pack(pady=10)

button = ttk.Button(root, text="Choose Images", command=choose_images)
button.pack(pady=10)

root.mainloop()