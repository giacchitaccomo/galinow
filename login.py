import requests
import os
import logging

from dotenv import load_dotenv



load_dotenv()

def fetch():
    """
    Dal sito del registro elettronico accedo e ricavo le informazioni generali, ritornate come dict
    """
    url =  "https://" + "galilei-cr-sito.registroelettronico.com/api/v4/utenti/login-web/"
    pack = ""
    
    pack = {
    "mastercom": "galilei-cr",
    "utente": os.getenv("MASTERCOM_USER"),
    "password": os.getenv("MASTERCOM_PASS")
    }
        
    answer = requests.post(url, json=pack)
    logging.debug("Accesso eseguito con successo")
    
    return answer.json()
        
        
        
    
