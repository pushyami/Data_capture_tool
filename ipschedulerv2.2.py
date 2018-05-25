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

	def scheduler(*user_input):
		#Retrieve username, clientID, clientSecret, and camera ip address from arguments
		user = user_input[1]
		clientID = user_input[2]
		clientSecret = user_input[3]
		user_ip = user_input[4]

		#Retrieve date to execute capture
		month = user_input[5][0:2]
		day = user_input[5][2:4]
		year = user_input[5][4:]

		#formats year
		#ex: 18 goes to 2018
		if (len(year) != 4):
			year = '20' + year

		#Retrieves time to execute capture (in military time)
		hour = user_input[6][0:2]
		minute = user_input[6][2:]

		#duration of capture in minutes
		duration = user_input[7]

		#cast datetimes to ints
		month = int(month)
		day = int(day)
		year = int(year)
		hour = int(hour)
		minute = int(minute)

		#create datetime object of execution date
		exec_datetime = datetime(year, month, day, hour, minute)

		#creates current datetime object
		curr_datetime = datetime.now()

		#checks for valid execution date (also handled in part by datetime object value bounds)
		if (exec_datetime < curr_datetime):
			exec_file = open('camera_exec_log.out', 'a')
			exec_file.write('Date or time has elapsed already' + str(exec_datetime) + '\n')
			exec_file.write('-----------------------------------------------------------------\n')
			exec_file.close()
			return
			
		#write 'command made' log to master file as
		"""
		Current date and time
		Capture will be set for:
		month/day/year at hour:minute for duration minutes
		On camera username, password, ip
		Process id: pid
		"""
		exec_file = open('camera_exec_log.out', 'a')
		curr_datetime = datetime.now()
		exec_file.write(str(curr_datetime) + '\n')
		exec_file.write('Capture will be set for: ')
		exec_file.write(str(month) + '/' + str(day) + '/' + str(year) + ' at ' + str(hour) + ':' + str(minute) + ' for ' + str(duration) + ' minutes.\n')
		exec_file.write('On camera ' + user + ', ' + user_ip + '\n')
		exec_file.write('Process id: ' + str(os.getpid()) + '\n')
		#separator for easy reading in log file
		exec_file.write('-----------------------------------------------------------------\n')
		exec_file.close()

		#main piece, 'sleeps' the process until execution time
		while (exec_datetime > curr_datetime):
			#updates current datetime
			curr_datetime = datetime.now()

		#writes log to master file as
		"""
		Current date and time
		Executing duration minutes capture on stream ip, username, password
		"""
		exec_file = open('camera_exec_log.out', 'a')
		curr_datetime = datetime.now()

		#Execution message with detail
		exec_message = 'Executing ' + duration + ' minute capture on stream ' + user_ip + ', ' + user + '\n'

		#gives desktop notification on execution
		s.call(["notify-send", "-i", "image-loading", exec_message])

		#write log to file
		exec_file.write(str(curr_datetime) + '\n')
		exec_file.write(exec_message)
		exec_file.write('-----------------------------------------------------------------\n')
		exec_file.close()

		videopath = IPSched.get_videopath(clientID, clientSecret, user_ip)
	
		if (videopath == 'None'):
			return
	
		IPSched.cap_video(user, user_ip, videopath, duration)			
	#------------------------end of scheduler




	#Automates video path retrieval (to complete stream URL) given IP
	#------------------------
	def get_videopath(clientID, clientSecret, user_ip):		
		result = {}

		endpoint = 'https://cam2-api.herokuapp.com/auth/' + '?clientID=' + clientID + '&clientSecret=' + clientSecret

		response = requests.get(endpoint)

		result = response.json()

		endpoint = 'https://cam2-api.herokuapp.com/cameras/search?type=ip&is_active_video=true'

		headers = {"Authorization":"Bearer " + result["token"]}

		response = requests.get(endpoint, headers=headers)

		result = response.json()

		videopath = 'None'
		
		for ips in result:
			if (ips['retrieval']['ip'] == user_ip):
				videopath = ips['retrieval']['video_path']
				break
		
		if (videopath == 'None'):
			exec_file = open('camera_exec_log.out', 'a')
			exec_file.write(str(datetime.now()) + '\nVideo path not found with ip ' + str(user_ip) + '\n')
			exec_file.write('-----------------------------------------------------------------\n')
			exec_file.close()
		
		return videopath	
	#-------------------------end of get_videopath
	

	

	#calls the video capture script here
	#-------------------------
	def cap_video(user, user_ip, videopath, duration):		
		cam_name = user
		ip = 'http://' + user_ip + videopath
		duration = float(duration)
		
		urlmj = ip

		cap = cv2.VideoCapture(urlmj)

		frame_width = int(cap.get(3))
		frame_height = int(cap.get(4))

		#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
		fourcc = cv2.VideoWriter_fourcc(*'XVID')

		#-------------------Setting the name of the output video file--------------------"

		date_time = (str(datetime.now())).split()

		date = re.findall('\d+', date_time[0])
		date = (''.join(date))

		time = re.findall('\d+', date_time[1])
		time = (''.join(time))[:6]
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
			user_input = input("Schedule > ").split(' ')

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
						if (count % 7 == 0):
							user_input += line
							user_input = user_input.split('\n')
							print(str(user_input))
							user_input = map(str.strip, user_input)
							new_thread = threading.Thread(target=self.scheduler, args=(user_input))
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
				camera_name = input("Camera name: ")
				clientID = input("Client ID: ")
				clientSecret = input("Client Secret: ")
				ip_address = input("IP Address: ")
				user_date = input("Date: ")
				user_time = input("Time: ")
				duration = input("Duration: ")
				user_input = camera_name + ' ' + clientID + ' ' + clientSecret + ' ' + ip_address + ' ' + user_date + ' ' + user_time + ' ' + duration
				user_input = user_input.split(' ')
				new_thread = threading.Thread(target=self.scheduler, args=(user_input))
				new_thread.start()

		sys.exit()
	#------------------------end of driver

init = IPSched()
init.driver()
