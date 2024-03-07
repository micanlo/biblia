import requests
from bs4 import BeautifulSoup
import json
import datetime
# from j import j


url_base = "https://bibliaparalela.com/"
biblia_filename = "biblia.json"
paralelos_filename = "paralelos2.json"

try:
    with open(paralelos_filename, 'r', encoding="utf8") as archivo:
        j = json.load(archivo)
except:
    print("No se ha podido leer el archivo '" + paralelos_filename + "', si no lo tienes creado haz una copia de 'biblia.json' (que puedes encontrar en github.com/micanlo) y renombralo con este nombre. Asegúrate de que esté en el mismo directorio que este script.")
    quit()

names_map = {
    "genesis": "genesis",
    "exodus": "exodo",
    "leviticus": "levitico",
    "numbers": "numeros",
    "deuteronomy": "deuteronomio",
    "joshua": "josue",
    "judges": "jueces",
    "ruth": "rut",
    "1_samuel": "1-samuel",
    "2_samuel": "2-samuel",
    "1_kings": "1-reyes",
    "2_kings": "2-reyes",
    "1_chronicles": "1-cronicas",
    "2_chronicles": "2-cronicas",
    "ezra": "esdras",
    "nehemiah": "nehemias",
    # "": "tobias",
    # "": "judit",
    "esther": "ester",
    # "": "1-macabeos",
    # "": "2-macabeos",
    "job": "job",
    "psalms": "salmos",
    "proverbs": "proverbios",
    "ecclesiastes": "eclesiastes",
    "songs": "cantar-de-los-cantares",
    # "": "sabiduria",
    # "": "eclesiastico",
    "isaiah": "isaias",
    "jeremiah": "jeremias",
    "lamentations": "lamentaciones",
    # "": "baruc",
    "ezekiel": "ezequiel",
    "daniel": "daniel",
    "hosea": "oseas",
    "joel": "joel",
    "amos": "amos",
    "obadiah": "abdias",
    "jonah": "jonas",
    "micah": "miqueas",
    "nahum": "nahun",
    "habakkuk": "habacuc",
    "zephaniah": "sofonias",
    "haggai": "ageo",
    "zechariah": "zacarias",
    "malachi": "malaquias",
    "matthew": "mateo",
    "mark": "marcos",
    "luke": "lucas",
    "john": "juan",
    "acts": "hechos-de-los-apostoles",
    "romans": "romanos",
    "1_corinthians": "1-corintios",
    "2_corinthians": "2-corintios",
    "galatians": "galatas",
    "ephesians": "efesios",
    "philippians": "filipenses",
    "colossians": "colosenses",
    "1_thessalonians": "1-tesalonicenses",
    "2_thessalonians": "2-tesalonicenses",
    "1_timothy": "1-timoteo",
    "2_timothy": "2-timoteo",
    "titus": "tito",
    "philemon": "filemon",
    "hebrews": "hebreos",
    "james": "santiago",
    "1_peter": "1-pedro",
    "2_peter": "2-pedro",
    "1_john": "juan-cartas-1-3",
    # "2_john": "",
    # "3_john": "",
    "jude": "judas",
    "revelation": "apocalipsis"
}

# Guarda el json en un fichero
def saveJson():
    with open(paralelos_filename, 'w', encoding='utf-8') as jf: 
        json.dump(j, jf, ensure_ascii=False, indent=2)

