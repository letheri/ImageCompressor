import os
from PIL import Image

MAX_WIDTH = 250
QUALITY = 80

def compress_and_resize_images(root_dir):
    # Iterate through all subdirectories and files
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Check if the file is an image
            if '_compressed' in file:
                continue
            elif file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(root, file)
                image = Image.open(image_path)

                # Resize the image while maintaining aspect ratio
                width, height = image.size
                if width > MAX_WIDTH:
                    new_height = int((MAX_WIDTH / width) * height)
                    resized_image = image.resize((MAX_WIDTH, new_height))
                else:
                    resized_image = image

                # Compress the resized image
                compressed_image = resized_image.copy()
                compressed_image.save(os.path.join(root, file.replace('.', '_compressed.')), quality = QUALITY)

                # Close the images to release memory
                resized_image.close()
                compressed_image.close()

if __name__ == "__main__":
    root_directory = r"root_path"  # Replace with your root directory path
    compress_and_resize_images(root_directory)
