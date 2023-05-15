import time
import requests
from bs4 import BeautifulSoup
from  requests_html import HTMLSession
import pymongo
import csv

on_queue = []
crawled = []
time_wait = 10
next_pagination_index = 0
next_pagination_link = ""
pagination_exits = True

#client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
#mydb=client['inmuebles_db']
#info = mydb.table1

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
starting_point_link = "https://www.supercasas.com/buscar/?do=1&ObjectType=123&PriceType=403&PriceFrom=0.00&PriceTo=200000.00&PagingPageSkip="
#starting_point_link = "https://www.supercasas.com/buscar/?do=1&ObjectType=123&PriceType=401&PriceFrom=0.00&PriceTo=200000.00&PagingPageSkip="
#starting_point_link = "https://www.supercasas.com/buscar/?do=1&PriceType=401&PriceFrom=0&PriceTo=200000&PagingPageSkip="
#parsing functions
link_1 = "https://www.supercasas.com/apartamentos-alquiler-piantini/1295764/"#good to crawl
link_2 = "https://www.supercasas.com/villas-alquiler-metro-country-club/1299217/"#good to crawl
link_3 = "https://www.supercasas.com/villas-alquiler-casa-de-campo/1263608/" #not to be saved to bd, price by day, not month

AMENITIES_FILE = "amenities.csv"

#===========================================================================================================================

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

#===========================================================================================================================

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

def save_to_csv_file_amenities(data_array):
    for line in data_array:
        with open(AMENITIES_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([line])

def get_csv_to_array_amenities():
    with open(AMENITIES_FILE) as f:
        reader = csv.reader(f)
        lst = list(reader)
    return [item for sublist in lst for item in sublist]



def get_post_info(link):
    try:
        save_to_csv_file([link], "crawled_links_supercasas.csv")
        #user_agent = manage_server_block.get_user_agent()
        req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})# 'Mozilla/5.0'
        soup = BeautifulSoup(req.content, 'html.parser')

        price_crawled_parent  = soup.find("div", {"class": "detail-ad-info-specs-block main-info"})
        price_crawled_narrow = [item for item in price_crawled_parent.find_all("div")]
        price_crawled_tag = str(price_crawled_narrow.pop())
        price = 0    
        if("Alquiler" in price_crawled_tag):
            price_crawled_string = price_crawled_tag[price_crawled_tag.index("</span>") + 7:price_crawled_tag.index("</div>")]
            price_crawled = str(price_crawled_string)
            if(price_crawled[0] == " "):
                price_crawled = price_crawled_string[1:]
            save = True
            if("Mes" not in price_crawled):
                return 
            price = convert_dollar_to_dominican_peso_supercasas(price_crawled)  

        post_title_parent = soup.find("div", {"id": "detail-ad-header"})
        post_title = str(post_title_parent.find("h2"))
        post_title = post_title[post_title.index("Alquiler, ") + 10:post_title.index("</h2>")] 

        general_data_and_amenities = [item.text for item in soup.find_all("div", {"class": "detail-ad-info-specs-block"})]
        location, sector, province, condition, current_use, square_footage, floor, elevator, buildable, construction_year, amenities, amount_amenities = get_general_data_and_amenities_supercasas(general_data_and_amenities[4], general_data_and_amenities[5])
        
        rooms_parent = soup.find("div", {"class": "detail-ad-info-specs-block secondary-info"})
        rooms_and_bathrooms = [item.string for item in rooms_parent.find_all("span")]
        rooms, bathrooms = get_rooms_and_bathrooms_supercasas(rooms_and_bathrooms)

        r = s.get(link)
        r.html.render(sleep=1)
        image_link = ""
        listings = r.html.xpath('//*[@id="detail-ad-info-specs"]', first=True)
        for l in listings.absolute_links:
            if ("/img.supercasas.com/" in str(l)):
                image_link = str(l)
                break
        
        details_array = ["supercasas",link,price_crawled,price,post_title,rooms,
        bathrooms,location,sector,province,condition,current_use,square_footage,floor,
        elevator,buildable,construction_year,amenities,amount_amenities, image_link]
        save_to_csv_file(details_array, "my_database_SUPERCASAS.csv")

        details = {
            "website": "supercasas", 
            "link": link,
            "price_crawled": price_crawled,
            "price_DOP": price,
            "title": post_title,
            "rooms": rooms,
            "bathrooms": bathrooms,
            "location_crawled":location, 
            "sector": sector, 
            "province": province, 
            "condition": condition, 
            "current_use": current_use, 
            "square_footage": square_footage, 
            "floor": floor, 
            "elevator": elevator, 
            "buildable": buildable, 
            "construction_year": construction_year, 
            "amenities": amenities, 
            "amount_amenities": amount_amenities,
            "image_link": image_link
        }
        #info.insert_many(details)
        save_to_csv_file([link], "saved_posts_supercasas.csv")        
    except:
        save_to_csv_file([link], "error_supercasas.csv") 

def get_posts_on_queue(link):
    global on_queue
    global crawled
    global pagination_exits
    r = s.get(link)
    r.html.render(sleep=1)
    if(r is not None):
        pagination_exits = True
    else:
        pagination_exits = False
    listings = r.html.xpath('//*[@id="bigsearch-results-inner-container"]', first=True)
    for post in listings.links:
        if str(post) not in on_queue and post not in crawled and "/buscar/" not in str(post) and "locales" not in str(post):
            save_to_csv_file(["https://www.supercasas.com" + str(post)], "on_queue_supercasas.csv") 
            on_queue.append("https://www.supercasas.com" + str(post))    
    save_to_csv_file(on_queue, "crawled_links_supercasas.csv")

def next_in_pagination(link):
    global next_pagination_index
    try:
        r = s.get(link)
        r.html.render(sleep=1)
        listings = r.html.xpath('//*[@id="bigsearch-results-inner-lowerbar-pages"]', first=True)
        return starting_point_link + next_pagination_index
    except:
        return -1

def populate_on_queue(link):
    get_posts_on_queue(link)
    return

def save_posts():
    for link in on_queue:
        print(link)
        get_post_info(link)
        time.sleep(10 * 60)

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

def get_on_queue():
    l = get_txt_file('last_pagination_supercasas.txt')
    get_posts_on_queue(starting_point_link + str(int(l[0])))
    set_txt_file('last_pagination_supercasas.txt', str(int(l[0]) + 1))

if __name__ == '__main__':
    l = get_txt_file('last_pagination_supercasas.txt')
    get_posts_on_queue(starting_point_link + str(int(l[0])))
    set_txt_file('last_pagination_supercasas.txt', str(int(l[0]) + 1))
    #current_link = get_first_line_csv_on_queue("on_queue_supercasas.csv")
    #remove_first_csv_line("on_queue_supercasas.csv")
    #get_post_info(current_link)
    #save_posts()
    #l = "https://www.supercasas.com/buscar/?do=1&PriceType=401&PriceFrom=0&PriceTo=200000&PagingPageSkip=18"
    #next_in_pagintation(l)
