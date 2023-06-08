import datetime
import json
import logging
import os
import sys

from PIL import Image, ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES = True
MAX_WIDTH = 250
QUALITY = 70


def date():
    return str(datetime.datetime.today()).split('.')[0].replace(' ', '__').replace(':', '-')


def check_folder(file_array, root):
    # Checks if the folder has all images compressed
    _compressedCount = len(list(filter(lambda x: '_compressed' in x, file_array)))
    _notCompressedCount = len(file_array) - _compressedCount
    if _compressedCount == _notCompressedCount:
        # logging.info(f'Klasör atlanıyor: {root}')
        return True
    return False


def compress_and_resize_images(root_dir):
    # Iterate through all subdirectories and files
    for root, dirs, files in os.walk(root_dir):
        print(root, dirs, files)
        if check_folder(files, root):
            # Skip the folder if the folder has already been compressed
            continue
        for file in files:
            # Check if the file is an image
            if '_compressed' in file:
                continue
            elif file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                try:
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
                    compressed_image.save(os.path.join(root, file.replace('.', '_compressed.')), optimize=True,
                                          quality=QUALITY)

                    # Close the images to release memory
                    resized_image.close()
                    compressed_image.close()
                except IOError:
                    logging.error(f'Resim dosyası okuma hatası.. Dosya Yolu:\n {os.path.join(root, file)}')
                    pass
                except Exception as ex:
                    logging.error(f'Hata: {ex}')


if __name__ == "__main__":
    doesLogFolderExist = os.path.exists('log')
    if not doesLogFolderExist:
        os.makedirs('log')
    logging.basicConfig(filename=fr'log\{date()}.log', filemode='x', format='%(name)s - %(levelname)s - %(message)s',
                        level=20, encoding="utf-8")

    logging.info(f'Feniş Resim sıkıştırma servisi başlıyor..\nTarih: ' + date())
    try:
        config = json.loads(open("config.json", "r", encoding="utf-8").read())
        root_directory = config['folder_path']
        if len(sys.argv) > 1:
            # Override the root directory if a command line argument exists
            root_directory = sys.argv[1]
        logging.info(f'Sıkıştırma için kullanılan klasör..\n{root_directory}')
        compress_and_resize_images(root_directory)
    except Exception as ex:
        logging.error(f'Hata: {ex}')
