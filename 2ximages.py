import os
from PIL import Image
import zipfile

def resize_image(image_path, factor=2):
    image = Image.open(image_path)
    new_image = image.resize((image.width * factor, image.height * factor))
    return new_image

def zip_images(input_folder, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith('.png'):
                    full_path = os.path.join(root, file)
                    image = resize_image(full_path)
                    image.save(full_path)  # Overwrite the original image
                    zipf.write(full_path, os.path.relpath(full_path, input_folder))

input_folder = 'your/input/folder'
output_zip = 'output.zip'
zip_images(input_folder, output_zip)
