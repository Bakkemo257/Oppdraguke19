# Oppdraguke19

## secret.py

Lag en fil kalt `secret.py` i prosjektets hovedmappe.

Den skal ha dette innholdet:

```py
MARIADB = {
  'user': '<mariadb-bruker>',
  'password': '<passord>',
  'host': 'localhost',          # Eller host
  'port': 3306,                 # By default
  'database': 'ticket_system',  # Hvis du skal endre dette, må det også endres i db.sql.
}

SECRET_KEY = '<secret key>'     # En helt tilfeldig string. Burde lages med noe som os.urandom.
```