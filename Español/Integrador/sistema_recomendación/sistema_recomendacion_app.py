import streamlit as st
import pandas as pd
from surprise import Reader,Dataset
from surprise.model_selection import train_test_split
from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise import accuracy
import datetime
import pyodbc

st.title('Sistema de recomendación de restaurants')

#Importamos todo el dataset de reviews completo
reviews = pd.read_parquet('https://storage.googleapis.com/restaurants_datalake/Archivos_app/reviews_ml.parquet')

#Importamos el dataset de restaurants
restaurants = pd.read_parquet('https://storage.googleapis.com/restaurants_datalake/restaurants.parquet')

#Importamos el dataset con los códigos e ids de usuarios y lo mergeamos con las reviews
usuarios = pd.read_csv('https://storage.googleapis.com/restaurants_datalake/usuarios.csv')
merge = pd.merge(reviews,usuarios,on='Cod_Usuario')
reviews = merge[['Id_Usuario','Id_Restaurant','Rating']]        #Nos quedamos con el id de usuario

#Definimos listas de estados y códigos
state_codes = {'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT',
    'Delaware': 'DE','Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA',
    'Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI',
    'Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH',
    'New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH','Oklahoma': 'OK',
    'Oregon': 'OR','Pennsylvania': 'PA','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX',
    'Utah': 'UT','Vermont': 'VT','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}

estados = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Columbia','Georgia',
           'Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan',
           'Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New_Hampshire','New_Jersey','New_Mexico','New_York',
           'North_Carolina','North_Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode_Island','South_Carolina','South_Dakota',
           'Tennessee', 'Texas', 'Utah','Vermont', 'Virginia', 'Washington', 'West_Virginia', 'Wisconsin', 'Wyoming']

#Elegimos el estado y filtramos los restaurants que sean del estado elegido
estado = st.selectbox('Ingrese un estado dentro de EE.UU:',options=estados)
estado_cod = state_codes.get(estado,'NY')
restaurants_est = restaurants[restaurants['Estado']==estado_cod]

#Ingresar el tipo de recomendación
tipo_recomendacion = st.selectbox('Ingrese el tipo de recomendacion que desea:',
                                  options=['Recomendación por usuario','Recomendación por tipo de restaurant'])
if tipo_recomendacion == 'Recomendación por usuario':
    #Filtraremos estos en el dataset de reviews
    reviews_est = reviews[reviews['Id_Restaurant'].isin(restaurants_est['Id_Restaurant'].values)]

    #Crea un objeto Reader y Dataset de Surprise
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(reviews_est[["Id_Usuario", "Id_Restaurant", "Rating"]], reader)

    #Dividimos los datos en conjuntos de entrenamiento y prueba
    trainset, testset = train_test_split(data, test_size=0.25)

    #Instanciamos modelo, entrenamos y testeamos
    model = SVD(n_factors=217, n_epochs=35, lr_all=0.025, reg_all=0.07)
    model.fit(trainset)
    predicciones = model.test(testset)
    precision = accuracy.rmse(predicciones,verbose=False)

    if precision > 1:
        st.markdown('#### El modelo no pudo entrenarse correctamente')
    else:
        usuario = st.selectbox('Ingrese su Id de usuario:',options=list(reviews_est['Id_Usuario'].unique()))
        buscar_us = st.button('Buscar')
        if buscar_us:
            restaurants_ya_visitados = list(reviews_est[reviews_est['Id_Usuario']==usuario]['Id_Restaurant'].unique())
            restaurants_posibles = reviews_est[~reviews_est['Id_Restaurant'].isin(restaurants_ya_visitados)]['Id_Restaurant'].unique()
            lista_rest = []
            lista_calif = []
            for r in restaurants_posibles:
                lista_rest.append(model.predict(usuario,r).iid)
                lista_calif.append(model.predict(usuario,r).est)
            diccionario = {'Restaurant_Id':lista_rest,'Rating_pred':lista_calif}
            predicciones_df = pd.DataFrame(diccionario)
            mejores_pred = predicciones_df[predicciones_df['Rating_pred']>3].sort_values(by='Rating_pred',ascending=False)
            if mejores_pred.shape[0]>5:
                restaurants_recom = restaurants_est[restaurants_est['Id_Restaurant'].isin(mejores_pred.iloc[:5]['Restaurant_Id'].values)]
            else:
                restaurants_recom = restaurants_est[restaurants_est['Id_Restaurant'].isin(mejores_pred['Restaurant_Id'].values)]
            st.write('Le recomendamos los siguientes restaurants:')
            st.dataframe(restaurants_recom[['Id_Restaurant','Nombre','Tipo']].reset_index(drop=True))
            # for i in range(5):            
            #     cursor.execute('INSERT INTO historial_busqueda (HB_Timestamp, HB_TipoRec, HB_RestId, HB_RestNombre, HB_RestTipo) VALUES(?,?,?,?,?)',
            #                 int(datetime.datetime.now().timestamp()),
            #                 tipo_recomendacion,
            #                 restaurants_recom['Id_Restaurant'].values[i],
            #                 restaurants_recom['Nombre'].values[i],
            #                 restaurants_recom['Tipo'].values[i])
            # cursor.commit()

else:
    tipo_rest = st.selectbox('Ingrese tipo de restaurant:',options=list(restaurants_est['Tipo'].unique()))
    buscar_tipo = st.button('Buscar')
    if buscar_tipo:
        restaurants_tipo = restaurants_est[restaurants_est['Tipo']==tipo_rest].sort_values(by='Rating_promedio',ascending=False)
        recomendaciones_tipo = restaurants_tipo[['Id_Restaurant','Nombre','Tipo']].reset_index(drop=True).head()
        st.write('Le recomendamos los siguientes restaurants:')
        st.dataframe(recomendaciones_tipo)
        # for i in range(5):            
        #     cursor.execute('INSERT INTO historial_busqueda (HB_Timestamp, HB_TipoRec, HB_RestId, HB_RestNombre, HB_RestTipo) VALUES(?,?,?,?,?)',
        #                 int(datetime.datetime.now().timestamp()),
        #                 tipo_recomendacion,
        #                 recomendaciones_tipo['Id_Restaurant'].values[i],
        #                 recomendaciones_tipo['Nombre'].values[i],
        #                 recomendaciones_tipo['Tipo'].values[i])
        # cursor.commit()

#Mostramos el historial de búsqueda. Sacar luego.
# hist_busqueda = st.checkbox('Mostrar historial de búsqueda')
# if hist_busqueda:
#     st.dataframe(pd.read_sql('SELECT * FROM historial_busqueda',conn))