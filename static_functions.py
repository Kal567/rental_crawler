from datetime import datetime, timedelta
import pytz
import csv
import numpy as np

USD_to_DOP_EXCHANGE_RATE = 56.7531
months = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}

days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
CAPITAL_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#============================CVS AND TXT FILES MANAGERS==========================================

def save_to_csv_file(data_array, csv_file_name):
    with open(csv_file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_array)

def get_txt_file(txt_file_name):
    with open(txt_file_name) as f:
        lines = f.readlines()
    return lines

def set_txt_file(txt_file_name, message):
    with open(txt_file_name, "w") as f:
        f.write(message)


#======================================================================

#--------------------------------SUPERCASAS----------------------------
def convert_dollar_to_dominican_peso_supercasas(price_str):
    price = price_str[price_str.index("$") + 1:price_str.index("/")]
    converted_amount = 0
    if(price[0] == " "):
        price = price[1:]
    price = int(price.replace(",", ""))
    converted_amount = price
    if("US" in price_str):
        converted_amount = USD_to_DOP_EXCHANGE_RATE * price
    return converted_amount

def get_general_data_and_amenities_supercasas(data_str, amenities_str):
    location, condition, current_use, square_footage, terrain, floor, elevator, buildable, construction_year = "", "", "", "", "", "", "", "", ""
    data_str = data_str[data_str.index("Localización:\n") + 14:]
    location = data_str[:data_str.find("\n")]
    l = location.split(",")
    sector = l[len(l) - 2]
    province = l[len(l) - 1]
    if(sector[0] == " "):
        sector = sector[1:]
    if(province[0] == " "):
        province = province[1:]

    data_str = data_str[data_str.index("Condición:\n") + 11:]
    condition = data_str[:data_str.find("\n")]

    data_str = data_str[data_str.index("Uso Actual:\n") + 12:]
    current_use = data_str[:data_str.find("\n")]
    data_str = data_str[data_str.index("Construcción:\n") + 14:]
    square_footage = data_str[:data_str.find(" Mt2")]
    data_str = data_str[data_str.index("Terreno:\n") + 9:]
    terrain = data_str[:data_str.find("\n")]
    data_str = data_str[data_str.index("Nivel/Piso:\n") + 12:]
    floor = data_str[:data_str.find("\n")]
    data_str = data_str[data_str.index("Ascensores:\n") + 12:]
    elevator = data_str[:data_str.find("\n")]
    data_str = data_str[data_str.index("Edificable:\n") + 12:]
    buildable = data_str[:data_str.find("\n")]
    data_str = data_str[data_str.index("Año Construcción:\n") + 18:]
    construction_year = data_str[:data_str.find("\n")]

    amenities_str = amenities_str[amenities_str.index("Comodidades:\n") + 13:]
    amenities_str = amenities_str[1:amenities_str.index("\n\n\n")]
    amenities, amount_amenities = get_amenities_supercasas(amenities_str)
    return location, sector, province, condition, current_use, square_footage, floor, elevator, buildable, construction_year, amenities, amount_amenities

def get_amenities_supercasas(amenities_str):
    result = ""
    amount_amenities = 0
    amenities_str_len = len(amenities_str)
    amenities_list = []
    for index, c in enumerate(amenities_str):
        if(c != " "):
            if (index < amenities_str_len-1 and amenities_str[index+1] in CAPITAL_ALPHABET and amenities_str[index-1] != " "):
                amenities_list.append(c)
                result += c + '-'
                amount_amenities += 1
                continue
        result += c
    save_to_csv_file(amenities_list, "amenities.csv")
    return result, amount_amenities + 1

def get_rooms_and_bathrooms_supercasas(list):
    rooms, bathrooms = "", ""
    for s in list:
        if("habitaci" in s):
            rooms = s[:s.find(" ")]
        if("baño" in s):
            bathrooms = s[:s.find(" ")]
    return float(rooms), float(bathrooms)

#--------------------------------MERCADO LIBRE----------------------------
def convert_dollar_to_dominican_peso_mercadolibre(price_str):
    amount = int(price_str.replace(',', ''))
    converted_amount = amount
    if("US" in price_str):
        converted_amount = USD_to_DOP_EXCHANGE_RATE * amount
    return amount, converted_amount

def format_string_to_date_mercadolibre(date_str):
    time_array = date_str[date_str.index("hace ") + 5:].split(" ")
    time_amount = int(time_array[0])
    time_type = time_array[1]
    date = count_from_current_date(time_amount, time_type)
    return str(date.day), str(date.month), str(date.year)

def count_from_current_date(amount, type):
    days_total_from_publishing = 0
    current_date = datetime.now()
    date = None
    if(type == "días" or type == "día"):
        days_total_from_publishing = amount * 1
        date = current_date - timedelta(days=days_total_from_publishing)
    if(type == "meses" or type == "mes"):
        days_total_from_publishing = calculate_months_to_days(amount)
        date = current_date - timedelta(days=days_total_from_publishing)
    if(type == "años" or type == "año"):
        days_total_from_publishing = amount * 365
        date = current_date - timedelta(days=days_total_from_publishing)
    return date

def calculate_months_to_days(months_amount):
    m = int(months_amount / 12)
    days = 0
    current_month = datetime.now().month
    while(m > 0):
        months_amount -= 12
        days += 365
        m -= 1
    index = current_month - 1
    while(months_amount > 0):
        if(index < 0):
            index = 11
        days += days_in_months[index]
        index -= 1
        months_amount -= 1
    return days - 1

def get_sector_and_province_from_location_mercadolibre(location_str):
    sector, province = "", ""
    location = location_str.split(", ")
    sector, province = location[-2], location[-1]
    if(province == "Santiago" or province == "santiago" and "aballeros" in sector):
        sector = "Santiago de los Caballeros"
    return sector, province

