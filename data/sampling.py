import os

import numpy as np
import pyheif
from PIL import Image, ImageOps

from helpers import *

@measure_elapsed_time
def rename_filenames(input_dir, start):
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png','.heic'))]
    image_files.sort()

    for i, image_file in enumerate(image_files, start=start):
      old_name = os.path.join(input_dir, image_file)
      ext = os.path.splitext(image_file)[1]
      new_name = os.path.join(input_dir, f"{start:05d}{ext}")
      if os.path.exists(new_name) == True:
          print(f"File {new_name} already exists. Skipping...")
          break
      else:
        os.rename(old_name, new_name)
        start+=1


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

    rgb_files = [f for f in os.listdir(rgb_dir) if f.lower().endswith(('.png'))]
    rgb_files.sort()

    for rgb_filename in rgb_files:
        rgb_path = os.path.join(rgb_dir, rgb_filename)
        depth_path = os.path.join(depth_dir, rgb_filename)
        with Image.open(rgb_path) as rgb_img, Image.open(depth_path).convert("L") as depth_img:
            depth_data = np.asarray(depth_img)
            depth_data_norm = (depth_data - np.min(depth_data)) / (np.max(depth_data) - np.min(depth_data)) * 255
            alpha_channel = Image.fromarray(depth_data_norm.astype(np.uint8))
            # make alpha channel and rgb channels the same size
            if rgb_img.size != alpha_channel.size:
                rgb_img = rgb_img.resize(alpha_channel.size)
            rgba_img = Image.merge("RGBA", tuple(rgb_img.split()[:3]) + (alpha_channel,))
            rgba_img = rgba_img.resize((int(rgba_img.size[0]*0.25), int(rgba_img.size[1]*0.25)))
            output_path = os.path.join(output_dir, os.path.splitext(rgb_filename)[0] + ".png")
            rgba_img.save(output_path, format="PNG")

    print(f"{len(rgb_files)} RGBA image/s created")

def check_if_not_portrait_orientation(input_dir):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            filepath = os.path.join(input_dir, filename)
            with Image.open(filepath) as im:
                width, height = im.size
                if height < width:
                    print(f'{filename} is not in portrait mode.')

#rename_filenames("data/train-depth", start=1)
#rename_filenames("data/train-heic", start=1)
#convert_heic_to_rgb("data/train-heic", "data/train-rgb", color_count=256)
#check_if_not_portrait_orientation("data/train-depth")

#create_rgba_images("data/train-rgb", "data/train-depth", "data/train-rgbd/")