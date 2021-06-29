import pandas as pd
import numpy as np
import pyodbc
import calendar
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import pickle

def getCallData(password):
    server = 'khcuy9chlt.database.windows.net' 
    bdd = 'ASERTEC' 
    user = 'tecnico@khcuy9chlt' 
    #password = 'xxxxxxxxxxxx'

    query = 'SELECT [IDCAMPANYA] \
          ,[IDSUJETO] \
          ,[VALOR] \
          ,[DATACREACIO] \
        FROM [dbo].[T_CCT_ALISYS_DATOSCLIENTE] \
        WHERE DATACREACIO IS NOT NULL AND DATACREACIO > GETDATE()-15 AND CLAVE = \'LLamadaTipoServicio\''

    conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}',server='tcp:khcuy9chlt.database.windows.net,1433',database=bdd, uid=user, pwd=password)

    df = pd.read_sql_query(query, conn)
    
    df = df[['IDCAMPANYA','VALOR','DATACREACIO']]
    
    df['tCreacion'] = pd.to_datetime(df['DATACREACIO'])

    df['Date'] = df['tCreacion'].dt.date
    df['Date'] = df['Date'].astype('str')

    df['dateCreacion'] = df['tCreacion'].dt.date
    df['dateCreacion'] = df['dateCreacion'].astype('str')
    
    df = df[['Date','dateCreacion','IDCAMPANYA','VALOR']]
    
    df = df.groupby(['Date','IDCAMPANYA','VALOR']).count()
    
    df = df.reset_index()
    
    df = df[(df['VALOR'] == 'Estado de Pedido') | (df['VALOR'] == 'No tiene Numero')]
    
    df = df.groupby('Date').sum()[['dateCreacion']]
    
    return df

def getDataEnvios(df):
    df = df.iloc[:, [0,4,15]]
    df['Fecha envío'] = pd.to_datetime(df['Fecha envío'])
    dias = list(calendar.day_name)
    df['dayofweek'] = [dias[numero] for numero in df['Fecha envío'].dt.dayofweek]
    df['Fecha envío'] =  pd.to_datetime(df['Fecha envío']).astype('str')
    df = df[['Fecha envío','Código servicio','dayofweek']]
    df.reset_index(inplace=True)
    df = df[['Fecha envío','Código servicio','dayofweek']]
    df['total'] = 1
    encoder = OneHotEncoder(handle_unknown='ignore')
    enc = df[['dayofweek']]
    encoder.fit(enc.values.reshape(-1,1))
    encoded = encoder.transform(enc.values.reshape(-1,1))
    encoded_df = pd.DataFrame(encoded.todense())
    encoded_df.columns = encoder.categories_[0]
    df = pd.concat([df,encoded_df], axis=1)
    df.drop(columns=['Código servicio','dayofweek'], inplace=True)
    df = df.groupby(['Fecha envío']).sum()
    df.Monday = [ 1 if value > 0 else 0 for value in df.Monday]
    df.Tuesday = [ 1 if value > 0 else 0 for value in df.Tuesday]
    df.Wednesday = [ 1 if value > 0 else 0 for value in df.Wednesday]
    df.Thursday = [ 1 if value > 0 else 0 for value in df.Thursday]
    df.Friday = [ 1 if value > 0 else 0 for value in df.Friday]
    df.Saturday = [ 1 if value > 0 else 0 for value in df.Saturday]
    df.Sunday = [ 1 if value > 0 else 0 for value in df.Sunday]
    df = df.drop(labels=['Saturday','Sunday'], axis=1)
    
    return df

def dataJoin(df_calls, df_shippins):
    df = pd.concat([df_shippins, df_calls], axis=1).reset_index()
    df['Fecha'] = df['index']
    df.drop('index', axis='columns', inplace=True)
    
    ordenado = ['Fecha', 'total', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'dateCreacion']
    df = df[ordenado]
    
    df.dropna(inplace=True)
    
    return df

def dataEngineering(df):
    # Lags de envios
    df['envioslag1'] = df['total'].shift(periods=1)
    df['envioslag6'] = df['total'].shift(periods=6)
    df['envioslag7'] = df['total'].shift(periods=7)
    df['envioslag8'] = df['total'].shift(periods=8)
    
    #Renombrar por claridad
    df['envios'] = df['total']
    df.drop('total', axis='columns', inplace=True)

    # Datos estacionales
    df['sinlag1'] = np.sin(2*np.pi*(1/1)*df.index)
    df['coslag1'] = np.cos(2*np.pi*(1/1)*df.index)

    df['sinlag2'] = np.sin(2*np.pi*(1/2)*df.index)
    df['coslag2'] = np.cos(2*np.pi*(1/2)*df.index)

    df['sinlag3'] = np.sin(2*np.pi*(1/3)*df.index)
    df['coslag3'] = np.cos(2*np.pi*(1/3)*df.index)

    df['sinlag4'] = np.sin(2*np.pi*(1/4)*df.index)
    df['coslag4'] = np.cos(2*np.pi*(1/4)*df.index)

    df['sinlag5'] = np.sin(2*np.pi*(1/5)*df.index)
    df['coslag5'] = np.cos(2*np.pi*(1/5)*df.index)

    df['sinlag6'] = np.sin(2*np.pi*(1/6)*df.index)
    df['coslag6'] = np.cos(2*np.pi*(1/6)*df.index)

    df['sinlag7'] = np.sin(2*np.pi*(1/7)*df.index)
    df['coslag7'] = np.cos(2*np.pi*(1/7)*df.index)
    
    # Lags de llamadas
    df['llamadaslag1'] = df['dateCreacion'].shift(periods=1)
    df['llamadaslag2'] = df['dateCreacion'].shift(periods=2)
    df['llamadaslag3'] = df['dateCreacion'].shift(periods=3)
    df['llamadaslag4'] = df['dateCreacion'].shift(periods=4)
    df['llamadaslag5'] = df['dateCreacion'].shift(periods=5)
    df['llamadaslag6'] = df['dateCreacion'].shift(periods=6)
    df['llamadaslag7'] = df['dateCreacion'].shift(periods=7)
    
    #Renombrar por claridad
    df['llamadas'] = df['dateCreacion']
    df.drop('dateCreacion', axis='columns', inplace=True)
    
    df.dropna(inplace=True)
    
    df  = df.tail(1).iloc[:,1:-1]
    
    df.reset_index(inplace=True)
    df.drop('index', axis='columns', inplace=True)
    
    return df

def dataScaler(df):
    # Cargar scaler desde Pickle
    scaler_pkl_filename = 'data/scaler.pkl'
    scaler_pkl = open(scaler_pkl_filename, 'rb')
    scaler = pickle.load(scaler_pkl)
    
    df = scaler.transform(df)
    
    return df

def dataPredict(data):
    # Cargar modelo desde Pickle
    regl_pkl_filename = 'data/regl.pkl'
    regl_pkl_model = open(regl_pkl_filename, 'rb')
    regl = pickle.load(regl_pkl_model)
    
    predict = regl.predict(data)
    
    return predict