from datetime import datetime, timedelta
import pytz
import csv

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