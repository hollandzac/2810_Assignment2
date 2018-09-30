import numpy
import sqlite3 as sql
import matplotlib

connection = sql.connect("compliance.db")
cursor = connection.cursor()
# query = """SELECT strftime('%Y-%m')
# FROM inspections"""


query = """SELECT COUNT(violations.serial_number), facility_zip,
strftime('%m-%Y', activity_date)
FROM violations, inspections
WHERE inspections.serial_number=violations.serial_number
GROUP BY facility_zip, strftime('%m-%Y',activity_date)
ORDER BY facility_zip, strftime('%Y',activity_date), strftime('%m',activity_date), COUNT(violations.serial_number) DESC
"""

cursor.execute(query)
result = cursor.fetchall()

for i in result:
    print(i[0],i[1],i[2])
