import time
import requests
from bs4 import BeautifulSoup
import urljoin
from  requests_html import HTMLSession
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
        amenities = get_amenities(amenities_description)
        #image_slider = post_description.find("div", {"class": "flickity-slider"})
        #print(image_slider)
        #first_image_in_slider = image_slider.find("div", {"class": "carousel-cell is-selected"})
        #print(first_image_in_slider)
        #image_link = first_image_in_slider.find("img", class_ = "pageloaded")['src']
        #print(image_link)
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
        other_specs,square_footage,half_bathrooms,sector_specs,amenities,0, image_link]
        save_to_csv_file(details_array, "my_database_COROTOS.csv")
        print(details_array)

        #info.insert_many(details)
        #save_to_csv_file([link], "saved_posts_corotos.csv")        
    except:
        return
        #save_to_csv_file([link], "error_corotos.csv")  


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

def get_saveposts_errors():
    current_link = get_first_line_csv_on_queue("error_corotos.csv")
    if(current_link is not None):
        remove_first_csv_line("error_corotos.csv")
        get_post_info(current_link)

if __name__ == '__main__':
    new = ['corotos', 'https://www.corotos.com.do/listings/rentamos-y-o-vendemos-por-ti-tu-apartamento-casa-aparta-estudio-solar-fjsy16z?q%5Bpublished_at_lteq%5D=2023-03-16T11%3A53%3A58Z&q%5Bsorts%5D=score_letter+asc%2Cpublished_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=22&count=212&render_time=2023-03-16T11%3A53%3A58Z', 35000, 1986358.5000000002, 'Publicado: 14 de enero de 2023', 14, 1, 'Rentamos y/o vendemos por ti tu Apartamento, casa, aparta-estudio, solar.\n', 'Distrito Nacional, Santo Domingo', 'Distrito Nacional', 'Santo Domingo', 'Sin Amueblar', '2', '2', '', '200', '---', 'Bella Vista', '3. Habitación terciaria (abierta)-4. (2) baños.-5. Comedor (por separado)-1. Habitación principal con baño y walking closet.-7. Área de lavado.-3. Cocina espaciosa.-Descripción de este apartamento:-Si no quieres lidiar con el proceso de alquiler o venta de tu inmueble nosotros nos encargamos de todo el proceso de muestra, negociación, financiero y legal.-Apartamento con decoración en paredes en madera pulida y bien acabada, es un apartamento bastante espacioso para disfrutar el estadía y comodidad en familia sin necesidad de salir-2. Habitación secundaria con closet espacioso.-4. Sala.-6. Balcón espacioso-Para más información ponte en contacto.', 0, '']
    save_to_csv_file(new, "my_database_COROTOS.csv")
    #time.sleep(3 * 60)
    #get_post_info("https://www.corotos.com.do/listings/rentamos-y-o-vendemos-por-ti-tu-apartamento-casa-aparta-estudio-solar-fjsy16z?q%5Bpublished_at_lteq%5D=2023-03-16T11%3A53%3A58Z&q%5Bsorts%5D=score_letter+asc%2Cpublished_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=22&count=212&render_time=2023-03-16T11%3A53%3A58Z")

    #l = get_txt_file('last_pagination_corotos.txt')
    #get_posts_on_queue(starting_point_link + str(int(l[0])))
    #set_txt_file('last_pagination_corotos.txt', str(int(l[0]) + 1))
    #populate_on_queue(starting_point_link)
    #save_posts()

