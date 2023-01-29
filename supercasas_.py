import time
import requests
from bs4 import BeautifulSoup
from  requests_html import HTMLSession
import pymongo
import static_functions

on_queue = []
crawled = []

s = HTMLSession()
starting_point_link = "https://inmuebles.mercadolibre.com.do/apartamentos/alquiler/_NoIndex_True#unapplied_filter_id%3Dsince%26unapplied_filter_name%3DFiltro+por+fecha+de+comienzo%26unapplied_value_id%3Dtoday%26unapplied_value_name%3DPublicados+hoy%26unapplied_autoselect%3Dfalse"
#COROTOS CRAWLER
#parsing functions
link_id = 0
link_1 = "https://apartamento.mercadolibre.com.do/MRD-523714674-alquiler-apartamento-en-llanos-de-gurabo-santiago-ajp-203-_JM#position=1&search_layout=grid&type=item&tracking_id=6f58c769-ea24-45e4-8012-5b8058cc9f9b"

