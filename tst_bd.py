

import sqlite3
import datetime

def dt_to_sqldate(dt):
    return dt.strftime("%Y-%m-%d")

def dt_to_sqldatetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

now = datetime.datetime.now()

print(dt_to_sqldate(now))
print(dt_to_sqldatetime(now))

def import_from_sql(db_name, days = 7):
    dt = []
    temp = []
    conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur =conn.cursor()
    now = datetime.datetime.now()
    dt_days = datetime.timedelta(days)
    print(now-dt_days)
#    now = datetime.datetime.now()
    print(datetime.datetime(2015,12,07))
#    for row in cur.execute('select ts, temperature from weatherstation where ts >= datetime.datetime(2016,01,01) AND ts <= datetime.datetime(2016,01,01)'):
#    for row in cur.execute("select ts, temperature from weatherstation"):
    for row in cur.execute("""select ts, temperature from weatherstation where ts BETWEEN "2016-01-01" AND %s  """, dt_to_sqldate(now)):
        dt.append(row[0])
        temp.append(row[1])
    cur.close()
    conn.close()
    return dt, temp

dt, temp = import_from_sql("./weasta2.sq3")
print(dt)

cur = con.cursor()
cur.execute("create table test(d date, ts timestamp)")

today = datetime.date.today()
now = datetime.datetime.now()

cur.execute("insert into test(d, ts) values (?, ?)", (today, now))
cur.execute("select d, ts from test")
row = cur.fetchone()
print today, "=>", row[0], type(row[0])
print now, "=>", row[1], type(row[1])

cur.execute('select current_date as "d [date]", current_timestamp as "ts [timestamp]"')
row = cur.fetchone()
print "current_date", row[0], type(row[0])
print "current_timestamp", row[1], type(row[1])