#l_41 = ['https://www.corotos.com.do/listings/se-renta-apartamento-nuevo-en-sarmiento-2nm0x5a?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=3&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/apartamento-95-m2-en-renta-amueblado-2-habitaciones-santiago-01gaw4dpfjx4hhb4s2bg1k7wp8', 'https://www.corotos.com.do/listings/vendo-apartamento-97-39mts-gazcue-01ghvna2vdrped5txze53c0369', 'https://www.corotos.com.do/listings/renta-de-apartamento-ubicado-en-san-isidro-labrador-464gp87?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=9&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamento-ubicado-en-colinas-de-los-rios-yxdwa4w?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=11&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/apartamento-en-renta-en-naco-vq1tkv1?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=15&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/apartamento-en-renta-115-m2-3-habitaciones-2-parqueos-ascensor-area-social-espxj9j?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=27&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamento-totalmente-amueblado-y-equipado-4z4qm4g?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=31&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamento-vacacional-en-cocotal-punta-cana-dia-semana-mes-hwewyj1?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=29&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamento-en-naco-sin-amueblar-01gkyv65n86dexqyphd5n5exyk', 'https://www.corotos.com.do/listings/sin-intermediario-rento-apartamento-amueblado-full-1-habitacion-1e3xp9a?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=21&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/apartamentos-en-renta-hfm0vrb?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=30&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/sin-intermediario-rento-apartamento-amueblado-full-2-hb-wn16219?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=33&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/apartamento-amueblado-frente-al-ole-de-la-jacobo-renta-corta-k5azqq2?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=18&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/apartamento-disponible-para-la-renta-rcfzmdf?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=5&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/sin-intermediarios-rento-apartamento-piantini-rkjnr0h?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=28&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamentos-nuevos-en-ciudad-satelite-ykhff6z?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=8&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamento-amueblado-en-evaristo-morales-01ghpc220220w7d6651pt9ytp0', 'https://www.corotos.com.do/listings/sin-intermediarios-rento-apartamento-en-naco-amplio-6m2ye8c?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=24&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/sin-intermediario-rento-apartamento-amueblado-full-1-habitacion-xc8kxj6?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=32&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/for-rent-bellisimo-y-moderno-apartamento-ejecutivo-con-alto-nivel-de-calidad-vv7wjce?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=14&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/sin-intermediarios-rento-apartamento-piantini-07kdtdc?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=23&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/sin-intermediarios-rento-apartamento-torre-moderna-100-mts2-291zm7t?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=20&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamento-1-habitacion-a-estrenar-en-el-millon-prox-a-gustavo-m-ricart-6pkdnps?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=19&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamento-ubicado-en-colinas-de-los-rios-yrfzqdq?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=12&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamento-en-naco-con-dos-parqueos-dos-habitaciones-01gkbwda5nes16qhx13s0fen7y', 'https://www.corotos.com.do/listings/sin-intermediarios-rento-apartamento-en-naco-cuarto-de-servicio-znwyjq9?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=22&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamento-en-el-paraiso-wgpsrwm?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=13&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/for-rent-bellisimo-y-moderno-apartamento-ejecutivo-con-alto-nivel-de-calidad-v83mvg8?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=16&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/apartamento-en-renta-evaristo-morales-145-mts-cuadrados-mj207e4?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=26&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/se-renta-apartamento-amueblado-kmarf3d?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=34&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/renta-apartamento-amueblado-en-santiago-rd-4j5ny21?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=36&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamentos-nuevos-en-ciudad-satelite-2s7v44y?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=1&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-hermoso-apartamento-nuevo-a-estrenar-bien-iluminado-ventilado-moderno-d1gjq8b?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=35&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/hermoso-apartamento-renta-vacacional-49d53x3?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=6&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/renta-de-apartamento-sy5qjmr?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=4&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/se-renta-apartamento-amueblado-res-alejo-v-yn2g96f?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=7&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/apartamento-en-venta-y-renta-en-serralles-pxfxd90?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=17&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/for-rent-hermoso-y-fresco-apartamento-piso-alto-ubicado-en-bella-vista-0e40bra?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=10&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/apartamento-disponible-para-rentar-11-800-mensual-yw3jg5v?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=2&count=190&render_time=2023-02-05T23%3A33%3A32Z', 'https://www.corotos.com.do/listings/rento-apartamentos-en-riveras-de-haina-bayona-rd-14-000-y-15-000-pesos-44jpy95?q%5Bpublished_at_lteq%5D=2023-02-05T23%3A33%3A32Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=1&per_page=36&details_page=25&count=190&render_time=2023-02-05T23%3A33%3A32Z']
    