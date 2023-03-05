import os

import numpy as np
import pyheif
from PIL import Image, ImageOps

from helpers import *

@measure_elapsed_time
def rename_filenames(input_dir, start=1):
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.heic', '.png','.HEIC', '.PNG'))]
    image_files.sort()
    for i, image_file in enumerate(image_files, start=start):
        old_name = os.path.join(input_dir, image_file)
        ext = os.path.splitext(image_file)[1]
        new_name = os.path.join(input_dir, f"{i:05d}{ext}")
        while os.path.exists(new_name):
            i += 1
            new_name = os.path.join(input_dir, f"{i:05d}{ext}")
        os.rename(old_name, new_name)

@measure_elapsed_time
def convert_heic_to_rgb(input_dir, output_dir, color_count):
    create_output_dir_if_not_exists(output_dir)

    i = 0
    for filename in os.listdir(input_dir):
        if filename.endswith(('.heic', '.HEIC')):
            heif_file = pyheif.read(os.path.join(input_dir, filename))
            image_data = heif_file.data

            # Load image as Pillow Image object
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                image_data,
                "raw",
                heif_file.mode,
                heif_file.stride
            )

            # Downsample image to 576x768, same image as the depth image
            new_size = (576, 768)
            resized_image = image.resize(new_size)
            quantized_image = resized_image.convert("P", palette=Image.ADAPTIVE, colors=color_count)

            # Convert to RGBA format
            rgb_image = quantized_image.convert("RGB")

            # Save the image
            file_name_without_ext = os.path.splitext(filename)[0]
            rgb_image.save(os.path.join(output_dir, file_name_without_ext + ".png"))
            i += 1
    print(f"{i} HEIC file/s converted to RGB")

@measure_elapsed_time
def create_rgba_images(rgb_dir, depth_dir, output_dir):
    create_output_dir_if_not_exists(output_dir)

    rgb_files = [f for f in os.listdir(rgb_dir) if f.endswith(('.png', '.PNG'))]
    rgb_files.sort()

    for rgb_filename in rgb_files:
        rgb_path = os.path.join(rgb_dir, rgb_filename)
        depth_path = os.path.join(depth_dir, rgb_filename)
        with Image.open(rgb_path) as rgb_img, Image.open(depth_path).convert("L") as depth_img:
            # depth_data = np.asarray(depth_img)
            # depth_data_norm = (255 - depth_data) * (5/255)
            # min_val = np.min(depth_data_norm)
            # max_val = np.max(depth_data_norm)
            # depth_data_norm = (depth_data_norm - min_val) / (max_val - min_val) * 255
            depth_data = np.asarray(depth_img)
            depth_data_norm = (depth_data - np.min(depth_data)) / (np.max(depth_data) - np.min(depth_data)) * 255
            alpha_channel = Image.fromarray(depth_data_norm.astype(np.uint8))
            print(alpha_channel)
            rgba_img = Image.merge("RGBA", tuple(rgb_img.split()[:3]) + (alpha_channel,))
            output_path = os.path.join(output_dir, os.path.splitext(rgb_filename)[0] + ".png")
            rgba_img.save(output_path, format="PNG")

    print(f"{len(rgb_files)} RGBA image/s created")