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
	
duration = sys.argv[1]

cam_name = 'webcam1'
duration = float(duration)

cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

fourcc = cv2.cv.CV_FOURCC(*'XVID')

t_start = datetime.now()
t_end = t_start + timedelta(minutes = duration)

#record before t_end
while True:
        ret, image = cap.read()

        curr = datetime.now()

        curr_name = str(curr.year) + str(curr.month) + str(curr.day) + '_' + str(curr.hour) + str(curr.minute) + str(curr.second) + '_' + str(curr.microsecond)

        cv2.imwrite(cam_name + '_' + curr_name + '.png', image)
        
        if curr >= t_end:
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
