from organizers import initialize
import logging
import pathlib
import os
from flask import Flask, render_template, redirect, session, url_for, request, make_response
from flask_session import Session
from functools import wraps



path = pathlib.Path(__file__).parent #first i retrieve the full path (the one with main.py), and then i retreive the dir main is in with .parent
if not os.path.exists(os.path.join(path, "cache")):
    os.makedirs(os.path.join(path, "cache")) #non so se ho bisogno di /cache ma nel caso

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

logging.getLogger("urllib3").setLevel(logging.WARNING) 
logging.getLogger("werkzeug").setLevel(logging.INFO)
#nasconde i log di debug di requests e flask


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
    print(session["voti_time"])
    return render_template("index.html", info=session["info"], materie = session["materie"], voti=session["voti_time"])


@app.route("/orario_settimanale")
@login_required
def orario_settimanale():
    return render_template("orario_settimanale.html", orario_html=session.get("orario_html"))

@app.route("/voti")
@login_required
def voti():
    return render_template("voti.html", voti_time = session["voti_time"], materie= session["materie2"])

@app.route("/compiti")
@login_required
def compiti():
    return render_template("compiti.html", compiti_time = session["compiti_time"], materie=session["materie2"])

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
            response = initialize(path, username, password)
            
            # Match the return type (string "500")
            if type(response) == int:
                error = f"Account inesistente / {response}"
                # We don't return resp here, we let it fall through to render_template
            else:
                # Unpack the list
                voti_materia, voti_time, compiti_materia, compiti_time, materie, orario, orario_html, info, materie2 = response

                # Update dictionary (strings must be reassigned)
                info["anno_scolastico"] = info["anno_scolastico"].replace("_", "/")

                # Save to session
                session.update({
                    "voti_materia": voti_materia,
                    "voti_time": dict(voti_time),
                    "compiti_materia": compiti_materia,
                    "compiti_time": compiti_time,
                    "materie": materie,
                    "orario": orario,
                    "orario_html": orario_html,
                    "info": info,
                    "username": username,
                    "password": password,
                    "materie2" : materie2, 
                    "logged_in": True
                })
                
                return redirect(url_for("index"))

        except Exception as exc:
            logging.exception("Random exception")
            if request.method == "POST":
                error = f"Errore di accesso: {exc}"
            else:
                # Clear session on failed auto-login
                session.clear() 
                return render_template("login.html", error=None)

    elif not auto:
        error = "Inserire username e password"

    # Final fallback for errors or missing credentials
    return render_template("login.html", error=error)
            


def main():
    app.run(debug=True)
    
    
  
  
if __name__ == "__main__":
    main()
