
import os
import glob
import time
   
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

dt_start = time.strftime("%y%m%d_%H%M", time.gmtime())
fr = open('results'+ dt_start + '.csv', 'w')

while True:	
	fw = open("/var/www/temperature/index.html", 'w')
	t = read_temp()
	date = time.strftime("%a; %d %b %Y %H:%M:%S;", time.gmtime())
	print date
	print t
	tf = float(t) / 1000
	fw.write('<html><body> <p>' + date + ' Bedroom temperature is ' + str(tf) + 'C')
	fw.write('</p> </body> </html>')
	fw.close()
	fr.write(date)
	fr.write(t)	
	fr.flush()
	time.sleep(1800)
