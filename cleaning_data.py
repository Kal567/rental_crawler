import csv
import os
import pymongo

client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
#database name
db = client["publicaciones"]
# Collection Name
col_corotos = db["corotos"]
col_mercadolibre = db["publicaciones_mercadolibre"]
col_supercasas = db["supercasas"]
col_santo_domingo = db["santo_domingo"]

#amenities - 29
banos,agua_potable,aire_acondicionado,area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,terraza,vestidores,walk_in_closet = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

#amenities = col.find({},{'0':1, '1':1, '1':1, '2':1, '3':1, '4':1, '5':1, '6':1, '8':1, '9':1, '12':1, '17':1, '18':1, '19':1})
#_data_supercasas = col_supercasas.find({},{'price_DOP':1, 'rooms':1, 'bathrooms':1, 'square_footage':1, 'province':1, 'amenities':1})
#_data_corotos = col_corotos.find({},{'price_DOP':1, 'rooms':1, 'bathrooms':1, 'square_footage':1, 'province':1, 'amount_amenities':1})
#_data_corotos = col_corotos.find({},{'3':1, '12':1, '13':1, '15':1, 
#                                     '10':1, '18':1})
#_data_frontend = col_supercasas.find({}, {'website':1,'link':1,'price_crawled':1,'price_DOP':1,
#                                          'title':1,'rooms':1,'bathrooms':1,'location_crawled':1,
#                                          'sector':1,'province':1,'condition':1,'current_use':1,
#                                          'square_footage':1,'floor':1,'elevator':1,'buildable':1,
#                                          'construction_year':1,'amenities':1,'amount_amenities':1,
#                                          'image_link':1})

_data_frontend = col_supercasas.find({}, {'0':1,'1':1,'2':1,'3':1,
                                          '4':1,'5':1,'6':1,'7':1,
                                          '8':1,'9':1,'10':1,'11':1,
                                          '12':1,'13':1,'14':1,'15':1,
                                          '16':1,'17':1,'18':1,
                                          '19':1})

_supercasas = col_supercasas.find({}, 
                                  {'website':1,'link':1,'price_crawled':1,'price_DOP':1,
                                  'title':1,'rooms':1,'bathrooms':1,'location_crawled':1,
                                  'sector':1,'province':1,'square_footage':1,'amenities':1,
                                  'amount_amenities':1,'image_link':1})

_corotos = col_corotos.find({}, 
                           {'website':1,'link':1,'price_crawled':1,'price_DOP':1,
                            'title':1,'rooms':1,'bathrooms':1,'location_crawled':1,
                            'sector_from_location':1,'province':1,'square_footage':1,
                            'amenities_description':1,'amount_amenities':1,'image_link':1})

_santo_domingo = col_santo_domingo.find({}, 
                           {'website':1,'link':1,'price_crawled':1,'price_DOP':1,
                            'title':1,'rooms':1,'bathrooms':1,'location_crawled':1,
                            'sector':1,'province':1,'square_footage':1,
                            'amenities':1,'amount_amenities':1,'image_link':1})

#'website':1, 'link':1, 'price_crawled':1, 'price_DOP':1, 'date_crawled':1, 'day_upload':1,
#                                 'month_upload':1, 'year_upload':1, 'title':1, 'location_crawled':1, 'sector_from_location':1, 
#                                 'province':1,'tipo':1, 'rooms':1, 'other_specs':1, 'square_footage':1, 'half_bathrooms':1,
#                                 'sector_from_specs':1, 'amenities_description':1, 'amount_amenities':1})

DATA = []

TD_ALTAGRACIA = "training_data_altagracia.csv"
TD_ROMANA = "training_data_romana.csv"
TD_SANPEDRO = "training_data_sanpedromacoris.csv"
TD_SANTIGO = "training_data_santiago.csv"
TD_SANTODOMINGO = "training_data_santodomingo.csv"

#website,link,price_crawled,price_DOP,date_crawled,day_upload,month_upload,year_upload,title,location_crawled,sector_from_location,province,tipo,rooms,bathrooms,other_specs,square_footage,half_bathrooms,sector_from_specs,amenities_description,amount_amenities
AMENITIES_FILE = "amenities.csv"
COROTOS_FILE = "cleaned_data_corotos.csv"
MERCADOLIBRE_FILE = "cleaned_data_mercadolibre.csv"
SUPERCASAS_FILE = "cleaned_data_supercasas.csv"

