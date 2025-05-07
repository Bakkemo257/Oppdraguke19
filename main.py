from flask import Flask, render_template, request, redirect
from mariadb import connect
from secret import MARIADB
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route("/")
def ticket():
    return render_template("ticket.html")

@app.route('/login',  methods=["post", "Get"])
def login():
    if request.method == 'POST':
        username = request.form["username"] 
        password = request.form["password"]


        hashed_password = generate_password_hash(password).encode('utf-8')
        print(hashed_password)
    
        return redirect("/login")
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