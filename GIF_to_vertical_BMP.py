import os
import glob
import imageio
import shutil
from PIL import Image

source_directory = './sourceGIF/'
output_directory = './outputBMP/'
gif_list = []

# remove output directory and then recreate output directory... clears a path to work
shutil.rmtree(output_directory)
os.mkdir(output_directory)

# This function splits the gifs into individual frames
def gif_splitter(gif):
    gif_being_split = imageio.get_reader(gif)
    for frame_index, frame in enumerate(gif_being_split):
        imageio.imwrite(f"outputBMP/{os.path.basename(gif)[:-4]}/frame_{frame_index}.bmp", frame)

# This function processes the individual frames and resizes them to 32x32
def bmp_builder(bmp):
    output_subdirectory = os.path.join(output_directory + gif_list[bmp])
    print(f"This is the output subdirectory:{output_subdirectory}")
    for each_file in glob.glob(os.path.join(output_subdirectory, '*.bmp')):
        print(each_file)
        with Image.open(each_file) as img:
            resized_img = img.resize((32, 32))
            resized_img.save(each_file)
    stack_images_vertically(output_subdirectory, bmp)

# This function stacks the frames into one tall bmp
def stack_images_vertically(directory, num):
    bmp_files = []
    for each_file in glob.glob(os.path.join(directory, '*.bmp')):
        bmp_files.append(each_file)
    print(len(bmp_files))
    final_height = len(bmp_files) * 32
    
    stacked_image = Image.new('RGB', (32, final_height))
    
    # Paste each image into the new blank image at the correct position
    y_offset = 0
    for frame in bmp_files:
        with Image.open(frame) as ind_frame:
            stacked_image.paste(ind_frame, (0, y_offset))
            y_offset += 32
    # Save the tall image    
    stacked_image.save(os.path.join(directory, gif_list[num] + '.bmp'))

# One function to rule them all, and in the darkness bind them
for file_number, each_file in enumerate(glob.glob(os.path.join(source_directory, '*.gif'))):
    gif_list.append(os.path.basename(each_file)[:-4])
    os.mkdir(f"./outputBMP/{os.path.basename(each_file)[:-4]}")
    gif_splitter(each_file)
    bmp_builder(file_number) 
