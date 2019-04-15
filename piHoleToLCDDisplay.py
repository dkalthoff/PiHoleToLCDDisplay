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
		data_pihole2 = requests.get("http://192.168.1.56/admin/api.php").json()

		totalAdsBlocked = data_pihole1['ads_blocked_today'] + data_pihole2['ads_blocked_today']
		totalPercentageBlocked = (data_pihole1['ads_percentage_today'] + data_pihole2['ads_percentage_today']) / 2
		totalDNSQueries = data_pihole1['dns_queries_today'] + data_pihole2['dns_queries_today']
		fileLastRefreshedDatePiHole1 = date.fromtimestamp(data_pihole1['gravity_last_updated']['absolute'])
		fileLastRefreshedDatePiHole2 = date.fromtimestamp(data_pihole2['gravity_last_updated']['absolute'])

		writeToLCD("Requests Blocked", 1, 0)
		writeToLCD("{:,}".format(totalAdsBlocked) + " ({0:.0f}%)".format(totalPercentageBlocked), 2, 10)

		writeToLCD("Total Requests", 1, 0)
		writeToLCD(str(totalDNSQueries), 2, 10)

		writeToLCD("Pi-Hole1 BlkList", 1, 0)
		writeToLCD("Update: " + fileLastRefreshedDatePiHole1.strftime("%m/%d/%y"), 2, 5)

		writeToLCD("Pi-Hole2 BlkList", 1, 0)
		writeToLCD("Update: " + fileLastRefreshedDatePiHole2.strftime("%m/%d/%y"), 2, 5)

except KeyboardInterrupt:
	print("Keyboard interrupt")
	lcd.clear()
finally:
	print("GPIO clean up")
	lcd.close(clear=True)
