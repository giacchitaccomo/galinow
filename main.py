from organizers import initialize
import logging
import pathlib
import os
from flask import Flask, render_template, redirect, session, url_for, request, make_response
from flask_session import Session
from functools import wraps



path = pathlib.Path(__file__).parent #first i retrieve the full path (the one with main.py), and then i retreive the dir main is in with .parent


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(funcName)s] / (%(asctime)s.%(msecs).03d) - %(levelname)s - %(message)s", #formatta i messaggi di logging al livello di DEBUG 
    datefmt="%I:%M:%S"
    
)


  

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session"

Session(app)



def login_required(f):
    
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        else:
            return f(*args, **kwargs)
    return decorated



@app.route("/")
@login_required
def index():
        return render_template("index.html", info=session["info"])


@app.route("/orario_settimanale")
@login_required
def orario_settimanale():
    return render_template("orario_settimanale.html", orario_html=session.get("orario_html"))

@app.route("/voti")
@login_required
def voti():
    return render_template("voti.html", voti_time = session["voti_time"], materie= session["materie"])

@app.route("/compiti")
@login_required
def compiti():
    return render_template("compiti.html", compiti_time = session["compiti_time"], materie=session["materie"])

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    username = None
    password = None
    auto = True

    
    if request.method == "POST": #se la richiesta è post allora sto inviando le credenziali tramite form
        session.clear() 
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        auto = False
    else:
        # se no è un get, tento di recuperare le credenziali tramite cookie
        # username = request.cookies.get("username")
        # password = request.cookies.get("password")
        username = session.get("username") 
        password = session.get("password")       
        auto = True

    # se username e pw != None
    if username and password:
        try:
            # provo a usarli per il login
            voti_materia, voti_time, compiti_materia, compiti_time, materie, orario, orario_html, info = initialize(path, username, password)

            # salvataggio dati pesanti lato server, non permanente
            session["voti_materia"] = voti_materia
            session["voti_time"] = voti_time
            session["compiti_materia"] = compiti_materia
            session["compiti_time"] = compiti_time
            session["materie"] = materie
            session["orario"] = orario
            session["orario_html"] = orario_html
            info["anno_scolastico"].replace("_", "/")   #2025_2026 -> 2025/2026            
            session["info"] = info

            # CREAZIONE RISPOSTA CON REDIRECT + COOKIE
            resp = make_response(redirect(url_for("index")))
            # resp.set_cookie("username", username, max_age=60*60*24*7) # 7 giorni
            # resp.set_cookie("password", password, max_age=60*60*24*7)
            # resp.set_cookie("logged_in", "True", max_age=60*60*24*7)
            session["username"] = username  # 7 giorni
            session["password"] = password 
            session["logged_in"] = True 
            
            return resp

        except Exception as exc:
            logging.exception("Login failed")
            # Se POST => è fallito un login manuale
            if request.method == "POST":
                error = f"Errore di accesso: {exc}"
            else:
                # se GET => fallimento auto login, credenziali non valide, reset
                resp = make_response(render_template("login.html", error=None))
                session.pop("username", None)
                session.pop("password", None)
               
                return resp
    elif not auto: # se non ho username e pw e non si tratta di un tentativo automatico
        error = "Inserire username e password"

    return render_template("login.html", error=error)
        


def main():
    app.run(debug=True)
    
    
  
  
if __name__ == "__main__":
    main()
