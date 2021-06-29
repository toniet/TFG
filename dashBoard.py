
import pandas as pd
import streamlit as st


def my_widget(key):
    st.subheader('Carga de datos')
    #Carga datos Agencia 4800
    data_file = st.file_uploader("Agencia 4800",type=['xlsx'])
    if data_file is not None:
        file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
        st.write(file_details)
        df = pd.read_excel(data_file)
        st.dataframe(df)
        
    #Carga datos Agencia 4802
    data_file = st.file_uploader("Agencia 4802",type=['xlsx'])
    if data_file is not None:
        file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
        st.write(file_details)
        df = pd.read_excel(data_file)
        st.dataframe(df)
    
st.header('Predicción llamadas contact center')

st.header('Importar ficheros de datos para predecir')

data_file = st.file_uploader("Upload Data Files",type=['xlsx'])
if data_file is not None:
    file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
    st.write(file_details)
    df = pd.read_excel(data_file)
    st.dataframe(df)
       
#container = st.beta_container()
#columna1, columna2, columna3 = container.beta_columns(3)


#st.set_page_config(layout="wide")

#st.image('imagen_ruta.jpg',  use_column_width=True)

with st.sidebar:
    clicked = my_widget("Actualizar")
    if clicked:
        df = getSigaData()
        df_opens = getSigaOpens()
