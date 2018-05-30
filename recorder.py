"""
This version counts the number of frames in each minute interval and then creates one minute blocks
according to the fps calculated of the one minute block

To run the code
$ python3 recorder.py name_of_file 'url' minutes
$ python3 recorder.py doggie 'http://173.165.152.131/axis-cgi/mjpg/video.cgi' 5

"""
import datetime

import cv2
import urllib
import numpy as np
import os

import time

import urllib
import requests

import re

import sys

import math

from collections import Counter

cam_name = str(sys.argv[1])
ip = str(sys.argv[2])
duration = float(sys.argv[3])

urlmj = ip

#-------------------Setting the name of the output video file--------------------"

date_time = (str(datetime.datetime.now())).split()

date = re.findall('\d+', date_time[0])
date = (''.join(date))

time = re.findall('\d+', date_time[1])
time = (''.join(time))[:6]
file_name = cam_name + '_' + date + '_' + time

#-------------------Setting the name of the output video file--------------------"

'''

Part I: Write the frames of the stream into an avi file 

'''

urlmj = ip

cap = cv2.VideoCapture(urlmj)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

file_name_avi = file_name + '.avi'
out = cv2.VideoWriter(file_name_avi,fourcc,30,(int(cap.get(3)),int(cap.get(4))))

list_n_frames = [] #each entry contains the number of frames per minute
n_frames = 0
total_frames = 0

t_start = datetime.datetime.now()
t_end = t_start + datetime.timedelta(minutes = duration)

u_start = t_start

while True:
	ret, frame = cap.read()

	out.write(frame)
	cv2.imshow('frame',frame)
	
	n_frames += 1
	total_frames += 1

	if (datetime.datetime.now() - u_start).total_seconds() >= 60.0:
		u_start = datetime.datetime.now()
		list_n_frames.append(n_frames)
		n_frames = 0

	if datetime.datetime.now() >= t_end:
		break

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

if n_frames > 0:
	list_n_frames.append(n_frames)
	n_frames = 0


'''
Part II: Write One Minute Videos

Get one minute videos according to the different number of frames per minute
because frames per minute is different as it depends on the network

'''

index = 1

file_name_mp4 = file_name + '.mp4'

cap_1 = cv2.VideoCapture(file_name_avi)

files = []

for i in list_n_frames:
	
	file_name_temp = str(index) + '_' + file_name_avi
	
	files.append(file_name_temp)

	index += 1

	fps_i = i/60.0	#count the fps of this one minute block

	out_i = cv2.VideoWriter(file_name_temp,fourcc,fps_i,(int(cap_1.get(3)),int(cap_1.get(4))))

	for j in range(i):
		ret, frame = cap_1.read()

		if ret == False:
			break

		out_i.write(frame)
	out_i.release()

cap_1.release()
cv2.destroyAllWindows()


'''

Part III: Combine videos 

Use ffmpeg to combine the videos

Video quality might suffer

'''

cmd = 'ffmpeg -i "concat:'

for i in files:
	cmd = cmd + i + '|'

cmd = cmd[:-1]
cmd = cmd + '" -c copy post_' + file_name_avi

os.system(cmd) 






