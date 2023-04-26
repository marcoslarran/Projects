# Webscrapping - Imágenes
En el siguiente proyecto se realizó el scrapping de un conjunto de imágenes de una página web utilizando el módulo de Python BeautifuSoup.

## **Objetivos**
Los objetivos planteados eran los siguientes:
* Almacenar localmente las imágenes obtenidas desde una web de un fabricante de baterías. Fuente: https://www.exidegroup.com/es/es/battery-finder/browse-all
* Renombrar las imágenes dándoles el siguiente formato Marca- MODELO.jpg. Ejemplo: EXIDE- EK508.jpg.
* Subir las mismas a Google Drive utilizando Google Drive API.
* Crear un archivo de Excel con el nombre de cada imagen dado anteriormente juntamente con su URL.

## **Proceso y stack tecnológico**
Para realizar el trabajo se utilizaron las siguientes herramientas:


![Stack_tecnologico](Stack.png)

## **Documentos**
En el presente proyecto se encuentran las siguientes carpetas y archivos:
* **webscrapping.ipynb:** Notebook con todo el código necesario para realizar el trabajo.
* **quickstart.py:** Script de python para gestionar permisos de Google Drive API. Fuente: Documentación de Google Drive API
* **imagenes:** Carpeta con todas las imágenes de las baterías descargadas.
* **baterias.xlsx:** Excel con el nombre de la batería y un link a la imagen.
* **Stack.png:** Imagen con el stack tecnológico.