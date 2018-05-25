Version 2.1 of IP Scheduler

Schedules recording sessions of IP cameras

Dependencies:
- opencv
- venv
- requests
- numpy

Usage:
- Run in venv by navigating to the home directory and executing **source venv/bin/activate**
- Navigate to scheduler's directory
- Run scheduler using **python ipschedulerv2.1.pi**
- Run in file mode using **file [ file name ]**
	* File format:

			camera name - Name of device, alternatively used for file naming (goes at the front of every output file name)
		
			client ID
		
			client secret
		
			ip address - Needed to retrieve corresponding video path and create URL
		
			date - as a 6 digit number, ex: 052518 for May 25th, 2018
		
			time - as a 4 digit number in military time, ex: 1445 for 2:45PM
		
			duration - in minutes, use a float for seconds, ex: 1.5 for 1 minute and 30 seconds of footage
	
			Ex:
			dog_cam
			*****e03eba853ea97f907112fbeb1bfacad823c3759d52ca71418eb75ff3b3a7ab009c9a5682bb4c4f10a**********
			*****d487f83782439ad5c5701aef98d99c0690414915b15d5bb6423dd380**********
			173.165.152.131
			052518
			1411
			0.5	


- Run in interactive mode using **active**
		* Creates input prompt that follows same format as files

- Enter help to get list of commands
	
- Enter exit to close program (WARNING: KILLS ACTIVE THREADS/FUTURE EXECUTIONS)


Terminal must be left **OPEN** until all threads finish execution to get capture, i.e. threads are not background processes, they are attached to the terminal session.

To do:
	
	- Modularize
	
	- Possible dependency install script
	
	- Active mode input history (active mode is very tedious)
	
	- Search tool, will not execute a scheduler itself but will find list of IPs corresponding to search inputs: source, country, state, city, etc.
