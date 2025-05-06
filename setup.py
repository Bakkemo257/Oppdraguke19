import mariadb
from secret import MARIADB

with open('db.sql', 'r') as f:
  sql = f.read()

connection = mariadb.connect(
  user=MARIADB['user'],
  password=MARIADB['password'],
  host=MARIADB['host'],
  port=MARIADB['port']
)

cursor = connection.cursor()

for command in sql.split(';'):
  if command.strip() == '': continue
  cursor.execute(command)

connection.commit()
connection.close()

print('Database set up')