# Devuelve el nombre del libro en español
def en2es(name_en):
    names_map = {
        "genesis": "genesis",
        "exodus": "exodo",
        "leviticus": "levitico",
        "numbers": "numeros",
        "deuteronomy": "deuteronomio",
        "joshua": "josue",
        "judges": "jueces",
        "ruth": "rut",
        "1_samuel": "1-samuel",
        "2_samuel": "2-samuel",
        "1_kings": "1-reyes",
        "2_kings": "2-reyes",
        "1_chronicles": "1-cronicas",
        "2_chronicles": "2-cronicas",
        "ezra": "esdras",
        "nehemiah": "nehemias",
        # "": "tobias",
        # "": "judit",
        "esther": "ester",
        # "": "1-macabeos",
        # "": "2-macabeos",
        "job": "job",
        "psalms": "salmos",
        "proverbs": "proverbios",
        "ecclesiastes": "eclesiastes",
        "songs": "cantar-de-los-cantares",
        # "": "sabiduria",
        # "": "eclesiastico",
        "isaiah": "isaias",
        "jeremiah": "jeremias",
        "lamentations": "lamentaciones",
        # "": "baruc",
        "ezekiel": "ezequiel",
        "daniel": "daniel",
        "hosea": "oseas",
        "joel": "joel",
        "amos": "amos",
        "obadiah": "abdias",
        "jonah": "jonas",
        "micah": "miqueas",
        "nahum": "nahun",
        "habakkuk": "habacuc",
        "zephaniah": "sofonias",
        "haggai": "ageo",
        "zechariah": "zacarias",
        "malachi": "malaquias",
        "matthew": "mateo",
        "mark": "marcos",
        "luke": "lucas",
        "john": "juan",
        "acts": "hechos-de-los-apostoles",
        "romans": "romanos",
        "1_corinthians": "1-corintios",
        "2_corinthians": "2-corintios",
        "galatians": "galatas",
        "ephesians": "efesios",
        "philippians": "filipenses",
        "colossians": "colosenses",
        "1_thessalonians": "1-tesalonicenses",
        "2_thessalonians": "2-tesalonicenses",
        "1_timothy": "1-timoteo",
        "2_timothy": "2-timoteo",
        "titus": "tito",
        "philemon": "filemon",
        "hebrews": "hebreos",
        "james": "santiago",
        "1_peter": "1-pedro",
        "2_peter": "2-pedro",
        "1_john": "juan-cartas-1-3",
        "2_john": "juan-cartas-1-3",
        "3_john": "juan-cartas-1-3",
        "jude": "judas",
        "revelation": "apocalipsis"
    }

    name_es = names_map[name_en]
    return name_es

def parseParalelo(raw):

    p1 = raw.split("/")
    libro = p1[1]

    p2 = p1[2].split(".")[0]
    p3 = p2.split("-")

    capitulo = "c"+str(p3[0])
    versiculo = "v"+str(p3[1])

    paralelo = {
        "libro": en2es(libro),
        "capitulo": capitulo,
        "versiculo": versiculo
    }

    return paralelo

def scrape():
    
    # Recorremos todos los libros de la variable names_map
    for book in names_map.keys():

        # Traducimos el nombre del libro al español
        book_es = en2es(book)

        # Averiguamos a que testamento corresponde el libro, para poder guardarlo correctamente
        testamento = "nuevo_testamento"
        if book_es in j["biblia"]["antiguo_testamento"].keys():
            testamento = "antiguo_testamento"
        
        # Extraemos el número de capítulos del libro
        max_capitulos = j["biblia"][testamento][book_es]["info"]["capitulos"]

        # Recorremos cada capítulo
        for c in range(max_capitulos):

            # Extraemos el número de versículos del capítulo
            max_versiculos = j["biblia"][testamento][book_es]["c"+str(c+1)]["versiculos"]

            # Recorremos cada versículo
            for v in range(max_versiculos):

                # Generamos el URL de donde se extrerá la información de los paralelos
                url = url_base + "/" + book + "/" + str(c+1) + "-" + str(v+1) + ".htm"

                # Hacemos la petición
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers)

                # Verificamos si la solicitud fue exitosa
                if response.status_code == 200:

                    # Parseamos el contenido HTML con BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')
                    div_paralelos = soup.find('div', id='crf')
                    spans_paralelos = div_paralelos.find_all('span', class_='crossverse')

                    # Para cada paralelo, guardamos el contenido en el json
                    for i, span_paralelo in enumerate(spans_paralelos):
                        if i == 0: 
                            j["biblia"][testamento][book_es]["c"+str(c+1)]["v"+str(v+1)] = []    
                        a = span_paralelo.find('a')
                        a_link = a["href"]
                        paralelo = parseParalelo(a_link)
                        j["biblia"][testamento][book_es]["c"+str(c+1)]["v"+str(v+1)].append(paralelo)

                    # # Mostramos por pantalla el proceso a nivel de versículo
                    # print(book_es+", Capítulo " + str(c+1) + "/"+str(max_capitulos)+", Versículo " + str(v+1) + "/"+str(max_versiculos))
                    # print("* " + str(len(spans_paralelos)) + " paralelos encontrados")
                    # print()

            # Mostramos por pantalla el proceso a nivel de capítulo
            print("✓ "+book_es+", Capítulo " + str(c+1) + "/"+str(max_capitulos))

            # Guardamos el json cada vez que terminamos un capítulo
            saveJson()

scrape()
