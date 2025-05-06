from flask import Flask, render_template

app = Flask(__name__)

@app.route("/ticket")
def ticket():
    return render_template("ticket.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run()