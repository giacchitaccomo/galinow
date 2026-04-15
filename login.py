import requests
import logging
import json





def fetch(username, password):
    """
    Dal sito del registro elettronico accedo e ricavo le informazioni generali, ritornate come dict
    """
    url =  "https://" + "galilei-cr-sito.registroelettronico.com/api/v4/utenti/login-web/"
    pack = {"mastercom":"galilei-cr","utente": username,"password": password}
    answer = requests.post(url, json=pack)
    logging.debug("Accesso eseguito con successo")
    
    return answer.json()
        
        
        
    
