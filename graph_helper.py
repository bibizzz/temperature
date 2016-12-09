import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sqlite3

#import datetime
from datetime import datetime #, date, time
from matplotlib.dates import AutoDateFormatter, AutoDateLocator, YearLocator, MonthLocator, DateFormatter, DayLocator, HourLocator
import random


def import_from_csv(filename):
    dt = []
    temp = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            if len(row) == 3:
                print(row)
                dt.append(datetime.strptime(row[1], " %d %b %Y %H:%M:%S"))
                temp.append(float(row[2])/1000)
    return dt, temp

def import_from_sql(db_name):
    dt = []
    temp = []
    conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur =conn.cursor()
    for row in cur.execute("select ts, temperature from weatherstation"):
        dt.append(row[0])
        temp.append(row[1])
    cur.close()
    conn.close()
    return dt, temp


def save_graph(dt, temp, filename, type = "normal"):

    days = DayLocator()   # every day
    hours = HourLocator(range(0,24,6))  # every 6 hour
    daysFmt = DateFormatter('%a %d/%m')
    hoursFmt = DateFormatter('%Hh')
    auto = AutoDateLocator()
    auto_f = AutoDateFormatter(auto)

    fig, ax = plt.subplots()
    ax.plot_date(dt, temp, '-')

    #ax.set_axis(auto)
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)
    ax.xaxis.set_minor_locator(hours)
    #ax.xaxis.set_minor_formatter(hoursFmt)
    ax.autoscale_view()
    ax.set_ylabel('Temperature (C)')
    ax.grid(True, which='major', linestyle='--')
    ax.grid(True, which='minor')
    plt.savefig(filename)

#dt, temp = import_from_csv("results.csv")
#save_graph(dt, temp, "week_daysformat.png")
dt, temp = import_from_sql("/home/pi/temperature/weasta2.sq3")
save_graph(dt, temp, "/var/www/temperature/days.png")
