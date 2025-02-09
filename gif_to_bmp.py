import os
import glob
import imageio
import shutil
from PIL import Image


source_directory = './sourceGIF/'
output_directory = './outputBMP/'
final_output_directory = './finalVersions/'
gif_list = []

# remove output directory and then recreate output directory... clears a path to work
if os.path.exists(output_directory):
    shutil.rmtree(output_directory)
os.mkdir(output_directory)

if os.path.exists(final_output_directory) is  False:
    os.mkdir(final_output_directory)
if os.path.exists(source_directory) is  False:
    os.mkdir(source_directory)

# splits source gif into frames
def gif_splitter(gif):
    gif_being_split = imageio.get_reader(gif)
    for frame_index, frame in enumerate(gif_being_split):
        frame_index_str = f"{frame_index:02}"  
        imageio.imwrite(f"outputBMP/{os.path.basename(gif)[:-4]}/frame_{frame_index_str}.bmp", frame)

# resizes split frames into 32x32
def bmp_builder(bmp):
    output_subdirectory = os.path.join(output_directory + gif_list[bmp])
    for each_file in glob.glob(os.path.join(output_subdirectory, '*.bmp')):
        with Image.open(each_file) as img:
            resized_img = img.resize((32, 32))
            resized_img.save(each_file)
    stack_images_vertically(output_subdirectory, bmp)

# stack the 32x32 frames into a tall bmp
def stack_images_vertically(directory, num):
    bmp_files = []

    for each_file in glob.glob(os.path.join(directory, '*.bmp')):
        bmp_files.append(each_file)
    final_height = len(bmp_files) * 32
    
    stacked_image = Image.new('RGB', (32, final_height))
    
    y_offset = 0
    for frame in bmp_files:
        with Image.open(frame) as ind_frame:
            stacked_image.paste(ind_frame, (0, y_offset))
            y_offset += 32

    stacked_image.save(os.path.join(final_output_directory, gif_list[num] + '.bmp'))

# function to create a directory for each file and run the script against it
for file_number, each_file in enumerate(glob.glob(os.path.join(source_directory, '*.gif'))):
    gif_list.append(os.path.basename(each_file)[:-4])
    os.mkdir(f"./outputBMP/{os.path.basename(each_file)[:-4]}")
    gif_splitter(each_file)
    bmp_builder(file_number) 
    
shutil.rmtree(output_directory)



