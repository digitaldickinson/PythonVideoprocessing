"""
A SCRIPT TO GRAB A VIDEO AND THEN USE OPENCV TO SAMPLE ONE FRAME A SECOND.

"""
import cv2
import numpy as np
import os, os.path #using this to count images
import cv2
import math
from glob import iglob #Grab files to do stuff with
from PIL import Image #Handle the image stuff
import re # This for the sorting of filenames
import warnings #this for the DecompressionBombWarning


#import some libs to work with
def extract_image_one_fps(video_source_path):

    vidcap = cv2.VideoCapture(video_source_path)
    count = 0
    success = True
    while success:
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
      success,image = vidcap.read()

      ## Stop when last frame is identified
      image_last = cv2.imread("frames/frame{}.png".format(count-1))
      if np.array_equal(image,image_last):
          break

      cv2.imwrite("frames/frame%d.png" % count, image)     # save frame as PNG file
      print("done frame"+format(count))
      count += 1

def count_images():
    img_num = len([name for name in os.listdir('./frames') if os.path.isfile(name)])
    print (image_num)

def numericalSort(value):
    #This is function that helps sort the images into the right order
    #https://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def thumbnailer(thumbpath, grid, thumb_size, background_color):
    """ Coroutine to receive image file names and produce thumbnail pages of
        them laid-out in a grid. This came from https://stackoverflow.com/questions/38421160/combine-multiple-different-images-from-a-directory-into-a-canvas-sized-3x6
    """
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

            print('====> thumbnail page completed')
            if paste_cnt:
                page_num += 1
                print('Saving thumbpage{}.jpg'.format(page_num))
                new_img.save(os.path.join(thumbpath, 'thumbpage{}.jpg'.format(page_num)))
    finally:
        print('====> finally')
        if paste_cnt:
            page_num += 1
            print('Saving thumbpage{}.jpg'.format(page_num))
            new_img.save(os.path.join(thumbpath, 'thumbpage{}.jpg'.format(page_num)))

warnings.simplefilter('ignore', Image.DecompressionBombWarning)
video = '120418.mov'
path = 'frames/'
extract_image_one_fps(video)

numbers = re.compile(r'(\d+)')
npath = [infile for infile in sorted(iglob(os.path.join(path, '*.png')), key=numericalSort)]
#How many images?
num_images = len(npath)
print ("We've got "+len(npath)+" frames to work with ")
#How many minutes?
minutes = math.ceil(len(npath)/60)
print ("And "+minutes+" minutes overall")

#The function I found uses coroutines, I'm not familiar with them but I did need to tweak it a little for Python3
coroutine = thumbnailer(path, (minutes,60), (384,216), 'black')
coroutine.__next__()  # start it

for filepath in npath:
    coroutine.send(filepath)

print('====> closing coroutine')
coroutine.close()
