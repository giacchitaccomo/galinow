import requests



import collections

from bs4 import BeautifulSoup


def fetch_online(headers, url):
    """
    trasforma in un dizionario e ritorna la risposta di get(url)
    """
    response = requests.get(url=url, headers=headers)
    response = response.json()
    return response



def fetch_orario(classe):
    url = "https://galileicrema.edu.it/extran/orarioclasse.php/" + classe.strip()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        classi_html = collections.defaultdict(list)
        hours = 0

        for row in rows:
            cells = row.find_all("td")
            
            if not cells:
                continue
            
            if hours == 5:
                classi_html[hours] = "PAUSA"
                hours += 1
                continue
            
            riga_del_giorno = []
            
            for cell in cells[1:7]:
                text = cell.get_text(separator="|").strip()
                
            
                if text and text != "|":
                    parts = text.split("|")
                    subject = parts[0].strip()
                    room = parts[1].strip() if len(parts) > 1 else ""
                    
                    
                    riga_del_giorno.append([subject, room])
                else:
                    riga_del_giorno.append("")
                    
            classi_html[hours] = riga_del_giorno
            
            hours += 1
                    
        return classi_html
    else:
        return None
                
                
            
   