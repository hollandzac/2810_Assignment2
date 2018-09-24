import sqlite3 as sql

connection = sql.connect("compliance.db")
cursor = connection.cursor()

query = """SELECT DISTINCT facility_name FROM inspections, violations WHERE violations.serial_number=inspections.serial_number"""
cursor.execute(query)

result = sorted(cursor.fetchall())

for r in result:
    print(r[0])


cursor.execute("""CREATE TABLE IF NOT EXISTS Previous_Violations(
name VARCHAR(30),
address VARCHAR(50),
zipcode VARCHAR(15),
city VARCHAR(50)
)""")

query = """INSERT INTO Previous_Violations SELECT facility_name, facility_address, facility_zip, facility_city
FROM inspections, violations
WHERE violations.serial_number=inspections.serial_number GROUP BY facility_name"""

cursor.execute(query)

query = """SELECT COUNT(violations.serial_number), facility_name FROM inspections, violations WHERE violations.serial_number=inspections.serial_number 
GROUP BY facility_name ORDER BY COUNT(violations.serial_number) DESC"""

cursor.execute(query)

result = cursor.fetchall()

for t in result:
	print(t[1], t[0])
print(len(result))


connection.commit()
connection.close()
