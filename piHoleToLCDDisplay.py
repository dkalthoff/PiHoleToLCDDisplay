#!/usr/bin/env python3

import time
from datetime import date
import requests
import RPi.GPIO as GPIO
from RPLCD import CharLCD

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23], 
		numbering_mode=GPIO.BOARD)


def writeToLCD( message, lineNumber, sleepSeconds ):
	if ( lineNumber == 1 ):
		lcd.clear()
	else:
		lcd.cursor_pos = (1,0)

	lcd.write_string(message)
	time.sleep(sleepSeconds)

	return;

try:
	while True:
		data_pihole1 = requests.get("http://localhost/admin/api.php").json()
		data_pihole2 = requests.get("http://192.168.1.4/admin/api.php").json()

		totalAdsBlocked = data_pihole1['ads_blocked_today'] + data_pihole2['ads_blocked_today']
		totalDNSQueries = data_pihole1['dns_queries_today'] + data_pihole2['dns_queries_today']
		totalDNSQueriesCached = data_pihole1['queries_cached'] + data_pihole2['queries_cached']

		totalPercentageBlocked = (totalAdsBlocked / totalDNSQueries) * 100
		totalPercentageCached = (totalDNSQueriesCached / totalDNSQueries) * 100

		fileLastRefreshedDatePiHole1 = date.fromtimestamp(data_pihole1['gravity_last_updated']['absolute'])
		fileLastRefreshedDatePiHole2 = date.fromtimestamp(data_pihole2['gravity_last_updated']['absolute'])

		writeToLCD("Blocked: ({0:.0f}%)".format(totalPercentageBlocked), 1, 0)
		writeToLCD("{:,}/{:,}".format(totalAdsBlocked, totalDNSQueries), 2, 5)

		writeToLCD("Cached: ({0:.0f}%)".format(totalPercentageCached), 1, 0)
		writeToLCD("{:,}/{:,}".format(totalDNSQueriesCached, totalDNSQueries), 2, 5)

		writeToLCD("Pi-Hole1 BlkList", 1, 0)
		writeToLCD("Update: " + fileLastRefreshedDatePiHole1.strftime("%m/%d/%y"), 2, 3)

		writeToLCD("Pi-Hole2 BlkList", 1, 0)
		writeToLCD("Update: " + fileLastRefreshedDatePiHole2.strftime("%m/%d/%y"), 2, 3)

except KeyboardInterrupt:
	print("Keyboard interrupt")
	lcd.clear()
finally:
	print("GPIO clean up")
	lcd.close(clear=True)
