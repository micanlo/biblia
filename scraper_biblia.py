"""
Name: scraper_biblia.py
Description: Lee de la web de la conferecia episcopal española la biblia y la guarda en un json

Author: Miguel Cantero
Contact: micanlo.dev@gmail.com  

Version: v1.0.0
Date: 26-02-2024
""" 

import requests
from bs4 import BeautifulSoup
import json

filename = 'biblia.json'

# Ejemplo de la estructura que llevará
j = {
    "biblia": {
        "antiguo_testamento": {
            "genesis": {
                "info": {
                    "nombre": "Génesis",
                    "abreviatura": "Gn",
                    "grupo": "pentateuco",
                    "capitulos": 50
                },
                "c1": {
                    "versiculos": 31,
                    "v1": "Al principio creó Dios el cielo y la tierra. ",
                    "v2": "La tierra estaba informe y vacía; la tiniebla cubría la superficie del abismo, mientras el espíritu de Dios se cernía sobre la faz de las aguas.",
                    "v3": "Dijo Dios: «Exista la luz». Y la luz existió."
                }
            }
            
        },
        "nuevo_testamento": {}
    } 
}

# Libros de cada testamento
antiguo = ["genesis", "exodo", "levitico", "numeros", "deuteronomio", "josue", "jueces", "rut", "1-samuel", "2-samuel", "1-reyes", "2-reyes", "1-cronicas", "2-cronicas", "esdras", "nehemias", "tobias", "judit", "ester", "1-macabeos", "2-macabeos", "job", "salmos", "proverbios", "eclesiastes", "cantar-de-los-cantares", "sabiduria", "eclesiastico", "isaias", "jeremias", "lamentaciones", "baruc", "ezequiel", "daniel", "oseas", "joel", "amos", "abdias", "jonas", "miqueas", "nahun", "habacuc", "sofonias", "ageo", "zacarias", "malaquias"]
nuevo = ["mateo", "marcos", "lucas", "juan", "hechos-de-los-apostoles", "romanos", "1-corintios", "2-corintios", "galatas", "efesios", "filipenses", "colosenses", "1-tesalonicenses", "2-tesalonicenses", "1-timoteo", "2-timoteo", "tito", "filemon", "hebreos", "santiago", "1-pedro", "2-pedro", "juan-cartas-1-3", "judas", "apocalipsis"]

url_base = "https://www.conferenciaepiscopal.es"


def scrape(path, ref):
    # Establecer un encabezado de agente de usuario para simular una solicitud de navegador web
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Realizamos la solicitud GET a la página con el encabezado personalizado
    url = url_base + path
    response = requests.get(url, headers=headers)

    # Verificamos si la solicitud fue exitosa
    if response.status_code == 200:
        # Parseamos el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontramos todos los elementos <div> con la clase "capitulo"
        capitulos = soup.find_all('div', class_='capitulo')
        
        # Iteramos sobre los elementos encontrados
        for ic, capitulo in enumerate(capitulos):

            if ref in antiguo:
                j["biblia"]["antiguo_testamento"][ref]["info"]["capitulos"] = ic+1
            elif ref in nuevo:
                j["biblia"]["nuevo_testamento"][ref]["info"]["capitulos"] = ic+1

            if ref in antiguo:
                j["biblia"]["antiguo_testamento"][ref]["c"+str(ic+1)] = {"versiculos": 0}
            elif ref in nuevo:
                j["biblia"]["nuevo_testamento"][ref]["c"+str(ic+1)] = {"versiculos": 0}

            # Encontramos el elemento <span> con la clase "versiculos"
            numvers = capitulo.find_all('span', class_='numvers')
            contenido = capitulo.find_all('span', class_='contenido')

            for iv, numver in enumerate(numvers):
                
                if ref in antiguo:
                    j["biblia"]["antiguo_testamento"][ref]["c"+str(ic+1)]["versiculos"] = iv+1
                elif ref in nuevo:
                    j["biblia"]["nuevo_testamento"][ref]["c"+str(ic+1)]["versiculos"] = iv+1

                if ref in antiguo:
                    j["biblia"]["antiguo_testamento"][ref]["c"+str(ic+1)]["v"+str(iv+1)] = contenido[iv].text.strip()
                elif ref in nuevo:
                    j["biblia"]["nuevo_testamento"][ref]["c"+str(ic+1)]["v"+str(iv+1)] = contenido[iv].text.strip()

    else:
        print('Error al acceder a la página:', response.status_code)


def getUrls():

    url = 'https://www.conferenciaepiscopal.es/biblia/'

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    # Verificamos si la solicitud fue exitosa
    if response.status_code == 200:
        # Parseamos el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontramos todos los elementos <div> con la clase "capitulo"
        columnas = soup.find_all('div', class_='wp-block-column')
        
        for columna in columnas:

            uls = columna.find_all('ul')

            for ul in uls:
                lis = ul.find_all('li')

                for li in lis:
                    a = li.find('a')
                    
                    nombre = a.text
                    ref = a["href"].split("/")[-2]
                    url_final = a["href"]

                    if ref in antiguo:
                        j["biblia"]["antiguo_testamento"][ref] = {"info": {"nombre": nombre}}
                    elif ref in nuevo:
                        j["biblia"]["nuevo_testamento"][ref] = {"info": {"nombre": nombre}}

                    scrape(url_final, ref)
                    print("✓ " + nombre)

    else:
        print('Error al acceder a la página:', response.status_code)


getUrls()

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(j, f, ensure_ascii=False, indent=4)

print("\nBiblia completa descargada y guardada en '"+filename+"'")
