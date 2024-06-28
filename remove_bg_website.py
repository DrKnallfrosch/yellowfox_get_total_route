import requests
from PIL import Image
from io import BytesIO


def remove_background(image_url, output_path):
    try:
        # Step 1: Download the image
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Step 2: Ensure image is in RGBA format
        img = img.convert("RGBA")

        # Step 3: Detect the background color (top-left pixel)
        background_color = img.getpixel((0, 0))

        # Step 4: Create a new image with a transparent background
        new_img = Image.new("RGBA", img.size, (255, 255, 255, 0))

        def color_distance(c1, c2):
            return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

        # Define a color distance threshold
        threshold = 50

        for x in range(img.width):
            for y in range(img.height):
                pixel = img.getpixel((x, y))
                if color_distance(pixel[:3], background_color[:3]) < threshold:
                    new_img.putpixel((x, y), (255, 255, 255, 0))
                else:
                    new_img.putpixel((x, y), pixel)

        # Step 5: Save the image with a transparent background
        new_img.save(output_path, format="ICO")
        print(f"Background removed. Saved as {output_path}")
    except Exception as e:
        print(f"Error: {e}")
