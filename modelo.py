import joblib
import numpy as np
"""
 'Escuelas de educación primaria del sector publico',
       'Exhibición de películas', 'Hospitales generales del sector privado',
       'educación superior', 'farmacia', 'gasolina', 'hoteles',
       'oxxo', 'starbucks', 'supermercados',
       'CONSTRUCCIÓN(M2)','VALOR ESTIMADO','TERRENO(M2)','Latitud', 'Longitud'
"""

def prediccion( denue:dict,
                construccion:float, valor:float, terreno:float, lat:float,
                long:float):
    vector =[denue["escuelas"], denue["cines"],denue["hospitales"],
             denue["universidad"],denue["farmacia"], denue["gasolina"],
              denue["hoteles"], denue["oxxo"],denue["starbucks"],
               denue["supermercados"], construccion, valor, terreno, lat,long]
    vector = np.reshape(vector,(1,-1))
    modelo = joblib.load("modelo.pkl")
    clase = modelo.predict(vector)[0]
    print(clase)
    return clase
    
