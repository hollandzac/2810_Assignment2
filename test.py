import openpyxl as xl
import sqlite3 as sql

connection = sql.connect("blah.db")
cursor = connection.cursor()
insp = xl.load_workbook("test.xlsx")['Sheet1']

cursor.execute("""CREATE TABLE test(
a VARCHAR(10),
b VARCHAR(10),
c INTEGER(5),
d VARCHAR(10)
)""")

insert = """INSERT INTO test VALUES ('{}','{}','{}','{}')"""
for row in insp.iter_rows(min_row=2):
    a =[row[i].value for i in range(4)]
    command = insert.format(*a)
    print(command)
    cursor.execute(command)

connection.commit()
connection.close()
