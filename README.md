# Oppdraguke19
# 🎫 Flask Ticket System

Et enkelt webbasert ticketsystem laget med Flask og HTML. Systemet tillater brukere å sende inn tickets som lagres i databasen. Ansatte kan logge inn for å se og endre status på tickets, legge til nye brukere, og administratorer kan slette tickets.

## 🧰 Teknologi

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS
- **Database**: Mariadb
- **Autentisering**: Flask-Login

## 🚀 Kom i gang

### 1. Klon repoet

```bash
git clone https://github.com/Bakkemo257/Oppdraguke19.git
cd ticket-system

python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt

python main.py #for å kjøre kode
```
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

Når du har skrevet det du trenger skal du runne `secret.py` som lager alle table