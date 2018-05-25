Version 2.1 of IP Scheduler

Schedules recording sessions of IP cameras

Dependencies:
	- opencv
	- venv
	- requests
	- numpy

Usage:
1. Run in venv by navigating to the home directory and executing **source venv/bin/activate**
2. Navigate to scheduler's directory
3. Run scheduler using **python ipscheduler2.1.pi**
4. Run in file mode using **file [ file name ]**
	- File format:
		camera name - Name of device, alternatively used for file naming (goes at the front of every output file name)
		client ID
		client secret
		ip address - IP address of designated device
		date - as a 6 digit number, ex: 052518 for May 25th, 2018
		time - as a 4 digit number in military time, ex: 1445 for 2:45PM
		duration - in minutes, use a float for seconds, ex: 1.5 for 1 minute and 30 seconds of footage

5. Run in interactive mode using **active**
	- Creates input prompt that follows same format as files
7. Enter help to get list of commands
8. Enter exit to close program (WARNING: KILLS ACTIVE THREADS/FUTURE EXECUTIONS)


Terminal must be left **OPEN** until all threads finish execution to get capture, i.e. threads are not background processes, they are attached to the terminal session.