def get_squarefootage_mercadolibre(squarefootage_str):
    return squarefootage_str[0:squarefootage_str.index(" m²")]

def get_rooms_mercadolibre(rooms_str):
    return rooms_str[0:rooms_str.index(" habitaci")]

def get_amenities_mercadolibre(amenities_str):
    index_start = amenities_str

def get_bathrooms_mercadolibre(baths_str):
    return baths_str[0:baths_str.index(" baño")]

def get_amenities_mercadolibre(amenities_str):
    amenities = remove_doubles(amenities_str[0:amenities_str.index("</p>")].split("<br/>"))
    result = ""
    for amenity in amenities:
        if(amenity != ''):
            result += amenity + "-"
    return result[:-1]

#--------------------------------COROTOS----------------------------

def convert_dollar_to_dominican_peso_corotos(price_str):
    amount = int(price_str[price_str.index("$") + 2:].replace(',', ''))
    converted_amount = USD_to_DOP_EXCHANGE_RATE * amount
    return amount, converted_amount

def remove_doubles(array):
    return [*set(array)]

def convert_string_to_date(date_str):
    date = date_str.split(" de ")
    day = date[0][date[0].index(":") + 1:]
    return int(day), months[date[1]], int(date[2])

def location_to_sector_and_province(location):
    location_split = location.split(", ")
    return location_split[0], location_split[1]

def get_details(specs_items_array):
    type_amenity, rooms, bathrooms, square_footage, half_bathrooms, sector_specs = "---", "---" , "---" , "---" , "---" , "---"
    other_specs = "" 
    for item in specs_items_array:
        title_start = item.index("\n")
        title_end = item[title_start + 1:].index("\n")
        title = item[title_start + 1:title_end + 1]
        value = item[title_end + 2:-1]
        if("Tipo" in title):
            type_amenity = value
            continue
        if("Habitaciones" in title):
            rooms = value
            continue
        if("Baños" in title):
            bathrooms = value
            continue
        if("m²" in title):
            square_footage = value
            continue
        if("Baños Medios" in title):
            half_bathrooms = value
            continue
        if("Sector" in title):
            sector_specs = value
            continue
        else:
            other_specs += title + ":" + value + "-"
    return type_amenity, rooms, bathrooms, square_footage, half_bathrooms, sector_specs, other_specs
        
def get_amenities(amenities_description):
    amenities = remove_doubles(split_by_line_jump(amenities_description))
    result = ""
    for amenity in amenities:
        result += amenity + "-" 
    return result[:-1]

def split_by_line_jump(array):
    result = []
    for item in array:
        sub_items = item.split("\n")
        for sub_item in sub_items:
            if(sub_item != ''):
                result.append(sub_item)
    return result

#if __name__ == '__main__':
    #l = get_txt_file('amenities_.txt')
    #print(int(l[0]))
    #set_txt_file('amenities_.txt', str(int(l[0]) + 1))
    #l = get_txt_file('amenities_.txt')
    #print(l[0])

    #print(convert_dollar_to_dominican_peso_supercasas("US$ 1,350/Mes"))
    #l = '\nDatos Generales\n\n\nLocalización:\nPiantini, Santo Domingo Centro (D.N.), Santo Domingo\n\n\nCondición:\nNueva\nUso Actual:\nResidencial\n\n\nConstrucción:\n71 Mt2\nTerreno:\n0 Mt2\n\n\nNivel/Piso:\n6\nAscensores:\n2\n\n\nEdificable:\nNo\nAño Construcción:\nN/D\n\n\n'
    #l = ['\nDatos Generales\n\n\nLocalización:\nPiantini, Santo Domingo Centro (D.N.), Santo Domingo\n\n\nCondición:\nNueva\nUso Actual:\nResidencial\n\n\nConstrucción:\n71 Mt2\nTerreno:\n0 Mt2\n\n\nNivel/Piso:\n6\nAscensores:\n2\n\n\nEdificable:\nNo\nAño Construcción:\nN/D\n\n\n', 
    #'\nComodidades:\n\nAgua PotableArea de Juegos InfantilesAscensorBalcónCisternaControl de AccesoGimnasioLobbyPiscinaPlanta EléctricaPozoSeguridad 24 HorasTerrazaWalk In Closet\n\n\n', '\nMás Fotos\n\n\n\n\n\n\n\n\n\n\n\n\n', '\nObservaciones:\nAlquiler Amueblado!!\r\n\r\nTorre Urbano Residences \r\n\r\nApartamento de 1 habitación. El diseño de Urbano Residences rompe los esquemas de construcción para asegurar tu inversión a través del tiempo.\r\n\r\nUbicación Estratégica / 3 áreas sociales completas tanto en el piso 2 como en el piso 15 / Piscina de Nado / Mini Golf / Terrazas / Gimnasio / Lavandería /\r\n\r\nLa Torre Urbano Residences cuenta con un novedoso diseño e integración con las aceras, le dan mayor impacto y sobriedad. También su fachada está conformada por paneles de aluminio microperforados, que han sido diseñados para la protección solar del interior según su orientación y, al mismo tiempo, permite un flujo moderado de iluminación y aire natural.\n', '\nPropiedades similares en el sector\nVolver atrás\n']
    #l = ['1 habitaciones', '2.0 baños', '1 parqueos']
    #print(get_rooms_and_bathrooms_supercasas(l))
    #save_to_csv_file(l, "my_database.csv")
    #save_to_csv_file(["skjdnfkjsnkfjnsdf"], "error_saving_these_posts.csv") 
    #l = []
    #l.append([1,2])