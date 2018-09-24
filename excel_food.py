import openpyxl as xl
from openpyxl import Workbook
import sqlite3 as sql

connection = sql.connect("compliance.db")
cursor = connection.cursor()

wb = Workbook()

ws1 = wb.active

ws1.title = 'Violation_Types'

print(wb.sheetnames)

