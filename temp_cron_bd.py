import os
import glob
import time
import sqlite3
import datetime

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
		return temp_c, temp_f


cur =conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS weatherstation(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     place TEXT,
     ts TIMESTAMP,
     temperature FLOAT,
     humidity FLOAT
)
""")

now = datetime.now()
temperature = read_temp()[0]

cur.execute("insert into weatherstation(place, ts, temperature) values (?, ?, ?)",
     ("DG's bedroom", now,temperature))


for row in cur.execute("select place, ts, temperature from weatherstation"):
    print(row[1])

cur.execute("select place, ts, temperature from weatherstation")
row = cur.fetchone()
print "=>", row[0], type(row[0])
print now, "=>", row[1], type(row[1])
print  "=>", row[2], type(row[2])

cur.close()
conn.close()