def save_to_csv_file_amenities(data_array, file):
    for line in data_array:
        with open(file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([line])

def get_csv_to_array_amenities():
    with open(AMENITIES_FILE) as f:
        reader = csv.reader(f)
        lst = list(reader)
    return [item for sublist in lst for item in sublist]

def get_first_line_csv_on_queue(file):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        return next(reader)[0]
    
def save_to_csv_file(data_array, csv_file_name):
    with open(csv_file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_array)

def remove_first_csv_line(file):
    try:
        with open(file, 'r+') as fp:
                lines = fp.readlines()
                if len(lines) > 0:
                    fp.seek(0)
                    fp.truncate()
                    fp.writelines(lines[1:])                    
    except:
        return


def save_to_csv_file(data_array, csv_file_name):
    with open(csv_file_name, 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data_array)


def save_supercasas():
    for d in _data_supercasas:
        if(d['square_footage'] != 0):
            correctDOP = (d['price_DOP'] / 56.7531) * 55.25
            save_to_csv_file([correctDOP, d['rooms'], d['bathrooms'], d['square_footage'], d['province'],d['amount_amenities']], SUPERCASAS_FILE)
        
def clean_corotos():
    for d in _data_corotos:
        year = d['date_crawled'][-4:]
        save_to_csv_file([d['website'], d['link'], d['price_crawled'], d['price_DOP'], d['date_crawled'],d['day_upload'],
                          d['month_upload'], year, d['year_upload'], d['title'], d['location_crawled'], d['sector_from_location'],d['province'],
                          d['tipo'], d['rooms'], d['square_footage'], d['other_specs'], d['half_bathrooms'],
                          d['amenities_description'], d['amount_amenities']], COROTOS_FILE)

def corotos_to_training():
    for d in _data_corotos:
        if(d['square_footage'] > 1):
            correctDOP = (d['price_DOP'] / 56.7531) * 55.25
            #correctDOP, d['rooms'], d['bathrooms'], d['square_footage'], d['province'],d['amount_amenities']
            save_to_csv_file([correctDOP, d['rooms'], d['bathrooms'], d['square_footage'], d['province'],d['amount_amenities']], "training_data.csv")

def dividing_csv_by_province():
    for d in _data_corotos:
        if(d['square_footage'] > 1):
            correctDOP = (d['price_DOP'] / 56.7531) * 55.25
            if("Santo Domingo" in d['province']):
                save_to_csv_file([correctDOP, d['rooms'], d['bathrooms'], 
                                  d['square_footage'], d['province'],d['amount_amenities']], TD_SANTODOMINGO)
            if("Santiago" in d['province'] or "Santiago de los Caballeros" in d['province']):
                save_to_csv_file([correctDOP, d['rooms'], d['bathrooms'], 
                                  d['square_footage'], 'Santiago',d['amount_amenities']], TD_SANTIGO)
            if("La Altagracia" in d['province']):
                save_to_csv_file([correctDOP, d['rooms'], d['bathrooms'], 
                                  d['square_footage'], d['province'],d['amount_amenities']], TD_ALTAGRACIA)
            if("La Romana" in d['province']):
                save_to_csv_file([correctDOP, d['rooms'], d['bathrooms'], 
                                  d['square_footage'], d['province'],d['amount_amenities']], TD_ROMANA)
            if("San Pedro de Macor" in d['province']):
                save_to_csv_file([correctDOP, d['rooms'], d['bathrooms'], 
                                  d['square_footage'], 'San Pedro de Macoris',d['amount_amenities']], TD_SANPEDRO)

def sort_amenities(_data_array):
    for d in _data_array:
        print(d['square_footage'])
        if(d['square_footage'] > 1):
            correctDOP = (d['price_DOP'] / 56.7531) * 54.04
            banos,agua_potable,aire_acondicionado,area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,terraza,vestidores = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            province_id = 0
            #sort provinces
            if("Santo Domingo" in d['province']):
                province_id = 5
            if("Santiago" in d['province'] or "Santiago de los Caballeros" in d['province']):
                province_id = 4
            if("La Altagracia" in d['province']):
                province_id = 3
            if("La Romana" in d['province']):
                province_id = 2
            if("San Pedro de Macor" in d['province']):
                province_id = 1

            #amenities
            if("1/2 Ba" in d['amenities'] or "Baños" in d['amenities'] or "Ba�os" in d['amenities']):
                banos = 1
            if("Agua Potable" in d['amenities']):
                agua_potable = 1
            if("Aire Acondicionado" in d['amenities']):
                aire_acondicionado = 1
            if("Area de Juegos Infantiles" in d['amenities'] or "Juegos Infantiles" in d['amenities']):
                area_juegos_infantiles = 1
            if("Area Servicio"  in d['amenities'] or "Area de Servicio" in d['amenities']):
                area_servicio = 1
            if("Ascensor" in d['amenities'] or "Elevador" in d['amenities']):
                ascensor = 1
            if("Balcon" in d['amenities'] or "Balcón" in d['amenities'] or "Balc�n" in d['amenities']):
                balcon = 1
            if("Cisterna" in d['amenities']):
                cisterna = 1
            if("Control de Acceso" in d['amenities'] or "Control Acceso" in d['amenities'] or 
               "Control Aceso" in d['amenities'] or "Control de Aceso" in d['amenities']):
                control_acceso = 1
            if("Cuarto de Servicio" in d['amenities'] or "Cuarto Servicio" in d['amenities'] or 
               "Habitacion Servicio" in d['amenities'] or "Habitacion de Servicio" in d['amenities'] or
               "Habitaci�n Servicio" in d['amenities'] or "Habitaci�n de Servicio" in d['amenities'] or
               "Cuarto de Servisio" in d['amenities'] or "Cuarto Servisio" in d['amenities'] or 
               "Habitacion Servisio" in d['amenities'] or "Habitacion de Servisio" in d['amenities'] or
               "Habitaci�n Servisio" in d['amenities'] or "Habitaci�n de Servisio" in d['amenities'] or
               "Cuarto de Serbicio" in d['amenities'] or "Cuarto Serbicio" in d['amenities'] or 
               "Habitacion Serbicio" in d['amenities'] or "Habitacion de Serbicio" in d['amenities'] or
               "Habitaci�n Serbicio" in d['amenities'] or "Habitaci�n de Serbicio" in d['amenities'] or
               "Cuarto de Serbisio" in d['amenities'] or "Cuarto Serbisio" in d['amenities'] or 
               "Habitacion Serbisio" in d['amenities'] or "Habitacion de Serbisio" in d['amenities'] or
               "Habitaci�n Serbisio" in d['amenities'] or "Habitaci�n de Serbisio" in d['amenities']):
                cuarto_servicio = 1
            if("Estar Familiar" in d['amenities'] or "Sala de Estar" in d['amenities'] or 
               "Sala de Estar Familiar" in d['amenities'] or "Sala Estar Familiar" in d['amenities'] or
               "Sala Familiar" in d['amenities'] or "Family Room" in d['amenities']):
                estar_familiar = 1
            if("Estudio" in d['amenities']):
                estudio = 1
            if("Gazebo" in d['amenities'] or "Gasebo" in d['amenities'] or "Gazevo" in d['amenities'] or
               "Gasevo" in d['amenities']):
                gazebo = 1
            if("Gimnasio" in d['amenities'] or "Gim" in d['amenities'] or "Gym" in d['amenities']):
                gimnasio = 1
            if("Inversor" in d['amenities'] or "Inbersor" in d['amenities'] or
               "Inverzor" in d['amenities'] or "Inberzor" in d['amenities']):
                inversor = 1
            if("Jacuzzi" in d['amenities'] or "Jacuzi" in d['amenities'] or "Jacussi" in d['amenities'] or
               "Jacusi" in d['amenities']):
                jacuzzi = 1
            if("Lobby" in d['amenities'] or "Loby" in d['amenities']):
                lobby = 1
            if("Patio" in d['amenities']):
                patio = 1
            if("Picuzzi" in d['amenities'] or "Picuzi" in d['amenities'] or "Picussi" in d['amenities'] or
               "Pucusi" in d['amenities']):
                picuzzi
            if("Piscina" in d['amenities'] or "Picina" in d['amenities'] or "Pisina" in d['amenities']):
                piscina = 1
            if("Planta Eléctrica" in d['amenities'] or "Planta Electrica" in d['amenities'] or
               "Planta El�ctrica" in d['amenities']):
                planta_electrica = 1
            if("Pozo" in d['amenities'] or "Poso" in d['amenities']):
                pozo = 1
            if("Satélite" in d['amenities'] or "Satelite" in d['amenities'] or "Sat�lite" in d['amenities']):
                satelite = 1
            if("Sauna" in d['amenities']):
                sauna = 1
            if("Seguridad 24 Horas" in d['amenities'] or "Seguridad" in d['amenities'] or
               "24 Horas de Seguridad" in d['amenities'] or "24 Horas Seguridad" or
               "Seguridad las 24 Horas" in d['amenities'] or "protect" in d['amenities']):
                seguridad = 1
            if("Shutters" in d['amenities'] or "Shuters" in d['amenities'] or "Shutter" in d['amenities'] or
               "Shuter" in d['amenities'] or "Persianas" in d['amenities'] or "Persiana" in d['amenities'] or
               "Perciana" in d['amenities']):
                shutters = 1
            if("Terraza" in d['amenities'] or "Terrasa" in d['amenities'] or "Teraza" in d['amenities'] or
               "Terasa" in d['amenities']):
                terraza = 1
            if("Vestidores" in d['amenities'] or "Vestidor" in d['amenities'] or "Bestidor" in d['amenities'] or
               "Walk In Closet" in d['amenities'] or "WalkIn Closet" in d['amenities'] or 
               "walkin-closet" in d['amenities'] or "walking closet" in d['amenities']):
                vestidores = 1
            save_to_csv_file([correctDOP, d['rooms'], d['bathrooms'], d['square_footage'], 
                                province_id,banos,agua_potable,aire_acondicionado,
                                area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,
                                cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,
                                patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,
                                terraza,vestidores], "cleaned_data.csv")

def sort_amenities_new(_data_array, 
                       square_footage, rooms, bathrooms, price, province, amenities):
    for d in _data_array:
        if(d[square_footage] > 1):
            correctDOP = (d[price] / 56.7531) * 54.04
            if(correctDOP < 1000000):
                banos,agua_potable,aire_acondicionado,area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,terraza,vestidores = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                province_id = 0
                #sort provinces
                if("Santo Domingo" in d[province]):
                    province_id = 5
                if("Santiago" in d[province] or "Santiago de los Caballeros" in d[province]):
                    province_id = 4
                if("La Altagracia" in d[province]):
                    province_id = 3
                if("La Romana" in d[province]):
                    province_id = 2
                if("San Pedro de Macor" in d[province]):
                    province_id = 1

                #amenities
                if("1/2 Ba" in d[amenities] or "Baños" in d[amenities] or "Ba�os" in d[amenities]):
                    banos = 1
                if("Agua Potable" in d[amenities]):
                    agua_potable = 1
                if("Aire Acondicionado" in d[amenities]):
                    aire_acondicionado = 1
                if("Area de Juegos Infantiles" in d[amenities] or "Juegos Infantiles" in d[amenities]):
                    area_juegos_infantiles = 1
                if("Area Servicio"  in d[amenities] or "Area de Servicio" in d[amenities]):
                    area_servicio = 1
                if("Ascensor" in d[amenities] or "Elevador" in d[amenities]):
                    ascensor = 1
                if("Balcon" in d[amenities] or "Balcón" in d[amenities] or "Balc�n" in d[amenities]):
                    balcon = 1
                if("Cisterna" in d[amenities]):
                    cisterna = 1
                if("Control de Acceso" in d[amenities] or "Control Acceso" in d[amenities] or 
                "Control Aceso" in d[amenities] or "Control de Aceso" in d[amenities]):
                    control_acceso = 1
                if("Cuarto de Servicio" in d[amenities] or "Cuarto Servicio" in d[amenities] or 
                "Habitacion Servicio" in d[amenities] or "Habitacion de Servicio" in d[amenities] or
                "Habitaci�n Servicio" in d[amenities] or "Habitaci�n de Servicio" in d[amenities] or
                "Cuarto de Servisio" in d[amenities] or "Cuarto Servisio" in d[amenities] or 
                "Habitacion Servisio" in d[amenities] or "Habitacion de Servisio" in d[amenities] or
                "Habitaci�n Servisio" in d[amenities] or "Habitaci�n de Servisio" in d[amenities] or
                "Cuarto de Serbicio" in d[amenities] or "Cuarto Serbicio" in d[amenities] or 
                "Habitacion Serbicio" in d[amenities] or "Habitacion de Serbicio" in d[amenities] or
                "Habitaci�n Serbicio" in d[amenities] or "Habitaci�n de Serbicio" in d[amenities] or
                "Cuarto de Serbisio" in d[amenities] or "Cuarto Serbisio" in d[amenities] or 
                "Habitacion Serbisio" in d[amenities] or "Habitacion de Serbisio" in d[amenities] or
                "Habitaci�n Serbisio" in d[amenities] or "Habitaci�n de Serbisio" in d[amenities]):
                    cuarto_servicio = 1
                if("Estar Familiar" in d[amenities] or "Sala de Estar" in d[amenities] or 
                "Sala de Estar Familiar" in d[amenities] or "Sala Estar Familiar" in d[amenities] or
                "Sala Familiar" in d[amenities] or "Family Room" in d[amenities]):
                    estar_familiar = 1
                if("Estudio" in d[amenities]):
                    estudio = 1
                if("Gazebo" in d[amenities] or "Gasebo" in d[amenities] or "Gazevo" in d[amenities] or
                "Gasevo" in d[amenities]):
                    gazebo = 1
                if("Gimnasio" in d[amenities] or "Gim" in d[amenities] or "Gym" in d[amenities]):
                    gimnasio = 1
                if("Inversor" in d[amenities] or "Inbersor" in d[amenities] or
                "Inverzor" in d[amenities] or "Inberzor" in d[amenities]):
                    inversor = 1
                if("Jacuzzi" in d[amenities] or "Jacuzi" in d[amenities] or "Jacussi" in d[amenities] or
                "Jacusi" in d[amenities]):
                    jacuzzi = 1
                if("Lobby" in d[amenities] or "Loby" in d[amenities]):
                    lobby = 1
                if("Patio" in d[amenities]):
                    patio = 1
                if("Picuzzi" in d[amenities] or "Picuzi" in d[amenities] or "Picussi" in d[amenities] or
                "Pucusi" in d[amenities]):
                    picuzzi
                if("Piscina" in d[amenities] or "Picina" in d[amenities] or "Pisina" in d[amenities]):
                    piscina = 1
                if("Planta Eléctrica" in d[amenities] or "Planta Electrica" in d[amenities] or
                "Planta El�ctrica" in d[amenities]):
                    planta_electrica = 1
                if("Pozo" in d[amenities] or "Poso" in d[amenities]):
                    pozo = 1
                if("Satélite" in d[amenities] or "Satelite" in d[amenities] or "Sat�lite" in d[amenities]):
                    satelite = 1
                if("Sauna" in d[amenities]):
                    sauna = 1
                if("Seguridad 24 Horas" in d[amenities] or "Seguridad" in d[amenities] or
                "24 Horas de Seguridad" in d[amenities] or "24 Horas Seguridad" or
                "Seguridad las 24 Horas" in d[amenities] or "protect" in d[amenities]):
                    seguridad = 1
                if("Shutters" in d[amenities] or "Shuters" in d[amenities] or "Shutter" in d[amenities] or
                "Shuter" in d[amenities] or "Persianas" in d[amenities] or "Persiana" in d[amenities] or
                "Perciana" in d[amenities]):
                    shutters = 1
                if("Terraza" in d[amenities] or "Terrasa" in d[amenities] or "Teraza" in d[amenities] or
                "Terasa" in d[amenities]):
                    terraza = 1
                if("Vestidores" in d[amenities] or "Vestidor" in d[amenities] or "Bestidor" in d[amenities] or
                "Walk In Closet" in d[amenities] or "WalkIn Closet" in d[amenities] or 
                "walkin-closet" in d[amenities] or "walking closet" in d[amenities]):
                    vestidores = 1
                save_to_csv_file([correctDOP, d[rooms], d[bathrooms], d[square_footage], 
                                    province_id,banos,agua_potable,aire_acondicionado,
                                    area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,
                                    cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,
                                    patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,
                                    terraza,vestidores], "cleaned_data.csv")
                
def sort_amenities_new_frontend(_data_array, website, link, price_crawled, price,
                                title, rooms, bathrooms, location_crawled,
                                sector, province, condition, current_use, 
                                square_footage, floor, elevator, buildable_str,
                                construction_year, amenities, amount_amenities,
                                image_link):
    for d in _data_array:
        if(d[square_footage] > 1):
            correctDOP = (d[price] / 56.7531) * 54.56
            if(correctDOP < 1000000):
                banos,agua_potable,aire_acondicionado,area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,terraza,vestidores = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                #sort provinces
                if("Santo Domingo" in d[province]):
                    province_id = 5
                if("Santiago" in d[province] or "Santiago de los Caballeros" in d[province]):
                    province_id = 2
                if("La Altagracia" in d[province]):
                    province_id = 1.5
                if("La Romana" in d[province]):
                    province_id = 1
                if("San Pedro de Macor" in d[province]):
                    province_id = 0.5

                buildable = 0
                if('S�' in d[buildable_str] or 'Si' in d[buildable_str] or 'S' in d[buildable_str]):
                    buildable = 1
                #amenities
                if("1/2 Ba" in d[amenities] or "Baños" in d[amenities] or "Ba�os" in d[amenities]):
                    banos = 1
                if("Agua Potable" in d[amenities]):
                    agua_potable = 1
                if("Aire Acondicionado" in d[amenities]):
                    aire_acondicionado = 1
                if("Area de Juegos Infantiles" in d[amenities] or "Juegos Infantiles" in d[amenities]):
                    area_juegos_infantiles = 1
                if("Area Servicio"  in d[amenities] or "Area de Servicio" in d[amenities]):
                    area_servicio = 1
                if("Ascensor" in d[amenities] or "Elevador" in d[amenities]):
                    ascensor = 1
                if("Balcon" in d[amenities] or "Balcón" in d[amenities] or "Balc�n" in d[amenities]):
                    balcon = 1
                if("Cisterna" in d[amenities]):
                    cisterna = 1
                if("Control de Acceso" in d[amenities] or "Control Acceso" in d[amenities] or 
                "Control Aceso" in d[amenities] or "Control de Aceso" in d[amenities]):
                    control_acceso = 1
                if("Cuarto de Servicio" in d[amenities] or "Cuarto Servicio" in d[amenities] or 
                "Habitacion Servicio" in d[amenities] or "Habitacion de Servicio" in d[amenities] or
                "Habitaci�n Servicio" in d[amenities] or "Habitaci�n de Servicio" in d[amenities] or
                "Cuarto de Servisio" in d[amenities] or "Cuarto Servisio" in d[amenities] or 
                "Habitacion Servisio" in d[amenities] or "Habitacion de Servisio" in d[amenities] or
                "Habitaci�n Servisio" in d[amenities] or "Habitaci�n de Servisio" in d[amenities] or
                "Cuarto de Serbicio" in d[amenities] or "Cuarto Serbicio" in d[amenities] or 
                "Habitacion Serbicio" in d[amenities] or "Habitacion de Serbicio" in d[amenities] or
                "Habitaci�n Serbicio" in d[amenities] or "Habitaci�n de Serbicio" in d[amenities] or
                "Cuarto de Serbisio" in d[amenities] or "Cuarto Serbisio" in d[amenities] or 
                "Habitacion Serbisio" in d[amenities] or "Habitacion de Serbisio" in d[amenities] or
                "Habitaci�n Serbisio" in d[amenities] or "Habitaci�n de Serbisio" in d[amenities]):
                    cuarto_servicio = 1
                if("Estar Familiar" in d[amenities] or "Sala de Estar" in d[amenities] or 
                "Sala de Estar Familiar" in d[amenities] or "Sala Estar Familiar" in d[amenities] or
                "Sala Familiar" in d[amenities] or "Family Room" in d[amenities]):
                    estar_familiar = 1
                if("Estudio" in d[amenities]):
                    estudio = 1
                if("Gazebo" in d[amenities] or "Gasebo" in d[amenities] or "Gazevo" in d[amenities] or
                "Gasevo" in d[amenities]):
                    gazebo = 1
                if("Gimnasio" in d[amenities] or "Gim" in d[amenities] or "Gym" in d[amenities]):
                    gimnasio = 1
                if("Inversor" in d[amenities] or "Inbersor" in d[amenities] or
                "Inverzor" in d[amenities] or "Inberzor" in d[amenities]):
                    inversor = 1
                if("Jacuzzi" in d[amenities] or "Jacuzi" in d[amenities] or "Jacussi" in d[amenities] or
                "Jacusi" in d[amenities]):
                    jacuzzi = 1
                if("Lobby" in d[amenities] or "Loby" in d[amenities]):
                    lobby = 1
                if("Patio" in d[amenities]):
                    patio = 1
                if("Picuzzi" in d[amenities] or "Picuzi" in d[amenities] or "Picussi" in d[amenities] or
                "Pucusi" in d[amenities]):
                    picuzzi
                if("Piscina" in d[amenities] or "Picina" in d[amenities] or "Pisina" in d[amenities]):
                    piscina = 1
                if("Planta Eléctrica" in d[amenities] or "Planta Electrica" in d[amenities] or
                "Planta El�ctrica" in d[amenities]):
                    planta_electrica = 1
                if("Pozo" in d[amenities] or "Poso" in d[amenities]):
                    pozo = 1
                if("Satélite" in d[amenities] or "Satelite" in d[amenities] or "Sat�lite" in d[amenities]):
                    satelite = 1
                if("Sauna" in d[amenities]):
                    sauna = 1
                if("Seguridad 24 Horas" in d[amenities] or "Seguridad" in d[amenities] or
                "24 Horas de Seguridad" in d[amenities] or "24 Horas Seguridad" or
                "Seguridad las 24 Horas" in d[amenities] or "protect" in d[amenities]):
                    seguridad = 1
                if("Shutters" in d[amenities] or "Shuters" in d[amenities] or "Shutter" in d[amenities] or
                "Shuter" in d[amenities] or "Persianas" in d[amenities] or "Persiana" in d[amenities] or
                "Perciana" in d[amenities]):
                    shutters = 1
                if("Terraza" in d[amenities] or "Terrasa" in d[amenities] or "Teraza" in d[amenities] or
                "Terasa" in d[amenities]):
                    terraza = 1
                if("Vestidores" in d[amenities] or "Vestidor" in d[amenities] or "Bestidor" in d[amenities] or
                "Walk In Closet" in d[amenities] or "WalkIn Closet" in d[amenities] or 
                "walkin-closet" in d[amenities] or "walking closet" in d[amenities]):
                    vestidores = 1
                save_to_csv_file([d[website],d[link],d[price_crawled],correctDOP,
                    d[title],d[rooms],d[bathrooms],d[location_crawled],
                    d[sector],d[province],d[condition],d[current_use],
                    d[square_footage],d[floor],d[elevator],buildable,
                    d[construction_year],d[amenities],d[amount_amenities],
                    d[image_link],banos,agua_potable,aire_acondicionado,
                    area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,
                    cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,
                    patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,
                    terraza,vestidores], "cleaned_data_supercasas.csv")
                save_to_csv_file([correctDOP,d[rooms],d[bathrooms],d[square_footage],
                    province_id,banos,agua_potable,aire_acondicionado,
                    area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,
                    cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,
                    patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,
                    terraza,vestidores], "cleaned_data.csv")

#89166.0,1.0,1.5,78.0,5,1,1,1,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,0,1,1,0,0,0,1,0,0,1
#sort_amenities_new(_data_corotos, '15', '12', '13', '3', '10', '18')
#sort_amenities_new(_data_array, square_footage, rooms, bathrooms, price, province, amenities):
#'price_DOP':1, 'rooms':1, 'bathrooms':1, 'square_footage':1, 'province':1, 'amenities':1})
#sort_amenities_new(_data_supercasas, 'square_footage', 'rooms', 'bathrooms', 'price_DOP', 'province', 'amenities')
#sort_amenities_new_frontend(_data_frontend, 'square_footage', 'price_DOP', 'amenities', 'buildable')
#sort_amenities_new_frontend(_data_frontend, '0', '1', '2', '3', '4', '5','6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19')

#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################


def clean_santo_domingo(_data_array, price,
                        rooms, bathrooms,
                        square_footage, 
                        amenities, amount_amenities):
    for d in _data_array:
        if(d[square_footage] > 1):
            #if(d[price] < 1000000):
            banos,agua_potable,aire_acondicionado,area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,terraza,vestidores = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            if("1/2 Ba" in d[amenities] or "Baños" in d[amenities] or "Ba�os" in d[amenities]):
                banos = 1
            if("Agua Potable" in d[amenities]):
                agua_potable = 1
            if("Aire Acondicionado" in d[amenities]):
                aire_acondicionado = 1
            if("Area de Juegos Infantiles" in d[amenities] or "Juegos Infantiles" in d[amenities]):
                area_juegos_infantiles = 1
            if("Area Servicio"  in d[amenities] or "Area de Servicio" in d[amenities]):
                area_servicio = 1
            if("Ascensor" in d[amenities] or "Elevador" in d[amenities]):
                ascensor = 1
            if("Balcon" in d[amenities] or "Balcón" in d[amenities] or "Balc�n" in d[amenities]):
                balcon = 1
            if("Cisterna" in d[amenities]):
                cisterna = 1
            if("Control de Acceso" in d[amenities] or "Control Acceso" in d[amenities] or 
            "Control Aceso" in d[amenities] or "Control de Aceso" in d[amenities]):
                control_acceso = 1
            if("Cuarto de Servicio" in d[amenities] or "Cuarto Servicio" in d[amenities] or 
            "Habitacion Servicio" in d[amenities] or "Habitacion de Servicio" in d[amenities] or
            "Habitaci�n Servicio" in d[amenities] or "Habitaci�n de Servicio" in d[amenities] or
            "Cuarto de Servisio" in d[amenities] or "Cuarto Servisio" in d[amenities] or 
            "Habitacion Servisio" in d[amenities] or "Habitacion de Servisio" in d[amenities] or
            "Habitaci�n Servisio" in d[amenities] or "Habitaci�n de Servisio" in d[amenities] or
            "Cuarto de Serbicio" in d[amenities] or "Cuarto Serbicio" in d[amenities] or 
            "Habitacion Serbicio" in d[amenities] or "Habitacion de Serbicio" in d[amenities] or
            "Habitaci�n Serbicio" in d[amenities] or "Habitaci�n de Serbicio" in d[amenities] or
            "Cuarto de Serbisio" in d[amenities] or "Cuarto Serbisio" in d[amenities] or 
            "Habitacion Serbisio" in d[amenities] or "Habitacion de Serbisio" in d[amenities] or
            "Habitaci�n Serbisio" in d[amenities] or "Habitaci�n de Serbisio" in d[amenities]):
                cuarto_servicio = 1
            if("Estar Familiar" in d[amenities] or "Sala de Estar" in d[amenities] or 
            "Sala de Estar Familiar" in d[amenities] or "Sala Estar Familiar" in d[amenities] or
            "Sala Familiar" in d[amenities] or "Family Room" in d[amenities]):
                estar_familiar = 1
            if("Estudio" in d[amenities]):
                estudio = 1
            if("Gazebo" in d[amenities] or "Gasebo" in d[amenities] or "Gazevo" in d[amenities] or
            "Gasevo" in d[amenities]):
                gazebo = 1
            if("Gimnasio" in d[amenities] or "Gim" in d[amenities] or "Gym" in d[amenities]):
                gimnasio = 1
            if("Inversor" in d[amenities] or "Inbersor" in d[amenities] or
            "Inverzor" in d[amenities] or "Inberzor" in d[amenities]):
                inversor = 1
            if("Jacuzzi" in d[amenities] or "Jacuzi" in d[amenities] or "Jacussi" in d[amenities] or
            "Jacusi" in d[amenities]):
                jacuzzi = 1
            if("Lobby" in d[amenities] or "Loby" in d[amenities]):
                lobby = 1
            if("Patio" in d[amenities]):
                patio = 1
            if("Picuzzi" in d[amenities] or "Picuzi" in d[amenities] or "Picussi" in d[amenities] or
            "Pucusi" in d[amenities]):
                picuzzi
            if("Piscina" in d[amenities] or "Picina" in d[amenities] or "Pisina" in d[amenities]):
                piscina = 1
            if("Planta Eléctrica" in d[amenities] or "Planta Electrica" in d[amenities] or
            "Planta El�ctrica" in d[amenities]):
                planta_electrica = 1
            if("Pozo" in d[amenities] or "Poso" in d[amenities]):
                pozo = 1
            if("Satélite" in d[amenities] or "Satelite" in d[amenities] or "Sat�lite" in d[amenities]):
                satelite = 1
            if("Sauna" in d[amenities]):
                sauna = 1
            if("Seguridad 24 Horas" in d[amenities] or "Seguridad" in d[amenities] or
            "24 Horas de Seguridad" in d[amenities] or "24 Horas Seguridad" or
            "Seguridad las 24 Horas" in d[amenities] or "protect" in d[amenities]):
                seguridad = 1
            if("Shutters" in d[amenities] or "Shuters" in d[amenities] or "Shutter" in d[amenities] or
            "Shuter" in d[amenities] or "Persianas" in d[amenities] or "Persiana" in d[amenities] or
            "Perciana" in d[amenities]):
                shutters = 1
            if("Terraza" in d[amenities] or "Terrasa" in d[amenities] or "Teraza" in d[amenities] or
            "Terasa" in d[amenities]):
                terraza = 1
            if("Vestidores" in d[amenities] or "Vestidor" in d[amenities] or "Bestidor" in d[amenities] or
            "Walk In Closet" in d[amenities] or "WalkIn Closet" in d[amenities] or 
            "walkin-closet" in d[amenities] or "walking closet" in d[amenities]):
                vestidores = 1

            save_to_csv_file([d[price],d[amount_amenities],
                d[rooms],d[bathrooms],
                d[square_footage],#d[amount_amenities],
                banos,agua_potable,aire_acondicionado,
                area_juegos_infantiles,area_servicio,ascensor,balcon,cisterna,control_acceso,
                cuarto_servicio,estar_familiar,estudio,gazebo,gimnasio,inversor,jacuzzi,lobby,
                patio,picuzzi,piscina,planta_electrica,pozo,satelite,sauna,seguridad,shutters,
                terraza,vestidores], "SD_supercasas_corotos_CLEAN.csv")

#getting all corotos and supercasas Santo Domingo samples
def get_province_samples(_data_array, website,link,price_crawled,
                         price_DOP,title,rooms,bathrooms,
                        location_crawled,sector,province,square_footage,amenities,
                        amount_amenities,image_link):
    for d in _data_array:
        if(d[square_footage] > 1):
            correctDOP = (d[price_DOP] / 56.7531) * 54.84
            if("Santo Domingo" in d[province]):#correctDOP < 1000000 and 
                save_to_csv_file([d[website],d[link],d[price_crawled],correctDOP,
                    d[title],d[rooms],d[bathrooms],d[location_crawled],
                    d[sector],d[province],
                    d[square_footage],d[amenities],d[amount_amenities],
                    d[image_link]], "SD_supercasas_corotos.csv")

#clean_santo_domingo(_santo_domingo, 'price_DOP',
#                                'rooms', 'bathrooms','square_footage', 
#                                'amenities', 'amount_amenities')

get_province_samples(_supercasas, 'website','link','price_crawled','price_DOP',
                                  'title','rooms','bathrooms','location_crawled',
                                  'sector','province','square_footage','amenities',
                                  'amount_amenities','image_link')

get_province_samples(_corotos, 'website','link','price_crawled','price_DOP',
                            'title','rooms','bathrooms','location_crawled',
                            'sector_from_location','province','square_footage',
                            'amenities_description','amount_amenities','image_link')   
                