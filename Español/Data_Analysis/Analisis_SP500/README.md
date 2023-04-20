El siguiente contenido es una guía para poder seguir el trabajo. Es importante aclarar que **el trabajo es realizado a modo de aprendizaje.**

## Contenido

El contenido va a ser listado en el orden en el que se realizaron las tareas del proyecto.

- **webscrapping.ipybnb:** En este notebook se importó toda la data necesaria por medio de la librería yfinance. El objetivo de descargar los datasets fue mejorar la performance de la app en streamlit. También se realizó un pequeño análisis inicial detectando correlaciones entre campos y columnas con valores únicos y se limpiaron. Se descargaron los siguientes datasets:

    - Empresas_SP500_con_marketcap.csv: Listado de las empresas que componen el índice SP500. Se obtuvo de wikipedia (https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) y se le agregó, luego, el valor de capitalización de mercado y el precio de la acción obtenidos por medio de yfinance.

    - sp500.csv: Evolución del índice durante los últimos 23 años. Se obtuvo de yfinance.

    - Sectores: Carpeta que contiene la evolución de los sectores que componen el índice SP500.

    - Empresas: Carpeta que contiene la evolución del precio de las acciones de todas las empresas que componen el índice SP500.

- **Análisis por sector.ipynb:** En este notebook se realizó una primera visualización del índice SP500, de los sectores, y de las empresas que componen los sectores.

- **EDA_app.py:** Script de python que contiene el código base de la aplicación realizada en streamlit utilizada para hacer el análisis inicial de los datos y obtener las empresas en las que se va a profundizar usando PowerBI.

- **pi02_st_env:** Entorno virtual creado para el desarrollo de la aplicación en streamlit.

- **requirements.txt:** Archivo enviado a streamlit con las librerías requeridas para el deploy de la aplicación. El link a la aplicación es el siguiente: https://pi02-eda.streamlit.app/

- **Analisis empresas.ipynb**: Se realizan nuevos gráficos en las empresas seleccionadas a través del análisis de la API que luego se cargarán también a la API para poder verlos ahi. 

- **PI02_Analisis empresas.pbix:** Dashboard donde se analizan las 3 empresas seleccionadas del sector seleccionado. En este se encuentran indicadores más precisos que para decidir en que empresa invertir.