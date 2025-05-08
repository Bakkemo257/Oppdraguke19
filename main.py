from flask import Flask, render_template, request, redirect, session
from mariadb import connect
from secret import MARIADB, SECRET_KEY
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/',  methods=["post", "Get"])
def ticket():
    if request.method == 'POST':
        title = request.form["title"] 
        name = request.form["name"]
        email = request.form["email"] 
        description = request.form["description"]
        
        connection = connect(
            user=MARIADB['user'],
            password=MARIADB['password'],
            host=MARIADB['host'],
            port=MARIADB['port'],
            database='ticket_system'
        )
        cur = connection.cursor()
        cur.execute(
        "INSERT INTO tickets (title, description, email, name) values (?, ?, ?, ?) returning id", 
        (title, description, email, name ))

        uuid, = cur.fetchone()

        connection.commit()
        connection.close()
        
        return redirect (f"/ticket/{uuid}")
    if request.method =="GET":
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
 
    """ print(tickets) """

    return render_template("ansatt.html", tickets=tickets)

@app.post('/adduser')
def adduser ():
    if 'email' not in session:
        return redirect('/ansatt')
    
    password = request.form['password']
    email = request.form['email']
    name = request.form['name']
    admin = 'admin' in request.form

    connection = connect(
        user=MARIADB['user'],
        password=MARIADB['password'],
        host=MARIADB['host'],
        port=MARIADB['port'],
        database='ticket_system'
    )

    cursor = connection.cursor()

    cursor.execute('select admin from clients where email = ?', (session['email'],))

    client = cursor.fetchone()

    if not client:
        return redirect('/')
    
    if not client[0]:
        return redirect('/ansatt')
    
    # Hash password
    hash = generate_password_hash(password)

    # Add user
    cursor.execute('insert into clients (email, name, hash, admin) values (?, ?, ?, ?)', (email, name, hash, admin))

    connection.commit()
    connection.close()

    return redirect('/ansatt')

@app.route('/ticket/<uuid>')
def ticket_page(uuid):
    connection = connect(
        user=MARIADB['user'],
        password=MARIADB['password'],
        host=MARIADB['host'],
        port=MARIADB['port'],
        database='ticket_system'
    )

    cursor = connection.cursor()    

    cursor.execute('select title, name, email, status, description from tickets where id = ?', (uuid,))
    ticket = cursor.fetchone()

    if not ticket: return redirect('/')
    
    title, name, email, status, description = ticket

    cursor.execute('select m.content, c.name from messages m left join clients c on c.id = m.client_id where m.ticket = ? order by sent_at asc', (uuid,))

    messages = [{ 'content': m[0], 'name': m[1] } for m in cursor.fetchall()]

    return render_template('ticket_page.html', title=title, name=name, email=email, status=status, description=description, messages=messages, uuid=uuid)


@app.route('/registrer', methods=['POST'])
def skrivTilDb():
    navn = request.form['navn']
    alder = request.form['alder']

@app.route('/ticket_change_status', methods=['POST'])
def ticket_change_status():
    change_name = ""
    ticket_id = request.form["uuid"]
    if 'open' in request.form:
    # Handle save action
        change_name ="open"
    elif 'in progress' in request.form:
    # Handle delete action
        change_name ="in progress"
    elif 'closed' in request.form:
    # Handle delete action
        change_name ="closed"

    connection = connect(
        user=MARIADB['user'],
        password=MARIADB['password'],
        host=MARIADB['host'],
        port=MARIADB['port'],
        database='ticket_system'
    )

    cursor = connection.cursor()

    cursor.execute('''
                    UPDATE tickets
                    SET status = ?
                    WHERE id = ?;''', (change_name, ticket_id,) )
    
    connection.commit()
    connection.close()
    return redirect("/ansatt")

@app.post('/message')
def send_message():
    content = request.form['content']
    ticket = request.form['ticket']

    email = 'email' in session and session['email'] or ''

    if not content or len(content) == 0:
        return redirect(f'/ticket/{ticket}')

    connection = connect(
        user=MARIADB['user'],
        password=MARIADB['password'],
        host=MARIADB['host'],
        port=MARIADB['port'],
        database='ticket_system'
    )

    cursor = connection.cursor()

    if email:
        cursor.execute('select id from clients where email = ?', (email,))

        client_id, = cursor.fetchone()

        cursor.execute('insert into messages (content, client_id, ticket, sent_at) values (?, ?, ?, NOW())', (content, client_id, ticket))
    else:
        cursor.execute('insert into messages (content, ticket, sent_at) values (?, ?, NOW())', (content, ticket))

    connection.commit()
    connection.close()

    return redirect(f'/ticket/{ticket}')

if __name__ == "__main__":
    app.run(debug=True)

