import requests





def fetch_online(headers, url):
    """
    trasforma in un dizionario e ritorna la risposta di get(url)
    """
    response = requests.get(url=url, headers=headers)
    response = response.json()
    return response

