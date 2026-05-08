
import requests
import logging






def fetch(username, password):
    """
    Dal sito del registro elettronico accedo e ricavo le informazioni generali, ritornate come dict
    """
    url =  "https://" + "galilei-cr-sito.registroelettronico.com/api/v4/utenti/login-web/"
    pack = {"mastercom":"galilei-cr","utente": username,"password": password}
    answer = requests.post(url, json=pack)
    logging.debug("Richiesta Login Inviata OK")
    status_code = answer.status_code
    logging.debug(f"Il codice della risposta è {status_code}")
    if status_code> 399:
        logging.debug(f"Il codice della risposta è maggiore di 399. ({status_code})")
        return status_code
    
    
    return answer.json()
        