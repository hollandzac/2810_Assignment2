import numpy
import sqlite3 as sql
import matplotlib.pyplot as plt
import datetime
from operator import itemgetter

connection = sql.connect("compliance.db")
cursor = connection.cursor()

postcode_total_viol = dict()
month_total_viol = dict()




query = """SELECT COUNT(violations.serial_number), facility_zip, strftime('%m-%Y', activity_date)
FROM violations, inspections
WHERE violations.serial_number=inspections.serial_number
GROUP BY facility_zip, strftime('%m',activity_date)
ORDER BY  facility_zip , strftime('%Y-%m', activity_date) DESC
"""

cursor.execute(query)
result = cursor.fetchall()
lastzip = 0
minvalue = 0
difference = 0



for i in result:
    postcode_total_viol[i[1]] = postcode_total_viol.get(i[1], 0) + i[0]
    month_total_viol[i[2]] = month_total_viol.get(i[2], [])
    month_total_viol[i[2]].append(i[0])
    if i[1] == lastzip:
        if difference < (abs(i[0] - minvalue)):
            difference = (abs(i[0] - minvalue))
            postdif = i[1]
        elif minvalue > i[0]:
            minvalue = i[0]
    lastzip = i[1]

monthavg = list()
for key, value in month_total_viol.items():
    monthavg.append([key,sum(value)/len(value)])



    #print(i[0], i[1], i[2])

most_violations = max(postcode_total_viol, key=postcode_total_viol.get)
postcode_viol = list()
postcode_dif_viol = list()

for j in result:
    if j[1] == most_violations:
        postcode_viol.append((j[2],j[0]))
    if postdif == j[1]:
        postcode_dif_viol.append((j[2],j[0]))

for date in monthavg:
    date[0] = date[0][3:] + '-' + date[0][:2]
monthavg = sorted(monthavg)

postcode_viol.reverse()
postcode_dif_viol.reverse()

x_value =[x[0] for x in postcode_viol]
y_value = [y[1] for y in postcode_viol]
plt.xticks(range(len(y_value)), x_value)
plt.plot(y_value)
plt.title(('Violations per month for zip code {} which has the highest total violations').format(most_violations))
plt.xlabel('Date')
plt.ylabel('Number of violations')
plt.show()

x_value = [x[0] for x in postcode_dif_viol]
y_value = [y[1] for y in postcode_dif_viol]
plt.xticks(range(len(y_value)), x_value)
plt.plot(y_value)
plt.title(('Violations per month for zip code {} which has the greatest variance').format(postdif))
plt.xlabel('Date')
plt.ylabel('Number of violations')
plt.show()


x_value =[x[0].replace('20','') for x in monthavg]
y_value = [y[1] for y in monthavg]
plt.xticks(range(len(y_value)), x_value)
plt.plot(y_value)
plt.title('Total violations per month for all zip codes')
plt.xlabel('Date')
plt.ylabel('Number of violations')
plt.show()

query = """SELECT COUNT(violations.serial_number), strftime('%Y-%m', activity_date), facility_name
FROM violations, inspections
WHERE violations.serial_number=inspections.serial_number AND (facility_name LIKE '%BURGER KING%' OR facility_name LIKE '%MCDONALDS%')
GROUP BY facility_name, strftime('%m',activity_date)
ORDER BY  facility_name , strftime('%Y-%m', activity_date) DESC
"""
cursor.execute(query)
result = cursor.fetchall()


restraunt = dict()
x = list()
y = list()
for item in result:
    restraunt[item[1]] = restraunt.get(item[1], 0) + item[0]
for key, value in restraunt.items():
    x.append(key)
    y.append(value)
plt.xticks(range(len(y_value)), x_value)
plt.plot(y_value)
plt.title('Total violations per month for all burger kings and mcdonalds')
plt.xlabel('Date')
plt.ylabel('Number of violations')
plt.show()
