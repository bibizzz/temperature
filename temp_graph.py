
import os
import glob
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator, HourLocator
import random

dt = []
temp = []

days = DayLocator()   # every day
hours = HourLocator(range(0,24,6))  # every 3hour
daysFmt = DateFormatter('%a %d/%m')
hoursFmt = DateFormatter('%Hh')
   
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
     
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
     
def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines
 
def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_string

#static = '<html><body><h1>It works OUUUTTT!</h1> <p>This is the default web page for this server.</p> <p>The web server software is running but no content has been added, yet.</p> </body></html>' 

dt_start = datetime.now()
#datetime.strftime("%y%m%d_%H%M", time.now())
#dt_start = datetime.now()
fr = open('results'+ dt_start.strftime("%y%m%d_%H%M") + '.csv', 'w')

while True:	
	fw = open("/var/www/temperature/index.html", 'w')
	t = read_temp()
	date = datetime.now()
	date_s= date.strftime("%a; %d %b %Y %H:%M:%S;")
	print date_s
	print t
	tf = float(t) / 1000
	dt.append(datetime.now())
	temp.append(tf)
	#create plot now
	fig, ax = plt.subplots()
	ax.plot_date(dt, temp, '-')
	ax.xaxis.set_major_locator(days)
	ax.xaxis.set_major_formatter(daysFmt)
	ax.xaxis.set_minor_locator(hours)
	#ax.xaxis.set_minor_formatter(hoursFmt)
	ax.autoscale_view()
	ax.set_ylabel('Temperature (C)')
	ax.grid(True, which='major', linestyle='--')
	ax.grid(True, which='minor')
	plt.savefig('/var/www/temperature/days.png')
		
	fw.write('<html><body> <p>' + date_s + ' Bedroom temperature is ' + str(tf) + 'C')
	fw.write('</p> <p> <img SRC="days.png">')
	fw.write('</p> </body> </html>')
	fw.close()
	fr.write(date_s)
	fr.write(t)	
	fr.flush()
	time.sleep(600)
