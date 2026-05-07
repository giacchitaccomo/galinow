import requests
import logging

def fetch(username, password):
    """
    Dal sito del registro elettronico accedo e ricavo le informazioni
    generali, ritornate come dict
    """
    url = "https://galilei-cr-sito.registroelettronico.com/api/v4/utenti/login-web/"
    pack = {"mastercom": "galilei-cr", "utente": username, "password": password}
    
    answer = requests.post(url, json=pack)
    
    # 1. Controlla se la richiesta è andata a buon fine (status 200)
    if not answer.ok:
        print(f"ERRORE API (Login): Status Code {answer.status_code}")
        print(f"Testo risposta: {answer.text}")
        return {"error": f"Accesso bloccato dal server della scuola (Codice: {answer.status_code})"}
        
    logging.debug("Accesso eseguito con successo (Status 200)")
    
    # 2. Prova a convertire in JSON, altrimenti stampa il testo grezzo
    try:
        return answer.json()
    except Exception as e:
        print(f"ERRORE DECODIFICA JSON (Login): {e}")
        print(f"Testo grezzo ricevuto: {answer.text}")
<<<<<<< HEAD
        return {"error": "Il server della scuola ha restituito una risposta non valida."}
=======
        return {"error": "Il server della scuola ha restituito una risposta non valida."}
>>>>>>> 59a912620f6c3e9179cc24da52c52f33804e44c5
