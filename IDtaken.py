#!/usr/bin/python3
#written by antymijaljevic@gmail.com

import json
import os
import time
from datetime import datetime
import pygsheets


#loading json db, text file and connecting with google spreadsheet
emtDb = json.load(open('/Users/amijaljevic/Desktop/emtDb.json'))
gc = pygsheets.authorize(service_file='/Users/amijaljevic/Desktop/creds.json')
#emtDb = json.load(open('/home/amijaljevic/Desktop/coding/my_projects_python/IDtaken/emtDb.json'))
#gc = pygsheets.authorize(service_file='/home/amijaljevic/Desktop/creds.json')
IDtaken = gc.open('IDtaken.py') #spreadsheet selected
assets = IDtaken[1] #first sheet selected #inventory B
with open("counter.txt", "r") as fileCounterR:
	counter = int(fileCounterR.read())

def badge_collector():
	#welcome text
	os.system('clear')
	print('''

	#### ########  ########    ###    ##    ## ######## ##    ## 
	 ##  ##     ##    ##      ## ##   ##   ##  ##       ###   ## 
	 ##  ##     ##    ##     ##   ##  ##  ##   ##       ####  ## 
	 ##  ##     ##    ##    ##     ## #####    ######   ## ## ## 
	 ##  ##     ##    ##    ######### ##  ##   ##       ##  #### 
	 ##  ##     ##    ##    ##     ## ##   ##  ##       ##   ### 
	#### ########     ##    ##     ## ##    ## ######## ##    ## 

	--because we want you to scan taken assets before you leave--


	"exit" ~ to quit
	"list" ~ to list badge database
	''')

	#collecting badge numbers and giving access to tech
	while True:
	    badgeNum = input('Please scan you badge: ')
	    if badgeNum == 'exit':
	    	print('Program terminated! Saving database... DONE')
	    	exit(0)
	    elif badgeNum == 'list':
	    	print('\n', emtDb.items(),'\n')
	    elif badgeNum in emtDb.keys():
	    	print('\nWelcome EMT Technician: ', emtDb[badgeNum])
	    	time.sleep(2)
	    	spreadsheet_write()
	    elif badgeNum is not emtDb.keys():
	    	print("\nEMT technician isn't in database.\n")
	    	emtDb[badgeNum] = input("\nPlease enter technician name: ")
	    	emtDb.update(emtDb)
	    	with open("/Users/amijaljevic/Desktop/emtDb.json", "w") as emtDatabase:
	    		json.dump(emtDb, emtDatabase)
	    	print("\nEMT technician is now added into database.")
	    	time.sleep(2)
	    	spreadsheet_write()

def spreadsheet_write():
	#writing scanned assets into spreadsheet
	global counter

	while True:
		os.system('clear')
		userInput = input("Please scan the assets that you want to take, scan badge again to finish: ")
		if counter == 1000:
			counter = 2
		elif userInput in emtDb.keys():
			assets.update_value('A' + str(counter), "Taken by: " + str(emtDb[userInput]) + '\n' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
			counter += 1
			with open("counter.txt", "w") as fileCounterW:
				fileCounterW.write(str(counter))
			print("\nAssets marked as taken! Thank you!")
			time.sleep(2)
			badge_collector()
		else:
			assets.update_value('A' + str(counter), userInput)
			counter += 1
			with open("counter.txt", "w") as fileCounterW:
				fileCounterW.write(str(counter))

badge_collector()