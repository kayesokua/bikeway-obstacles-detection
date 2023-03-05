# Documentation

`sampling.py` contains relevant functinos for batch resampling.

1. `rename_filenames(input_dir, start=1)` function takes an input directory path and an optional start argument, and renames all files in the directory with a new name starting from the given start value. The function searches for all HEIC and PNG files in the directory, sorts them alphabetically, and renames them sequentially with leading zeros to ensure proper file ordering.

2. `convert_heic_to_rgb(input_dir, output_dir, color_count)` function converts all HEIC image files in the input directory to RGB format and saves them to the output directory. The function loads each HEIC file, resizes it to 576x768, converts it to a quantized image with the given color count, and then converts it to an RGB image before saving it as a PNG file with the same filename in the output directory.

3. `create_rgba_images(input_depth_dir, input_rgb_dir, output_dir)` function creates RGB-D images by combining corresponding RGB and depth images. The function takes two input directories, one containing RGB images and the other containing depth images, and an output directory to save the resulting RGB-D images. The function loads each RGB and depth image, resizes the depth image to match the RGB image size, converts the depth image to depth values, and merges the RGB and depth images to create an RGBA image with depth values as alpha channels. The resulting RGBA image is then saved as a PNG file with the same filename in the output directory.