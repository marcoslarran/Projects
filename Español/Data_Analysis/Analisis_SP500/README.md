# Analisis del índice SP500

EL objetivo del presente trabajo es realizar una recomendación para invertir en alguna de las empresas que componen el índice SP500. Las conclusiones obtenidas están basadas en lo observado en los datos y no en conocimiento financiero i de trading. Es importante aclarar que **el trabajo es realizado a modo de aprendizaje.**

## Contenido

El contenido va a ser listado en el orden en el que se realizaron las tareas del proyecto.

- **webscrapping.ipybnb:** En este notebook se importó toda la data necesaria por medio de la librería yfinance. También se realizó un pequeño análisis inicial detectando correlaciones entre campos y columnas con valores únicos y se limpiaron.

- **Análisis por sector.ipynb:** En este notebook se realizó una primera visualización de los sectores que componen el índice SP500.

- **Analisis empresas.ipynb**: En este notebook se realizó una primera visualización de las empresas que componen el índice SP500.

- **Aplicacion.py:** Script de python que contiene el código base de la aplicación realizada en streamlit utilizada para hacer el análisis inicial de los datos y obtener las empresas en las que se va a profundizar usando PowerBI.

- **requirements.txt:** Archivo enviado a streamlit con las librerías requeridas para el deploy de la aplicación. El link a la aplicación es el siguiente: https://sp500ml.streamlit.app/

- **Analisis empresas.pbix:** Dashboard donde se analizan las 3 empresas seleccionadas del sector seleccionado. En este se encuentran indicadores más precisos que para decidir en que empresa invertir.