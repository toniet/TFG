
import pandas as pd
import streamlit as st
import SessionState

df_shipping = pd.DataFrame()

session_state = SessionState.get(df4800 = pd.DataFrame(), 
                                 df4802 = pd.DataFrame(),
                                 df4803 = pd.DataFrame(),
                                 df4806 = pd.DataFrame(),
                                 df4810 = pd.DataFrame(),
                                 df_shipping = pd.DataFrame(),
                                 todas=True)

st.dataframe(session_state.df_shipping)

def my_widget():
    global session_state
    
    st.subheader('Carga de datos')
    
    #Carga datos Agencia 4800
    if (len(session_state.df4800)==0):
        data_file_4800 = st.file_uploader("Agencia 4800",type=['xlsx'])
        if data_file_4800 is not None:
            session_state.df4800 = pd.read_excel(data_file_4800)
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
    
    #Carga datos Agencia 4802
    if (len(session_state.df4802)==0):
        data_file_4802 = st.file_uploader("Agencia 4802",type=['xlsx'])
        if data_file_4802 is not None:
            session_state.df4802 = pd.read_excel(data_file_4802)
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        
    #Carga datos Agencia 4803
    if (len(session_state.df4803)==0):
        data_file_4803 = st.file_uploader("Agencia 4803",type=['xlsx'])
        if data_file_4803 is not None:
            session_state.df4803 = pd.read_excel(data_file_4803)
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        
    #Carga datos Agencia 4806
    if (len(session_state.df4806)==0):
        data_file_4806 = st.file_uploader("Agencia 4806",type=['xlsx'])
        if data_file_4806 is not None:
            session_state.df4806 = pd.read_excel(data_file_4806)
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        
    #Carga datos Agencia 4810
    if (len(session_state.df4810)==0):
        data_file_4810 = st.file_uploader("Agencia 4810",type=['xlsx'])
        if data_file_4810 is not None:
            #file_details = {"Filename":data_file_4810.name,"FileType":data_file_4810.type,"FileSize":data_file_4810.size}
            #st.write(file_details)
            session_state.df4810 = pd.read_excel(data_file_4810)
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
    
    if (((len(session_state.df4800)>0) and (len(session_state.df4802)>0) and (len(session_state.df4803)>0) and (len(session_state.df4806)>0) and (len(session_state.df4810)>0)) and session_state.todas ):
        session_state.todas = False
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4800])
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4802])
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4803])
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4806])
        session_state.df_shipping = pd.concat([session_state.df_shipping, session_state.df4810])
        raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        print('Hola')
    
st.header('Predicción llamadas contact center')

st.header('Importar ficheros de datos para predecir')

#container = st.beta_container()
#columna1, columna2, columna3 = container.beta_columns(3)


#st.set_page_config(layout="wide")

#st.image('imagen_ruta.jpg',  use_column_width=True)

with st.sidebar:
    clicked = my_widget()
