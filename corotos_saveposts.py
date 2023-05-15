import time
import requests
from bs4 import BeautifulSoup
import urljoin
from  requests_html import HTMLSession
import pymongo
import csv

#MONGO_URI = 'mongodb://localhost:27017'
#client = MongoClient(MONGO_URI)
#db = client.inmuebles_db
#collection = db.publicaciones

#client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
#mydb=client['inmuebles_db']
#info = mydb.table1

ALL_AMENITIES = ['Agua Potable', 'Área de Juegos Infantiles', 'Area de Juegos Infantiles', 'Área de Juego Infantil',
                 'Area de Juego Infantil', 'Ascensor', 'Balcon', 'Balcón', 'Cisterna', 'Control de Acceso', 'Gimnasio',
                 'Lobby', 'Piscina', 'Planta Electrica', 'Pozo', 'Seguridad 24 Horas', 'Seguridad Privada', 'Terraza',
                 'Walk In Closet', '1/2 Baño', '1/2 Bano', 'Área Servicio Independiente', 'Area Servicio Independiente',
                 'Cuarto de Servicio', 'Inversor', 'Jacuzzi', 'Estar Familiar', 'Aire Acondicionado', 'Gazebo', 'Estudio',
                 'Patio', 'Vestidores', 'Vestidor', 'Family Room', 'Picuzzi', 'Satelite', 'Sauna', 'Shutters', 'Walk In Closet',
                 'Roof garden', 'Salon de usos múltiples', 'Salon de usos multiples', 'Salon multiuso', 'Almacenamiento', 
                 'Ludoteca', 'Seguridad', 'Estacionamiento', 'Parqueo', 'Bodega', 'Elevador', 'Ascensor', 'Salón de eventos',
                 'Salon de evento', 'Alberca', 'Pistas de ciclismo', 'Espacio de ciclismo', 'Pista para correr',
                 'Espacio para correr', 'Pista para caminar', 'Espacio para caminar','Cancha','Business Center',
                 'Instalaciones para mascotas','Guardería para perros','Guarderia para perros','Guarderia para perro',
                 'Bar','Spa','Sky Lounge','Lounge','Salón de belleza','Salon de belleza','Area para fogata','Jardines',
                 'Jardín','Jardin','Cuarto de Servicio','Ventanas Grandes','Áreas verdes','Areas Verdes','Casa Club',
                 'Área de asado','Area de asado','BBQ','Área infantil','Area infantil','Sala de cine','Cine','Espacio coworking',
                 'Area de lavado','Área de recepción','Area de recepción','Servicio de recepcionista','Recepcionista',
                 'Wifi','Lavadora','Secadora','Calefacción','Calefaccion','Área para trabajar con laptop',
                 'Area para trabajar con laptop','Mascotas','Detector de humo','Detector de monóxido de carbono',
                 'Detector de monoxido de carbono','Extintor','Botiquín de primeros auxilios','Botiquin de primeros auxilios',
                 'Números locales de emergencia','Numeros locales de emergencia','Plan y números locales de emergencia',
                 'Plan y numeros locales de emergencia','Plan de emergencia','Cocinas totalmente equipadas','Cocinas equipadas',
                 'Tina','Buena iluminación','Buena iluminacion','Amueblado','Línea blanca','Linea blanca','Zona de trabajo',
                 'Salón social','Salon social','Área residencial','Area residencial','Residencial','Cámaras de seguridad',
                 'Camaras de seguridad','Yoga y meditación','Yoga','Meditación','Meditacion','Cerca de parque','Rooftop Deck',
                 'Zona de Calisteria','Conserjeria','Servicio de Conserjería','Servicio de Conserjeria','Lavandería Comunitaria',
                 'Lavanderia Comunitaria','Parqueo de Visitantes','Estacionamiento de Visitantes','App Comunitario',
                 'Apps Comunitario','Apps Comunitaria','Gas Central','Acceso a la playa']

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

on_queue = []
crawled = []

s = HTMLSession()
starting_point_link = "https://www.corotos.com.do/k/renta%20de%20apartamentos?q%5Bpublished_at_lteq%5D=2022-12-16T04%3A55%3A59Z&q%5Bsorts%5D=published_at%20desc&search=renta%20de%20apartamentos&page=1&per_page=36"
#starting_point_link = "https://www.corotos.com.do/k/apartamentos%20en%20alquiler"

#===========================================================================================================================

def save_to_csv_file(data_array, csv_file_name):
    with open(csv_file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_array)

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
            print(bathrooms)
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
    i = 0
    for amenity in amenities:
        result += amenity + "-" 
        i += 1
    return result[:-1], i

def split_by_line_jump(array):
    result = []
    for item in array:
        sub_items = item.split("\n")
        for sub_item in sub_items:
            if(sub_item != ''):
                result.append(sub_item)
    return result

#===========================================================================================================================

#parsing functions
link_id = 0
time_wait = 10
link_1 = "https://www.corotos.com.do/listings/rento-apartamento-en-naco-con-dos-parqueos-dos-habitaciones-01gkbwda5nes16qhx13s0fen7y"
link_2 = "https://www.corotos.com.do/listings/rento-apartamento-amueblado-full-01gf9xrqjkb870xr1d7r8t9zm1"
link_3 = "https://www.corotos.com.do/listings/apartamento-con-piscina-perfecto-para-vivir-airbnb-y-renta-fija-santiago-r-d-01gk5b8v0z3s1az2zysp356ne8?q%5Bpublished_at_lteq%5D=2022-12-14T01%3A32%3A10Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=2&per_page=36&details_page=40&count=192&render_time=2022-12-14T01%3A32%3A10Z"

