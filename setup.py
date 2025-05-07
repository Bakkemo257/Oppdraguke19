import mariadb
from werkzeug.security import generate_password_hash
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

# Add admin account
passwd = input('Password for the admin account >> ')
hash = generate_password_hash(passwd).encode('utf8')

cursor.execute('insert into clients (email, name, hash, admin) values (\'admin@127.0.0.1\', \'Administrator\', ?, true)', (hash,))

print(f"""Admin account created
- Email: "admin@127.0.0.1"
- Password: "{passwd}\"""")

connection.commit()
connection.close()

print('Database set up')