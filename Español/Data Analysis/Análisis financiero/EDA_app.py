#Importamos las librerías
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import yfinance as yf
sns.set()

#Definimos función para guardar los datasets en dataframes.

def impData (symbol:str,comp=False):
    df = pd.DataFrame(yf.Ticker(symbol).history('23y'))
    df.index=df.index.strftime('%Y-%m-%d')
    df.index=pd.to_datetime(df.index)
    if comp:
        df.drop(columns=['Open','High','Low','Stock Splits'],inplace=True)
    else:
        df.drop(columns=['Open','High','Low','Dividends','Stock Splits'],inplace=True)
    return df

#Ponemos la fuente
st.markdown('###### Fuente: Yahoo Finance')

#Le agregamos un título
st.title('Análisis de empresas - SP500')

#Creamos el gráfico interactivo del índice SP500 donde vamos a analizar su comportamiento a lo largo de estos 23 años
sp500 = impData('^GSPC')
st.write('')
st.write('')
st.write('##### Evolucion del índice SP500 en los últimos 23 años')
st.write('')
st.write('')
fig1 = plt.figure(figsize=(8,6))
fecha_inicio,fecha_fin = st.slider('Definir período de análisis',value=(datetime.combine(sp500.index.min(), datetime.min.time()),
                                                        datetime.combine(sp500.index.max(), datetime.min.time())),
                    step=timedelta(days=1))
sns.lineplot(data=sp500[(sp500.index>fecha_inicio)&(sp500.index<fecha_fin)],y='Close',
             x=sp500[(sp500.index>fecha_inicio)&(sp500.index<fecha_fin)].index)
plt.title('SP500',fontdict={'fontsize':20})
plt.ylabel('Precio del activo (US$)')
plt.xlabel('Fecha')
st.pyplot(fig1)

st.write('')
st.write('')

#Seleccionamos un sector para analizar a profundidad.
st.write('##### Evolucion de los distintos sectores en los últimos 23 años')
sp500_empresas = pd.read_csv('Empresas_SP500_con_marketcap.csv')
lista_sectores = list(sp500_empresas['GICS Sector'].unique())
lista_sectores.remove('Energy')
sector = st.selectbox('Elija sector a analizar',options=lista_sectores)

industrias = {'Materials':15,'Industrials':20,'Consumer Discretionary':25,'Consumer Staples':30,'Health Care':35,
              'Financials':40,'Information Technology':45,'Communication Services':50,'Utilities':55,'Real Estate':60}

#Importamos la data de este sector.
sp_sector = impData('^SP500-'+str(industrias[sector]))

#Graficamos
fig2 = plt.figure(figsize=(8,6))
fecha_inicio_sec,fecha_fin_sec = st.slider('Definir fechas de gráfico',value=(datetime.combine(sp_sector.index.min(), datetime.min.time()),
                                                        datetime.combine(sp_sector.index.max(), datetime.min.time())),
                    step=timedelta(days=1))
sns.lineplot(data=sp_sector[(sp_sector.index>fecha_inicio_sec)&(sp_sector.index<fecha_fin_sec)],y='Close',
             x=sp_sector[(sp_sector.index>fecha_inicio_sec)&(sp_sector.index<fecha_fin_sec)].index)
plt.title('SP500 '+str(sector),fontdict={'fontsize':20})
plt.ylabel('Precio del activo (US$)')
plt.xlabel('Fecha')
st.pyplot(fig2)

#Añadimos información
if st.checkbox('Mostrar información del sector',False):
    st.write('Cantidad de empresas que componen en el sector: '+ str(sp500_empresas[sp500_empresas['GICS Sector']==sector].shape[0]))
    st.dataframe(sp500_empresas[sp500_empresas['GICS Sector']==sector])

st.write('')
st.write('')

#Seleccionamos los sectores a comparar
st.write('##### Comparación de la evolución de los distintos sectores en los últimos 23 años')
sector1,sector2 = st.multiselect('Elija sectores a comparar',options=lista_sectores,max_selections=2,default=lista_sectores[0:2])

#Importamos los datos
sp_sector1 = impData('^SP500-'+str(industrias[sector1]))
sp_sector2 = impData('^SP500-'+str(industrias[sector2]))

#Graficamos la evolucion de los 2 sectores
fig3, ax = plt.subplots(1,2,sharey=True,figsize=(12,8))
fecha_inicio_comp_sec,fecha_fin_comp_sec = st.slider('Definir fechas de gráficos',value=(datetime.combine(sp_sector1.index.min(), datetime.min.time()),
                                                        datetime.combine(sp_sector1.index.max(), datetime.min.time())),
                    step=timedelta(days=1))
sns.lineplot(data=sp_sector1[(sp_sector1.index>fecha_inicio_comp_sec)&(sp_sector1.index<fecha_fin_comp_sec)],
             y='Close',x=sp_sector1[(sp_sector1.index>fecha_inicio_comp_sec)&(sp_sector1.index<fecha_fin_comp_sec)].index,ax=ax[0])
ax[0].set_title('Indice del sector '+sector1)
ax[0].set_ylabel('Precio del activo (US$)')
ax[0].set_xlabel('')
sns.lineplot(data=sp_sector2[(sp_sector2.index>fecha_inicio_comp_sec)&(sp_sector2.index<fecha_fin_comp_sec)],
             y='Close',x=sp_sector2[(sp_sector2.index>fecha_inicio_comp_sec)&(sp_sector2.index<fecha_fin_comp_sec)].index,ax=ax[1])
ax[1].set_title('Indice del sector '+sector2)
ax[1].set_xlabel('')
st.pyplot(fig3)

