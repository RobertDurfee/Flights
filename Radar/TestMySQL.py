import mysql.connector

cxn = mysql.connector.connect(host='146.148.73.209', user='root', db='FlightsDatabase')
cursor = cxn.cursor()

query = '''
  SHOW COLUMNS FROM `Radar`;
  '''

cursor.execute(query)

result = cursor.fetchall()
print(result)

cursor.close()
cxn.close()
