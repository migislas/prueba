
"""
En este programa vamos a extraer informacion de la api del inegi llamada
DENUE, vamos a buscar informacion relacionada con los siguientes comercios :

    -farmacias
    -oxxo
    -hoteles
    -restaurantes
    -gasolinerias
    -supermercados
    -escuelas
    -hospitales generales del sector privado
    -hospitales generales del sector publico
    -cajero automatico(para conocer los bancos)
    -exhibición de peliculas(para los cines)
    -starbucks

se guarda la informacion en un diccionario llado comercios, las busquedas
se realizan e un radio de distancia de una cierta latitud y longitud, y cuenta
el numero de estos comercios a un cierto radio de la latitud y longitud.
Esta latitud y longitud se determina leyendo el archivo datos_lat_long.py
en este programa solo se guarda el id de la garantia, asi como el numero de los
establecimientos, esto se hace en un archivo de salida llamado: datos_denue_lat.csv
"""
import requests
import json


url = "https://www.inegi.org.mx/app/api/denue/v1/consulta/Buscar/"
#no_comercios_radio   es radio en donde realizaremos la busqueda
api_key = "d972dddf-8216-4bc3-9ad8-6df9f0430b39" #llave de la api otorgada por inegi


#inicio un diccionario global llamado comercios
#solo agrego un key llamado garantia


#Definimos la lista de los diferentes comercios, o claves para obtenerlos
lista_de_comercios = ( 
                        'Escuelas%20de%20educación%20primaria%20del%20sector%20publico',
                        'Exhibición%20de%20películas', 
                        'Hospitales%20generales%20del%20sector%20privado',
                        'educación%20superior', 'farmacia', 'gasolina', 'hoteles',
                        'oxxo', 'starbucks', 'supermercados'                         
                        )





def lat_long_inegi(latitud:float,longitud:float, no_comercios_radio:str)->None:
    print(latitud,longitud)
    comercios_respuesta = {}
    """
    En esta funcion hago las llamadas a la api del inegi,
    para esto utilizo los elementos de latitud y longitud, para usar la api
    esta api tiene el formato:
    url = "https://www.inegi.org.mx/app/api/denue/v1/consulta/Buscar/" +
            entidad economica+ /latitud,longitud/radio de busqueda/api_key
    la latitud y longitud son pasados como argumento en la funcion. Tambien para
    cada latitud y longitud guardo en el diccionarion comercios la id de esa latitud 
    y longitud 
    """
    for elementos in lista_de_comercios:
                
        """
        en el siguiente for recorro todas las unidades economicas de interes
        para cada latitud longitud el numero del elemento de la lista en latitud y
        longitud esta dado por indice_gar"""
        url_final = (url + elementos + "/" + str(latitud) + ","+ str(longitud) +"/"
                                + str(no_comercios_radio) + "/" + api_key )
        print(url_final)
        
        
           
        respuesta = requests.get(url_final) #aqui hacemos el request
        if respuesta.status_code == 200:
            respuesta_json = respuesta.json()
            if elementos == "Hospitales%20generales%20del%20sector%20privado" :
                elementos = "hospitales"
            if elementos == 'Escuelas%20de%20educación%20primaria%20del%20sector%20publico':
                elementos = "escuelas"
            if elementos == "Exhibición%20de%20películas" :
                elementos = "cines"
            if elementos == 'educación%20superior':
                elementos = "universidad"
            comercios_respuesta[elementos] = len(respuesta_json)
        else:
            if elementos == "Hospitales%20generales%20del%20sector%20privado" :
                elementos = "hospitales"
            if elementos == 'Escuelas%20de%20educación%20primaria%20del%20sector%20publico':
                elementos = "escuelas"
            if elementos == "Exhibición%20de%20películas" :
                elementos = "cines"
            if elementos == 'educación%20superior':
                elementos = "universidad"
            comercios_respuesta[elementos] = 0

      
       
    return comercios_respuesta
    

        
      
            






