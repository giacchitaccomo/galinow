
from organizers import initialize
import logging
import pathlib
from datetime import datetime, timedelta
import os
from flask import Flask, render_template, redirect, session, url_for, request




path = pathlib.Path(__file__).parent #first i retrieve the full path (the one with main.py), and then i retreive the dir main is in with .parent


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(funcName)s] / (%(asctime)s.%(msecs).03d) - %(levelname)s - %(message)s", #formatta i messaggi di logging al livello di DEBUG 
    datefmt="%I:%M:%S"
    
)

  

app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY')
app.secret_key = "chiave"





@app.route("/")
def home():
    if session.get("logged_in"):
        return render_template("index.html")
    else:
        return redirect(url_for("login"))


@app.route("/orario_settimanale")
def orario_settimanale():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("orario_settimanale.html", orario_html=session.get("orario_html"))

@app.route("/voti")
def voti():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("voti.html")

@app.route("/compiti")
def compiti():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("compiti.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            error = "Inserisci username e password"
        else:
            try:
                voti_materia, voti_tempo, compiti_materia, compiti_time, materie, orario, orario_html = initialize(path, username, password)

                session["logged_in"] = True
                session["voti_materia"] = voti_materia
                session["voti_tempo"] = voti_tempo
                session["compiti_materia"] = compiti_materia
                session["compiti_time"] = compiti_time
                session["materie"] = materie
                session["orario"] = orario
                session["orario_html"] = orario_html

                return redirect(url_for("home"))
            except Exception as exc:
                logging.exception("Login failed")
                error = f"Errore di accesso: {exc}"

    return render_template("login.html", error=error)
        


def main():
    app.run(debug=True)
    
    
  
  
if __name__ == "__main__":
    main()
