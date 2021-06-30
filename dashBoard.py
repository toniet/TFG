
import pandas as pd
import streamlit as st
import SessionState
import datetime
import calendar
from  functionsTFM import getCallData
from  functionsTFM import getDataEnvios
from  functionsTFM import dataJoin
from  functionsTFM import dataEngineering
from  functionsTFM import dataScaler
from  functionsTFM import dataPredict
from  functionsTFM import getTendencia

def my_widget():
    global session_state
    
    if not(session_state.todas):
        st.subheader('Carga de datos')
    
    # Carga datos Agencia 4800
    if (len(session_state.df4800)==0):
        data_file_4800 = st.file_uploader("Agencia 4800",type=['xlsx'])
        if data_file_4800 is not None:
            session_state.df4800 = pd.read_excel(data_file_4800)
            print(data_file_4800.name + ' cargado')
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
    
    # Carga datos Agencia 4802
    if (len(session_state.df4802)==0):
        data_file_4802 = st.file_uploader("Agencia 4802",type=['xlsx'])
        if data_file_4802 is not None:
            session_state.df4802 = pd.read_excel(data_file_4802)
            print(data_file_4802.name + ' cargado')
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        
    # Carga datos Agencia 4803
    if (len(session_state.df4803)==0):
        data_file_4803 = st.file_uploader("Agencia 4803",type=['xlsx'])
        if data_file_4803 is not None:
            session_state.df4803 = pd.read_excel(data_file_4803)
            print(data_file_4803.name + ' cargado')
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        
    # Carga datos Agencia 4806
    if (len(session_state.df4806)==0):
        data_file_4806 = st.file_uploader("Agencia 4806",type=['xlsx'])
        if data_file_4806 is not None:
            session_state.df4806 = pd.read_excel(data_file_4806)
            print(data_file_4806.name + ' cargado')
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        
    # Carga datos Agencia 4810
    if (len(session_state.df4810)==0):
        data_file_4810 = st.file_uploader("Agencia 4810",type=['xlsx'])
        if data_file_4810 is not None:
            #file_details = {"Filename":data_file_4810.name,"FileType":data_file_4810.type,"FileSize":data_file_4810.size}
            #st.write(file_details)
            session_state.df4810 = pd.read_excel(data_file_4810)
            print(data_file_4810.name + ' cargado')
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
            
    # Concatenar datos de las oficnas
    if (((len(session_state.df4800)>0) and (len(session_state.df4802)>0) and (len(session_state.df4803)>0) and (len(session_state.df4806)>0) and (len(session_state.df4810)>0)) and not(session_state.todas) ):
        print('Concatenando')
        session_state.todas = True
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4800])
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4802])
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4803])
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4806])
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4810])
        raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        
#########################################################################################################################################

# Variables locales
session_state = SessionState.get(df4800 = pd.DataFrame(), 
                                 df4802 = pd.DataFrame(),
                                 df4803 = pd.DataFrame(),
                                 df4806 = pd.DataFrame(),
                                 df4810 = pd.DataFrame(),
                                 df_shipping = pd.DataFrame(),
                                 todas=False)

dtoday = datetime.datetime.today()
dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
diasesp = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
dia = dias[dtoday.weekday()]
diaesp = diasesp[dtoday.weekday()]

st.header('Información relativa a la campaña')

df_info = pd.read_pickle('./data/df_data')
df_info = df_info[['Fecha', 'envios', 'llamadas']][df_info[dia]==1]

container = st.beta_container()
columna1, columna2 = container.beta_columns(2)
#st.set_page_config(layout="wide")

columna1.pyplot(getTendencia(df_info['llamadas'], 'Distribucion de llamadas en ' + diaesp, 'gray' ))
columna2.pyplot(getTendencia(df_info['envios'], 'Distribucion de envios en ' + diaesp, 'green'))
st.write('##### La media de llamadas en ' + diaesp + ' es: ' + str(df_info['llamadas'].mean().round(2)) + ' y la media de envios es: ' + str(df_info['envios'].mean().round(2)))

if (session_state.todas):
    st.header('Predicción llamadas contact center')
    
    df_calls = getCallData('xxxxxxxxxx')
    df_shippings = getDataEnvios(session_state.df_shipping)
    print('Haciendo join de los datos')
    df = dataJoin(df_calls, df_shippings)
    print('Haciendo dataengineering')
    df = dataEngineering(df)
    print('Normalizando datos')
    df = dataScaler(df)
    prediction = dataPredict(df)
    
    st.write('El dia ' + str(dtoday.day) + '/' + str(dtoday.month) + '/' + str(dtoday.year) + ' se esperan: ' + str(prediction) + ' llamadas')

with st.sidebar:
    clicked = my_widget()
    if (session_state.todas == True):
        st.header('Carga completa')
        st.write('Ahora ya puede cerrar esta barra de navegacion')
