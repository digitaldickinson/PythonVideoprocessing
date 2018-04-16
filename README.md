# PythonVideoprocessing
Inspired by Brendan Dawes cinenmaredux work - http://www.brendandawes.com/projects/cinemaredux 
I wrote this script to take the video from my cheap go-pro knock-off helmet camera and create a cinemaRedux style image that shows 1 image for each second of video organised into rows of 60

The script is a cut and paste job from various sources so may not win any coding awards but it works. I've written a bit about my approach to coding at https://medium.com/@digidickinson/the-giant-cap-approach-to-coding-for-journalists-400a143791bf 

The code is heavily commented including links to the various stackoverflow posts that I used to help make the script

There are a few things to be aware of in the code:
 - It's python 3
 - You'll need to install some libraries like OpenCV. My version of python is from the anaconda install so adding the libs wasn't too hard. 
 - it assumes the video file is in the same folder as the script
 - it also assumes there is a folder called frames in the same folder which is where the raw images are stored and one called output for the final thumbnail
 - ~~it doesn't clean up after itself so there could be lots of images left around if the video file is long!~~
 - it cleans up after itself by deleteing any files in the frames folder before it starts sampling the video.
