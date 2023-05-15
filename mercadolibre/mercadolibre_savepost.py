import time
from numpy import require
import requests
from bs4 import BeautifulSoup
import urljoin
from  requests_html import HTMLSession
from datetime import datetime, timedelta
import csv

on_queue = []
crawled = []

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

s = HTMLSession()
starting_point_link = "https://inmuebles.mercadolibre.com.do/apartamentos/alquiler/_NoIndex_True#unapplied_filter_id%3Dsince%26unapplied_filter_name%3DFiltro+por+fecha+de+comienzo%26unapplied_value_id%3Dtoday%26unapplied_value_name%3DPublicados+hoy%26unapplied_autoselect%3Dfalse"
#parsing functions
link_id = 0
time_wait = 10
link_1 = "https://apartamento.mercadolibre.com.do/MRD-523714674-alquiler-apartamento-en-llanos-de-gurabo-santiago-ajp-203-_JM#position=1&search_layout=grid&type=item&tracking_id=6f58c769-ea24-45e4-8012-5b8058cc9f9b"

#===========================================================================================================================

def convert_dollar_to_dominican_peso_mercadolibre(price_str):
    amount = int(str(price_str.string).replace(',', ''))
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
    print("MTS2: " +squarefootage_str)
    return squarefootage_str[0:squarefootage_str.index(" m²")]

def get_rooms_mercadolibre(rooms_str):
    return rooms_str[0:rooms_str.index(" habitaci")]

def get_amenities_mercadolibre(amenities_str):
    index_start = amenities_str

def get_bathrooms_mercadolibre(baths_str):
    return baths_str[0:baths_str.index(" baño")]

def remove_doubles(array):
    return [*set(array)]

def get_amenities_mercadolibre(amenities_str):
    amenities = remove_doubles(amenities_str[0:amenities_str.index("</p>")].split("<br/>"))
    result = ""
    for amenity in amenities:
        if(amenity != ''):
            result += amenity + "-"
    return result[:-1]

def save_to_csv_file(data_array, csv_file_name):
    with open(csv_file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_array)

#===========================================================================================================================
def get_post_info(link):
    #try:
        shell = require('shelljs')
        shell.exec('pkill chrome')
        save_to_csv_file([link], "crawled_links_mercadolibre.csv")
        #user_agent = manage_server_block.get_user_agent()
        req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})# 'Mozilla/5.0'
        soup = BeautifulSoup(req.content, 'html.parser')
        
        #post_title_parent = soup.find("div", {"class": "ui-vip-core"})
        post_title = soup.find("h1", {"class": "ui-pdp-title"})
        price_str = soup.find("span", {"class":"andes-money-amount__fraction"})
        price, converted_price_dop = convert_dollar_to_dominican_peso_mercadolibre(price_str)
        date_str = soup.find("p", {"class":"ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle"}).string
        day, month, year = format_string_to_date_mercadolibre(date_str)
        location_str = [item.string for item in soup.find_all("p", {"class":"ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title"})]
        location = location_str.pop()
        sector, province = get_sector_and_province_from_location_mercadolibre(location)

        sf = s.get(link)
        sf.html.render(sleep=1)    
        page_html = sf.html
        squarefootage_baths_rooms_str  = page_html.find(".ui-pdp-container__row ui-pdp-container__row--highlighted-specs-res")
        print(squarefootage_baths_rooms_str)
        squarefootage_baths_rooms_str = [item.string for item in soup.find_all("span", {"class":"ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-label"})]
        print(squarefootage_baths_rooms_str)
        square_footage = get_squarefootage_mercadolibre(squarefootage_baths_rooms_str[0])
        rooms = get_rooms_mercadolibre(squarefootage_baths_rooms_str[1])
        bathrooms = get_bathrooms_mercadolibre(squarefootage_baths_rooms_str[2])

        #r = s.get(link)
        #r.html.render(sleep=1)
        amenities_str = ""
        amenities = sf.html.find('p',containing='web data extraction')('[class="ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--REGULAR"]')
        #print(amenities)
        #for a in amenities:
        #    print(a)

        images = sf.html.find('img')
        image_link = ""
        for image in images:
                if("/http2.mlstatic.com/" in str(image.attrs['src']) and ".webp" in str(image.attrs['src'])):
                    image_link = str(image.attrs['src'])
                    break

        details_array = ["mercado-libre", link,price,converted_price_dop,date_str,day,
        month,year,post_title,location,sector,province,rooms,bathrooms,square_footage,amenities,0,image_link]
        save_to_csv_file(details_array, "my_database_MERCADOLIBRE.csv")

        print(details_array)
        details = {
            "website": "mercado-libre",
            "link": link,
            "price_crawled": price,
            "price_DOP": converted_price_dop,
            "date_crawled": date_str,
            "day_upload": day,
            "month_upload": month, 
            "year_upload": year,
            "title": post_title,
            "location_crawled": location,
            "sector_from_location": sector,
            "province": province,
            "rooms": rooms,
            "bathrooms": bathrooms,
            "square_footage": square_footage,
            "amenities": amenities,
            "amount_amenities": 0,
            "image_link": image_link
        }
        
        #save_to_csv_file([link], "saved_posts_mercadolibre.csv")        
    #except:
        #save_to_csv_file([link], "error_mercadolibre.csv") 

def get_posts_on_queue(link):
    global on_queue
    global crawled
    r = s.get(link)
    r.html.render(sleep=1)
    listings = r.html.xpath('//*[@class="ui-search shops__ui-main"]', first=True)
    for post in listings.absolute_links:
        if str(post) not in on_queue and post not in crawled:
            save_to_csv_file([str(post)], "on_queue_mercadolibre.csv")   
            on_queue.append(str(post))

def next_in_pagination(link):
    #go through the pagination of the origin link
    try:
        r = s.get(link)
        r.html.render(sleep=1)
        next_page = r.html.xpath('//*[@class="andes-pagination__link shops__pagination-link ui-search-link"]', first=True)
        return next_page.absolute_links.pop()
    except:
        return -1

#==========================================================================================================

def get_txt_file(txt_file_name):
    with open(txt_file_name) as f:
        lines = f.readlines()
    return lines

def set_txt_file(txt_file_name, message):
    with open(txt_file_name, "w") as f:
        f.write(message)

def populate_on_queue(current_in_pagination_link):
    while next_in_pagination(current_in_pagination_link) != -1:
        get_posts_on_queue(current_in_pagination_link)
        time.sleep(time_wait * 60)
        current_in_pagination_link = next_in_pagination(current_in_pagination_link)
    save_to_csv_file(on_queue, "crawled_links_mercadolibre.csv")
    return

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
    current_link = get_first_line_csv_on_queue("on_queue_mercadolibre.csv")
    if(current_link is not None):
        remove_first_csv_line("on_queue_mercadolibre.csv")
        get_post_info(current_link)
    time.wait(10*60)

if __name__ == '__main__':
    #while(True):
    #    get_save_post()

    current_link = "https://apartamento.mercadolibre.com.do/MRD-526809580-se-alquila-apartamento-en-1er-piso-residencial-monumental-santo-domingo-distrito-nacional-_JM#position=5&search_layout=grid&type=item&tracking_id=8d4842b1-e73f-4eb7-b934-c004c435bab6"
    get_post_info(current_link)
    #current_link = get_first_line_csv_on_queue("mercadolibre\on_queue_mercadolibre.csv")
    #if(current_link is not None):
    #    remove_first_csv_line("mercadolibre\on_queue_mercadolibre.csv")
    #    get_post_info(current_link)

