import time
import requests
from bs4 import BeautifulSoup
import urljoin
from  requests_html import HTMLSession
import pymongo
import static_functions

#MONGO_URI = 'mongodb://localhost:27017'
#client = MongoClient(MONGO_URI)
#db = client.inmuebles_db
#collection = db.publicaciones

#client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
#mydb=client['inmuebles_db']
#info = mydb.table1

on_queue = []
crawled = []

s = HTMLSession()
starting_point_link = "https://www.corotos.com.do/k/renta%20de%20apartamentos?q%5Bpublished_at_lteq%5D=2022-12-16T04%3A55%3A59Z&q%5Bsorts%5D=published_at%20desc&search=renta%20de%20apartamentos&page=1&per_page=36"
#starting_point_link = "https://www.corotos.com.do/k/apartamentos%20en%20alquiler"
#COROTOS CRAWLER
#parsing functions
link_id = 0
link_1 = "https://www.corotos.com.do/listings/rento-apartamento-en-naco-con-dos-parqueos-dos-habitaciones-01gkbwda5nes16qhx13s0fen7y"
link_2 = "https://www.corotos.com.do/listings/rento-apartamento-amueblado-full-01gf9xrqjkb870xr1d7r8t9zm1"
link_3 = "https://www.corotos.com.do/listings/apartamento-con-piscina-perfecto-para-vivir-airbnb-y-renta-fija-santiago-r-d-01gk5b8v0z3s1az2zysp356ne8?q%5Bpublished_at_lteq%5D=2022-12-14T01%3A32%3A10Z&q%5Bsorts%5D=published_at+desc&search=renta+de+apartamentos&page=2&per_page=36&details_page=40&count=192&render_time=2022-12-14T01%3A32%3A10Z"

def get_post_info(link):
    req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(req.content, 'html.parser')

    post_detail_parent = soup.find("div", {"class": "post__details"})
    price_str = post_detail_parent.find("h2", {"class": "post__price"})
    title_description = soup.find("h1", {"class": "post__title"}).contents[0]

    location_tags = str(soup.find("ul", {"class": "post__category-and-location"}))
    start_location = location_tags[location_tags.index("</span>") + 8:]
    end_location = start_location[:start_location.index("<li>") - 7]

    date_string = post_detail_parent.find("p", {"class": "post__date"})
    title = post_detail_parent.find("h1", {"class": "post__title"})
    specs_items_array = []
    post_description = soup.find("div", {"class": "post__description"})
    specs = post_description.find("ul", {"class": "post__specs"})
    specs_items_array = [item.text for item in specs.find_all("li", {"class": "specs__item"})]
    amenities_description = [item.text for item in post_description.find_all("p")]
    title_description = str(title_description).replace("\n", " ")
    price, converted_price_dop = static_functions.convert_dollar_to_dominican_peso_corotos(price_str.string)
    date = date_string.string
    day, month, year = static_functions.convert_string_to_date(date)
    sector, province = static_functions.location_to_sector_and_province(end_location)
    type_amenity, rooms, bathrooms, square_footage, half_bathrooms, sector_specs, other_specs = static_functions.get_details(specs_items_array)
    amenities = static_functions.get_amenities(amenities_description)
    
    details = {
        "website": "corotos",
        "link" : link, 
        "price_crawled": price, 
        "price_DOP": converted_price_dop,
        "date_crawled": date, 
        "day_upload": day,
        "month_upload": month, 
        "year_upload": year,
        "title": title.string, 
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
        "amenities_description": amenities
    }
    #info.insert_many(details)

def get_posts_on_queue(link):
    global on_queue
    global crawled
    r = s.get(link)
    r.html.render(sleep=1)
    listings = r.html.xpath('//*[@class="page_content"]', first=True)
    for post in listings.absolute_links:
        if str(post) not in on_queue and post not in crawled and "/listings/" in str(post):
            on_queue.append(str(post))

def next_in_pagination(link):
    #go through the pagination of the origin link
    page_start = link.index("&page=")
    page_index = int(link[page_start + 6:page_start + 7])
    next_page = page_index + 1
    next_link = link[:page_start + 6] + str(next_page) + link[page_start + 7:]
    return next_link

def get_total_pages_paginated():#works great the first time, after that the page changes it to the current page index
    get_new_link= s.get(starting_point_link)
    get_new_link.html.render(sleep=1)
    listings = get_new_link.html.xpath('//*[@class="flex items-center flex-wrap"]', first=True)
    listings_s = str(listings.text)
    total_pages = listings_s[listings_s.index("-") + 1:]
    return int(total_pages)


if __name__ == '__main__':
    current_page = get_total_pages_paginated()
    get_posts_on_queue(starting_point_link)

    pages_counter = 5
    while pages_counter > 0:
        get_post_info(on_queue[0])
        crawled.append(on_queue[0])
        on_queue.pop(0)
        pages_counter -= 1
        time_wait = 11
        time.sleep(time_wait * 60)
        if len(on_queue) > 0:
            if len(on_queue) - 5 >= 0:
                pages_counter += 5
            else:
                pages_counter += 1






#get_post_info(link_1)
#get_post_info(link_2)
#get_post_info(link_3)