"""
Este programa es una api para calcular la viabilidad de una casa dada su latit, longitud, tamaño de terreno,
tamaño de casa, costo del inmueble. El modelo solo funciona por el momento en cdmx.

La url para mandar la informacion  debe ser de la siguiente forma:
0.0.0.0:5000/datos?long=-99.159155&lat=19.384338&cons=120&val=5500000&terr=100
donde  
    long es longitud
    lat latitud
    cons construccion
    val valor
    terr terreno
"""
from flask import Flask
from flask import request
from flask import jsonify
import app_inegi as apin
from modelo import prediccion
import geopandas as gpd
from shapely.geometry import Point, Polygon

app = Flask(__name__)
radio = 5000 #5km

def checar_flotado(valor):
    """Checamos que se pueda convertir a floats
    Si se puede retorna el string como float, si no
    se puede regresa la cadena (no es un numero)"""
    try:
        return float(valor)
    except:
        return "no es número"


def encontrar_estado(lat:float,long:float):
    """
    En esta función checo que los datos esten dentro
    de la cdmx localizar  el estado estado y retorna la entidad
    """
    df = gpd.read_file("00ent.shp")
    df2 = df.to_crs("epsg:4326")
    punto = Point(long,lat)

    for estado in range(len(df2['CVE_ENT'])):
        """Buscamos en los 32 estados"""
        valor = punto.within(df2.iloc[estado]['geometry'])
        if str(valor) == "True":   
            entidad = str(df.iloc[estado]['CVE_ENT'])
            return entidad
    return "Tus coordenadas no estan en México lo siento"
    



@app.route('/datos', methods=['GET'])
def nuevo():
    Precalificacion = {}
    ###Leemos los datos de la url
    ###Y checamos que sea un numero o que se puedan convertir a floats
    longitud = checar_flotado(request.args.get('long'))
    if longitud == "no es número":
        return "Lo siento tu longitud " + longitud 
    latitud = checar_flotado(request.args.get('lat'))
    if latitud == "no es número":
        return "Lo siento tu latitud " + latitud 
    construccion = checar_flotado(request.args.get('cons'))
    if construccion == "no es número":
        return "Lo siento tu construccion " + construccion 
    valor = checar_flotado(request.args.get('val'))
    if valor == "no es número":
        return "Lo siento tu valor " + valor 
    terreno = checar_flotado(request.args.get('terr'))
    if terreno == "no es número":
        return "Lo siento tu terreno " + terreno
    ###Obtenemos informacion de la denue 
    estado = encontrar_estado(latitud,longitud)
    if estado == "Tus coordenadas no estan en México lo siento":
        return "Tus coordenadas geograficas no estan en México"
    if estado == '09':
        """Solo si esta dentro de la CDMX su calve es 09"""
        datos = apin.lat_long_inegi(latitud,longitud,radio)
        Precalificacion["Precalificacion_aprobada:"] = prediccion(datos,construccion, valor, terreno,latitud,longitud)
        return jsonify(Precalificacion)
    else:
        return "Lo siento el inmueble no esta en CDMX tiene calve de entidad: " + estado
    

if __name__ == '__main__':
 app.run(host='0.0.0.0')

