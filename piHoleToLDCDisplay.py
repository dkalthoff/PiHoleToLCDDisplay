import time
import requests
import RPi.GPIO as GPIO
from RPLCD import CharLCD

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23], 
		numbering_mode=GPIO.BOARD)

try:
	while True:
		data_pihole1 = requests.get("http://localhost/admin/api.php").json()
		data_pihole2 = requests.get("http://192.168.1.56/admin/api.php").json()

		totalAdsBlocked = data_pihole1['ads_blocked_today'] + data_pihole2['ads_blocked_today']
		totalPercentageBlocked = (data_pihole1['ads_percentage_today'] + data_pihole2['ads_percentage_today']) / 2
		totalDNSQueries = data_pihole1['dns_queries_today'] + data_pihole2['dns_queries_today']

		lcd.clear()
		lcd.cursor_pos = (0,0)
		lcd.write_string("Queries Blocked")
		lcd.cursor_pos = (1,0)
		lcd.write_string("{:,}".format(totalAdsBlocked) + " ({0:.0f}%)".format(totalPercentageBlocked))
		time.sleep(10)

		lcd.clear()
		lcd.cursor_pos = (0,0)
		lcd.write_string("DNS Queries")
		lcd.cursor_pos = (1,0)
		lcd.write_string(str(totalDNSQueries))
		time.sleep(10)

except KeyboardInterrupt:
	print("Keyboard interrupt")
	lcd.clear()
finally:
	print("GPIO clean up")
	lcd.cursor_pos = (0,0)
	lcd.write_string("script")
	lcd.cursor_pos = (1,0)
	lcd.write_string("terminated")
	GPIO.cleanup()
