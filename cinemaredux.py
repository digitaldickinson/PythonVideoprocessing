"""
A SCRIPT TO CREATE CINEMA REDUX STYLE IMAGE FROM A VIDEO FILE
Inspired by Brendan Dawes cinenmaredux work - http://www.brendandawes.com/projects/cinemaredux

"""
#import some libs to work with
import cv2 #The openCV lib to do video processing
import numpy as np #use this for arrays
import os, os.path #using this to count images
import math #Use this to round up numbers
from glob import iglob #Grab files to do stuff with
from PIL import Image #Handle the image stuff
import re # Regex - This for the sorting of filenames
import warnings #this for the DecompressionBombWarning that sometimes appears

#Define some functions to do stuff

def extract_image_one_fps(video_source_path):
    #This function takes the video specified in video_source_path and grabs one frame every second. This came from https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames

    vidcap = cv2.VideoCapture(video_source_path)
    count = 0
    success = True
    while success:
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
      success,image = vidcap.read()
      # There is a funny error that the last frame returns an empty image. I think this a problem with the camera
      # The if statement below checks to see if the image has been read.
      if success:
          ## Stop when last frame is identified
          image_last = cv2.imread("frames/frame{}.png".format(count-1))
          if np.array_equal(image,image_last):
              break

          cv2.imwrite("frames/frame%d.png" % count, image)     # save frame as PNG file
          print("done frame"+format(count))
      count += 1

def remove_files(folder):
    for the_file in os.listdir(path):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def count_images():
    #Short function to count the number of frame images in the frames folder. We use this to work out how many rows the image will have
    img_num = len([name for name in os.listdir('./frames') if os.path.isfile(name)])
    print (image_num)

def numericalSort(value):
    #This is function that helps sort the images into the right order
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def thumbnailer(thumbpath, op_path, grid, thumb_size, background_color):
     #Coroutine to receive image file names and produce thumbnail pages of them laid-out in a grid.
     #This came from https://stackoverflow.com/questions/38421160/combine-multiple-different-images-from-a-directory-into-a-canvas-sized-3x6

    page_num = 0
    page_extent = grid[1]*thumb_size[0], grid[0]*thumb_size[1]
    print(page_extent[0], page_extent[1])
    print(thumb_size[0], thumb_size[1])
    try:
        while True:
            paste_cnt = 0
            new_img = Image.new('RGB', page_extent, background_color)
            #Start at zero and go up in 384's till you get to width of the page
            for y in range(0, page_extent[1], thumb_size[1]):
            #Start at zero and go up in 216's till you get to height of the page
                for x in range(0, page_extent[0], thumb_size[0]):
                    try:
                        filepath = (yield)
                    except GeneratorExit:
                        print('GeneratorExit received')
                        return

                    filename = os.path.basename(filepath)
                    print('{} thumbnail -> ({}, {})'.format(filename, x, y))
                    thumbnail_img = Image.open(filepath)
                    thumbnail_img.thumbnail(thumb_size)
                    new_img.paste(thumbnail_img, (x,y))
                    paste_cnt += 1
                else:
                    continue  # no break, continue outer loop
                break  # break occurred, terminate outer loop

            print('Thumbnail page completed...')
            if paste_cnt:
                page_num += 1
                print('Saving thumbpage{}.jpg'.format(page_num))
                new_img.save(os.path.join(op_path, 'thumbpage{}.jpg'.format(page_num)))
    finally:
        print('Last part...')
        if paste_cnt:
            page_num += 1
            print('Saving thumbpage{}.jpg'.format(page_num))
            new_img.save(os.path.join(op_path, 'thumbpage{}.jpg'.format(page_num)))

#Turn off a warning that appears when the image is looking too big. Called a DecompressionBombWarning
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

# Tell it where the video is. Assumes it's in the same directory as the script
video = 'test.mov'
#Tell it where to put the frames and the final image
path = 'frames/'
#Then the path the save the finsihed thumbnail
op_path = 'output/'
# The following functions deletes any files in the frames folder before we start
# Comment this out if you don't want to risk it.
remove_files(path)
#Run the function that samples the video file. This will drop a png file into the frames folder for every second of video.
extract_image_one_fps(video)

#Now we have the frames we can begin to create the composite image.
# First problem to get over is how to read the image files from the frames folder in the right order as the standard sorting function (look for sorted() below) in Python deosn't do it!
# Found a solution to this at #https://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python
#First thing is to create a variable that splits out the numbers
numbers = re.compile(r'(\d+)')
#Then we hoover up all the images in the frames flder into a list using a custom function called numericalSort to make sure they are in the right order.
npath = [infile for infile in sorted(iglob(os.path.join(path, '*.png')), key=numericalSort)]
#Get some quick stats on what we are wokring withself.
#First, how many images?
num_images = len(npath)
#We can then use that to work out how many rows we'll need. Dawes uses one row for each minute of footage, thats sixty images per row. So we can do a basic divide which we then round up using math.ceil function so that we have full rows.
minutes = math.ceil(len(npath)/60)

#Now we can build the actual image.
#The function I found uses coroutines, I'm not familiar with them but it worked so that's for another day. I did need to tweak it a little for Python3. For example .next and xrange are not supported but it only took a quick google of the error message to sort that.
#Set some paremeters. In this case the number of rows is set with the minutes variable we created above.
coroutine = thumbnailer(path, op_path, (minutes,60), (384,216), 'black')
coroutine.__next__()  # start it

for filepath in npath:
    coroutine.send(filepath)

print('Done making the thumbnails')
coroutine.close()
