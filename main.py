from flask import Flask, render_template, request, redirect, session
from mariadb import connect
# Local file secret.py
from secret import MARIADB, SECRET_KEY
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/")
def ticket():
    return render_template("ticket.html")

@app.route('/login',  methods=["post", "Get"])
def login():
    if request.method == 'POST':
        email = request.form["email"] 
        password = request.form["password"]
    
        connection = connect(
            user=MARIADB['user'],
            password=MARIADB['password'],
            host=MARIADB['host'],
            port=MARIADB['port'],
            database='ticket_system'
        )

        cursor = connection.cursor()
        cursor.execute('select hash from clients where email = ?', (email,))

        client = cursor.fetchone()

        if not client:
            return redirect("/login")

        if not check_password_hash(client[0], password):
            return redirect("/login")

        # Set session token
        session['email'] = email

        return redirect('/ansatt')

    if request.method =="GET":
        return render_template("login.html")

@app.route("/ansatt")
def ansatt():
    connection = connect(
        user=MARIADB['user'],
        password=MARIADB['password'],
        host=MARIADB['host'],
        port=MARIADB['port'],
        database='ticket_system'
    )

    cursor = connection.cursor()

    # Check if user is authorized
    email = session['email']
    cursor.execute('select * from clients where email = ?', (email,))

    client = cursor.fetchone()

    if not client:
        return redirect('/login')

    cursor.execute('select id, title, description, name, email, status from tickets')

    raw_tickets = cursor.fetchall()

    tickets = [{
        'id': t[0],
        'title': t[1],
        'description': t[2],
        'name': t[3],
        'email': t[4],
        'status': t[5],
    } for t in raw_tickets]

    print(tickets)

    return render_template("ansatt.html", tickets=tickets)

if __name__ == "__main__":
    app.run(debug=True)