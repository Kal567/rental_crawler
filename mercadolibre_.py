import time
import requests
from bs4 import BeautifulSoup
import urljoin
from  requests_html import HTMLSession
import static_functions

on_queue = []
crawled = []

s = HTMLSession()
starting_point_link = "https://inmuebles.mercadolibre.com.do/apartamentos/alquiler/_NoIndex_True#unapplied_filter_id%3Dsince%26unapplied_filter_name%3DFiltro+por+fecha+de+comienzo%26unapplied_value_id%3Dtoday%26unapplied_value_name%3DPublicados+hoy%26unapplied_autoselect%3Dfalse"
#COROTOS CRAWLER
#parsing functions
link_id = 0
link_1 = "https://apartamento.mercadolibre.com.do/MRD-523714674-alquiler-apartamento-en-llanos-de-gurabo-santiago-ajp-203-_JM#position=1&search_layout=grid&type=item&tracking_id=6f58c769-ea24-45e4-8012-5b8058cc9f9b"

def get_post_info(link):
    req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(req.content, 'html.parser')

    #post_title_parent = soup.find("div", {"class": "ui-vip-core"})
    post_title = soup.find("h1", {"class": "ui-pdp-title"}).string
    price_str = soup.find("span", {"class":"andes-money-amount__fraction"}).string
    price, converted_price_dop = static_functions.convert_dollar_to_dominican_peso_mercadolibre(price_str)
    date_str = soup.find("p", {"class":"ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle"}).string
    day, month, year = static_functions.format_string_to_date_mercadolibre(date_str)
    location_str = [item.string for item in soup.find_all("p", {"class":"ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title"})]
    location = location_str.pop()
    sector, province = static_functions.get_sector_and_province_from_location_mercadolibre(location)
    squarefootage_baths_rooms_str = [item.text for item in soup.find_all("span", {"class":"ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-label"})]
    square_footage = static_functions.get_squarefootage_mercadolibre(squarefootage_baths_rooms_str[0])
    rooms = static_functions.get_rooms_mercadolibre(squarefootage_baths_rooms_str[1])
    bathrooms = static_functions.get_bathrooms_mercadolibre(squarefootage_baths_rooms_str[2])
    amenities_str = soup.find("p", {"class":"ui-pdp-description__content"})
    am_str = str(amenities_str)
    amenities = static_functions.get_amenities_mercadolibre(am_str[am_str.index('">') + 2:])

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
        "amenities": amenities
    }
    #info.insert_many(details)

def get_posts_on_queue(link):
    global on_queue
    global crawled
    r = s.get(link)
    r.html.render(sleep=1)
    listings = r.html.xpath('//*[@class="ui-search shops__ui-main"]', first=True)
    for post in listings.absolute_links:
        if str(post) not in on_queue and post not in crawled:
            on_queue.append(str(post))

def next_in_pagination(link):
    #go through the pagination of the origin link
    r = s.get(link)
    r.html.render(sleep=1)
    next_page = r.html.xpath('//*[@class="andes-pagination__link shops__pagination-link ui-search-link"]', first=True)
    return next_page.absolute_links.pop()

if __name__ == '__main__':
    #current_page = get_total_pages_paginated()
    print(next_in_pagination(starting_point_link))
    #pages_counter = 5
    #while pages_counter > 0:
    #    get_post_info(on_queue[0])
    #    crawled.append(on_queue[0])
    #    on_queue.pop(0)
    #    pages_counter -= 1
    #    time_wait = 11
    #    print("waiting...")
    #    time.sleep(time_wait * 60)
    #    print("crawled")
    #    if len(on_queue) > 0:
    #        if len(on_queue) - 5 >= 0:
    #            pages_counter += 5
    #        else:
    #            pages_counter += 1
