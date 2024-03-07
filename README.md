# Biblia de Jerusalén en JSON
Biblia católica en formato json extraída de la web de la conferencia episcopal española (https://www.conferenciaepiscopal.es/biblia/). Incluye otro json con los paralelos sacados de la web de biblia paralela (https://bibliaparalela.com/).

## Contenido
El repositorio incluye:
1. La biblia de Jerusalén completa en JSON
2. Script de web scraping de la web de la conferencia episcopal española que descarga la biblia entera y la guarda
3. Mapa con todos los paralelos en JSON
4. Script de web scraping de la web de biblia paralela que descarga todos los paralelos

Modificando el script se puede crear una estructura diferente a la diseñada. 

## Cómo usar
Este repositorio ya incluye los dos archivos JSON necesarios, pero si se desea descargar se pueden utilizar los script de python. Los pasos a seguir para generar los JSON son:
1. Ejecutar directamente el script que descarga la biblia (scraper_biblia.py). Al terminar creará el archivo JSON llamado 'biblia.json'.
```
python scraper_biblia.py
```
2. Hacer una copia de 'biblia.json' y renombrarlo a 'paralelos.json'. Este archivo será la base para descargar los paralelos.
3. Ejecutar el script que descarga los paralelos y los sobreescribe en el fichero 'paralelos.json'. Es posible que este proceso tarde un tiempo.
```
python scraper_paralelos.py
```
4. El archivo 

## Contacto
Para cualquier duda o contacto escribir a micanlo.dev@gmail.com
