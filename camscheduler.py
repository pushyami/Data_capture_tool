"""

	Version 2.2
	
	IP Camera Recording Scheduler
	
	IPSched Class

	Commands:
		- help: retrieve list of commands
		- exit: close the scheduler
		- active: Enters interactive mode
			Entered sequentially: camera name, clientID, clientSecret, ip address, date, time, duration
		- File input: file [file name]



	To be implemented:
		- Search tool: search [ retrieve: [ ip | video path ] ] [ with: [ cameraID | source | country | state | city | ip ] ]

"""

import threading
from datetime import datetime
from datetime import timedelta
import cv2
import numpy as np
import time
import requests
import re
import subprocess as s
import os, sys

class IPSched:

	def scheduler(self, month, day, year, hour, minute, duration):
    		#cast datetimes to ints
		month = int(month)
		day = int(day)
		year = int(year)
		hour = int(hour)
		minute = int(minute)

		#create datetime object of execution date
		exec_datetime = datetime(year, month, day, hour, minute)

                if (exec_datetime < datetime.now()):
                    return
               
                curr_datetime = datetime.now()
                
                while (exec_datetime > curr_datetime):
                        curr_datetime = datetime.now()
		inst = IPSched()
                inst.cap_video(duration, month, day, year, hour, minute)			
	#------------------------end of scheduler


	#calls the video capture script here
	#Thanks to ZK for this
	#-------------------------
	def cap_video(self, duration, month, day, year, hour, minute):		
		cam_name = 'webcam1'
		duration = float(duration)

		cap = cv2.VideoCapture(0)

		frame_width = int(cap.get(3))
		frame_height = int(cap.get(4))

		#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
		fourcc = cv2.cv.CV_FOURCC(*'XVID')

		#-------------------Setting the name of the output video file--------------------"
                date = str(month) + str(day) + str(year)
                time = str(hour) + str(minute)
		file_name = cam_name + '_' + date + '_' + time + '.avi'
		#-------------------Setting the name of the output video file--------------------"

		out = cv2.VideoWriter(file_name,fourcc,6.4,(int(cap.get(3)),int(cap.get(4))))
		
		#set the end time, sec = duration * 15 is experimental, should be changed
		sec = duration * 15.0

		t_start = datetime.now()
		t_end = t_start + timedelta(minutes = duration, seconds = sec)
		#t_end = t_start + datetime.timedelta(minutes = duration)

		#record before t_end
		while True:
			ret, frame = cap.read()

			out.write(frame)
			#cv2.imshow('frame',frame)
			
			if datetime.now() >= t_end:
				break

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		cap.release()
		out.release()
		cv2.destroyAllWindows()
	#-------------------------end of cap_video

	#Main start of program
	#Runs command prompt and spawns scheduler threads
	#------------------------
	def driver(self):
		#initial dummy message, needed for parsing 0th element
		user_input = 'Usage'
		usage = """
			Commands:
				- help: retrieve list of commands
				- exit: close the scheduler
				- active: Enters interactive mode
					Entered sequentially: camera name, clientID, clientSecret, ip address, date, time, duration
				- File input: file [file name]
		"""
		print("Enter help for for list of commands")

		#take input until user inputs "exit"
		while (True):
			#get input and split into arguments
			user_input = raw_input("Schedule > ").split(' ')

			if (user_input[0] == 'help'):
				print(usage)
				
			#file mode
			if (user_input[0] == 'file'):
				with open(user_input[1]) as f:
					orig_user = user_input
					user_input = ''
					count = 0
					#parses file and executes
					for line in f:
						count += 1
						if (count % 3 == 0):
							user_input += line
							user_input = user_input.split('\n')
							 
                                                        #Retrieve date to execute capture
                                                        month = user_input[0][0:2]
                                                        day = user_input[0][2:4]
                                                        year = user_input[0][4:]

                                                        #formats year
                                                        #ex: 18 goes to 2018
                                                        if (len(year) != 4):
                                                                year = '20' + year
                    
                                                        #Retrieves time to execute capture (in military time)
                                                        hour = user_input[1][1:3]
                                                        minute = user_input[1][3:]

                                                        #duration of capture in minutes
                                                        duration = user_input[2][1:]
                                                        print(month + day + year + ' ' + hour + minute + ' ' + duration)
							new_thread = threading.Thread(target=self.scheduler, args=(month, day, year, hour, minute, duration))
							new_thread.start()
							user_input = ''
						else:
							user_input += line + ' '
					user_input = orig_user	

			#exit on command
			if (user_input[0] == 'exit'):
				sys.exit()	

			#interactive mode
			if (user_input[0] == 'active'):
				user_date = raw_input("Date: ")
				user_time = raw_input("Time: ")
				duration = raw_input("Duration: ")
				user_input = user_date + ' ' + user_time + ' ' + duration
				user_input = user_input.split(' ')
                                
                                #Retrieve date to execute capture
                                month = user_input[0][0:2]
                                day = user_input[0][2:4]
                                year = user_input[0][4:]

                                #formats year
                                #ex: 18 goes to 2018
                                if (len(year) != 4):
                                        year = '20' + year

                                #Retrieves time to execute capture (in military time)
                                hour = user_input[1][0:2]
                                minute = user_input[1][2:]

                                #duration of capture in minutes
                                duration = user_input[2]
 
				new_thread = threading.Thread(target=self.scheduler, args=(month, day, year, hour, minute, duration))
				new_thread.start()

		sys.exit()
	#------------------------end of driver
#------------------------end of IPSched class

init = IPSched()
init.driver()