def get_post_info(link):
    try:
        #save_to_csv_file([link], "crawled_links_corotos.csv")
        #user_agent = manage_server_block.get_user_agent()
        req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})# 'Mozilla/5.0'
        soup = BeautifulSoup(req.content, 'html.parser')

        post_detail_parent = soup.find("div", {"class": "post__details"})
        price_str = post_detail_parent.find("h2", {"class": "post__price"})
        title_description = soup.find("h1", {"class": "post__title"}).contents[0]

        location_tags = str(soup.find("ul", {"class": "post__category-and-location"}))
        start_location = location_tags[location_tags.index("</span>") + 8:]
        end_location = start_location[:start_location.index("<li>") - 7]

        date_string = post_detail_parent.find("p", {"class": "post__date"})
        title_str = post_detail_parent.find("h1", {"class": "post__title"})
        title = title_str.string
        specs_items_array = []
        post_description = soup.find("div", {"class": "post__description"})
        specs = post_description.find("ul", {"class": "post__specs"})
        specs_items_array = [item.text for item in specs.find_all("li", {"class": "specs__item"})]
        amenities_description = [item.text for item in post_description.find_all("p")]
        title_description = str(title_description).replace("\n", " ")
        price, converted_price_dop = convert_dollar_to_dominican_peso_corotos(price_str.string)
        date = date_string.string
        day, month, year = convert_string_to_date(date)
        sector, province = location_to_sector_and_province(end_location)
        type_amenity, rooms, bathrooms, square_footage, half_bathrooms, sector_specs, other_specs = get_details(specs_items_array)
        amenities, amenities_amount = get_amenities(amenities_description)
        
        #r = s.get(link)
        #r.html.render(sleep=1)
        #images = r.html.find('img')
        image_link = ""
        #for image in images:
        #    if "/img.corotos.com.do/" in str(image):
        #        if("/img.corotos.com.do/variants/" in str(image.attrs['src'])):
        #            image_link = str(image.attrs['src'])
        #            break

        details_array = ["corotos",link,price,converted_price_dop,date,day,
        month,title,end_location,sector,province,type_amenity,rooms,bathrooms,
        other_specs,square_footage,half_bathrooms,sector_specs,amenities,amenities_amount, image_link]
        save_to_csv_file(details_array, "my_database_COROTOS.csv")
        print(details_array)

        details = {
            "website": "corotos",
            "link" : link, 
            "price_crawled": price, 
            "price_DOP": converted_price_dop,
            "date_crawled": date, 
            "day_upload": day,
            "month_upload": month, 
            "year_upload": year,
            "title": title, 
            "location_crawled": end_location,
            "sector_from_location": sector,
            "province": province,
            "tipo": type_amenity, 
            "rooms": rooms, 
            "bathrooms": bathrooms, 
            "other_specs": other_specs,
            "square_footage": square_footage, 
            "half_bathrooms": half_bathrooms, 
            "sector_from_specs": sector_specs,
            "amenities_description": amenities,
            "amount_amenities": 0,
            "image_link": image_link
        }

        #info.insert_many(details)
        save_to_csv_file([link], "saved_posts_corotos.csv")        
    except:
        save_to_csv_file([link], "error_corotos.csv")  


def next_in_pagination(link):
    #go through the pagination of the origin link
    page_start = link.index("&page=")
    page_index = int(link[page_start + 6:page_start + 7])
    next_page = page_index + 1
    next_link = link[:page_start + 6] + str(next_page) + link[page_start + 7:]
    return next_link

def get_total_pages_paginated(link):#works great the first time, after that the page changes it to the current page index
    get_new_link= s.get(link)
    get_new_link.html.render(sleep=1)
    listings = get_new_link.html.xpath('//*[@class="flex items-center flex-wrap"]', first=True)
    listings_s = str(listings.text)
    total_pages = listings_s[listings_s.index("-") + 1:]
    return int(total_pages)

def get_posts_on_queue(link):
    global on_queue
    global crawled
    r = s.get(link)
    r.html.render(sleep=1)
    listings = r.html.xpath('//*[@class="page_content"]', first=True)
    for post in listings.links:
        if str(post) not in on_queue and post not in crawled and "/listings/" in str(post):
            save_to_csv_file([str(post)], "on_queue_corotos.csv") 
            on_queue.append(str(post))    

def populate_on_queue(current_in_pagination_link):
    total_pagination = get_total_pages_paginated(current_in_pagination_link)
    i = 0
    while i < total_pagination:
        get_posts_on_queue(current_in_pagination_link)
        time.sleep(time_wait * 60)
        current_in_pagination_link = next_in_pagination(current_in_pagination_link)
        i += 1
    save_to_csv_file(on_queue, "crawled_links_corotos.csv")
    return

def get_txt_file(txt_file_name):
    with open(txt_file_name) as f:
        lines = f.readlines()
    return lines

def set_txt_file(txt_file_name, message):
    with open(txt_file_name, "w") as f:
        f.write(message)

def save_posts():
    for link in on_queue:
        get_post_info(link)
        #crawled.append(link) 
        time.sleep(time_wait * 60)

def get_first_line_csv_on_queue(file):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        return next(reader)[0]

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
    
def get_save_post():
    current_link = get_first_line_csv_on_queue("on_queue_corotos.csv")
    if(current_link is not None):
        remove_first_csv_line("on_queue_corotos.csv")
        get_post_info(current_link)
    time.sleep(3 * 60)

if __name__ == '__main__':
    while (True):
        get_save_post()
