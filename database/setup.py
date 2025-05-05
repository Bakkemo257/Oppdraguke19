import mariadb

with open('database/db.sql', 'r') as f:
  sql = f.read()

print(sql)