#Vamos a analizar las empresas individualmente para quedarnos con unas pocas. Para ello, definimos un sector y habilitamos la elección entre las empresas de este sector.
sector_selec = st.selectbox('Elija sector para profundizar',options=lista_sectores)
sector_comp = sp500_empresas[sp500_empresas['GICS Sector']==sector_selec]
lista_empresas = list(sector_comp['Security'].unique())

#Antes de adentrarnos a analizar cada empresa, las comparamos en su conjunto. Ploteamos un scatterplot.
fig5 = plt.figure()
sns.scatterplot(data=sector_comp,x='Market Capitalization',y='Current stock value')
plt.ylabel('Precio del activo (US$)')
plt.xlabel('Capitalización de mercado (US$)')
st.pyplot(fig5)

#Ploteamos el market cap y valor actual de la acción de la mitad con mayores valores.
fig4,ax2 = plt.subplots(1,2,figsize=(8,10))
sns.barplot(data=sector_comp.sort_values(by='Market Capitalization',
            ascending=False).head(int(sector_comp.shape[0]/2)),
            x='Market Capitalization',y='Symbol',orient='h',ax=ax2[0])
ax2[0].set_ylabel('Simbolo')
ax2[0].set_xlabel('Capitalización de mercado (US$)',loc='left')
sns.barplot(data=sector_comp.sort_values(by='Current stock value',
            ascending=False).head(int(sector_comp.shape[0]/2)),
            x='Current stock value',y='Symbol',orient='h',ax=ax2[1])
ax2[1].set_ylabel('Simbolo')
ax2[1].set_xlabel('Precio del activo (US$)')
st.pyplot(fig4)

#Seleccionamos las empresas dentro del sector seleccionado
empresas_seleccionadas = st.multiselect('Seleccione empresas a analizar',options=lista_empresas,max_selections=6,default=lista_empresas[0])

#Graficamos
if len(empresas_seleccionadas) == 1:
    fig6 = plt.figure(figsize=(8,6))
    simbolo = sp500_empresas[sp500_empresas['Security']==empresas_seleccionadas[0]]['Symbol'].values[0]     #Buscamos el código
    empresa = impData(simbolo,True)                                                                     #Importamos la data
    empresa_tendencia = empresa['Close'].rolling(window=(100),center=True).mean()                           #Obtenemos la media móvil
    empresa_tendencia.dropna(inplace=True)                                                                  #Descartamos los nulos
    sns.lineplot(data=empresa,x=empresa.index,y='Close')                                                    #Gráficamos la evolución de los precios de la empresa
    sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values)               #Graficamos la media móvil
    plt.title(empresas_seleccionadas[0])
    plt.xlabel('')
    plt.ylabel('Precio del activo (US$)')
elif len(empresas_seleccionadas)<4:
    fig6, ax3 = plt.subplots(1,len(empresas_seleccionadas),figsize=(6+(2*len(empresas_seleccionadas)),6),sharey=True)   #Armamos la figura adaptada a la
    ax3[0].set_ylabel('Precio del activo (US$)')                                                                        #cantidad de selecciones
    for i in range(len(empresas_seleccionadas)):
        simbolo = sp500_empresas[sp500_empresas['Security']==empresas_seleccionadas[i]]['Symbol'].values[0]
        empresa = impData(simbolo,True)
        empresa_tendencia = empresa['Close'].rolling(window=(100),center=True).mean()
        empresa_tendencia.dropna(inplace=True)
        sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[i])
        sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values,ax=ax3[i])
        ax3[i].set_title(empresas_seleccionadas[i])
        ax3[i].set_xlabel('')
elif len(empresas_seleccionadas) == 4:
     fig6, ax3 = plt.subplots(2,2,figsize=(10,10),sharex=True,sharey=True)
     plt.xlabel('')
     ax3[0,0].set_ylabel('Precio del activo (US$)')
     ax3[1,0].set_ylabel('Precio del activo (US$)')
     for i in range(len(empresas_seleccionadas)):
        simbolo = sp500_empresas[sp500_empresas['Security']==empresas_seleccionadas[i]]['Symbol'].values[0]
        empresa = impData(simbolo,True)
        empresa_tendencia = empresa['Close'].rolling(window=(100),center=True).mean()
        empresa_tendencia.dropna(inplace=True)                                                 
        if i<2:
            sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[0,i])
            sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values,ax=ax3[0,i])
            ax3[0,i].set_title(empresas_seleccionadas[i])
        else:
            sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[1,i-2])
            sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values,ax=ax3[1,i-2])
            ax3[1,i-2].set_title(empresas_seleccionadas[i])
            ax3[1,i-2].set_xlabel('')
else:
    fig6, ax3 = plt.subplots(2,1+round(len(empresas_seleccionadas)/3),sharex=True,sharey=True,
                             figsize=(8+2*round(len(empresas_seleccionadas)/3),10))
    ax3[0,0].set_ylabel('Precio del activo (US$)')
    ax3[1,0].set_ylabel('Precio del activo (US$)')
    for i in range(len(empresas_seleccionadas)):
        simbolo = sp500_empresas[sp500_empresas['Security']==empresas_seleccionadas[i]]['Symbol'].values[0]
        empresa = impData(simbolo,True)
        empresa_tendencia = empresa['Close'].rolling(window=(100),center=True).mean()
        empresa_tendencia.dropna(inplace=True)
        if i<3:
            sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[0,i])
            sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values,ax=ax3[0,i])
            ax3[0,i].set_title(empresas_seleccionadas[i])
        else:
            sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[1,i-3])
            sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values,ax=ax3[1,i-3])
            ax3[1,i-3].set_title(empresas_seleccionadas[i])
            ax3[1,i-3].set_xlabel('')
st.pyplot(fig6)