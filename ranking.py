import requests
from bs4 import BeautifulSoup
from  requests_html import HTMLSession
from sklearn.impute import SimpleImputer

provinces_names = ["Azua", "Bahoruco", "Barahona", "Dajabon", "Duarte", "El-Seibo", 
             "Elias-Pina", "Espaillat", "Hato-Mayor", "Hermanas-Mirabal",
             "Independencia", "La-Altagracia", "La-Romana", "La-Vega"
             "Maria-Trinidad-Sanchez", "Monsenor-Nouel", "Monte-Cristi",
             "Pedernales", "Peravia", "Puerto-Plata", "Samana", "San-Cristobal",
             "San-Jose-de-Ocoa", "San-Juan", "San-Pedro-De-Macoris", "Sanchez-Ramirez",
             "Santiago", "Santiago-Rodriguez", "Santo-Domingo", "Valverde",
             "Distrito-Nacional", "Monte-Plata"]

#provinces
azua = "https://www.airbnb.com/s/Azua--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=search_query"
bahoruco = "https://www.airbnb.com/s/Bahoruco--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=search_query"
barahona = "https://www.airbnb.com/s/Barahona--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=search_query"
dajabon = "https://www.airbnb.com/s/Dajabon--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Dajabon%2C%20Dominican%20Republic&place_id=ChIJN1PcDHYhsY4Rfb0wT6XQqoU&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
duarte = "https://www.airbnb.com/s/Duarte--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=search_query"
el_seibo = "https://www.airbnb.com/s/El-Seibo--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=search_query"
elias_piña = "https://www.airbnb.com/s/El%C3%ADas-Pi%C3%B1a--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=El%C3%ADas%20Pi%C3%B1a%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJZzeVDwe7sI4RgpnnEeYzTLE&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
espaillat = "https://www.airbnb.com/s/Espaillat--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Espaillat%2C%20Rep%C3%BAblica%20Dominicana&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&place_id=ChIJy7sB8pcUro4RV1HTDjWjtN0"
hato_mayor = "https://www.airbnb.com/s/Hato-Mayor--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Hato%20Mayor%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJrTKTGnQUr44RjVjg9-hU1HI&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
hermanas_mirabal = "https://www.airbnb.com/s/Hermanas-Mirabal--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Hermanas%20Mirabal%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJg-6o36Yoro4RM2AZ9d6Fxmo&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
independencia = "https://www.airbnb.com/s/Independencia--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&query=Independencia%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJK7C4Z_MSuo4RQRLcQfOH2xY"
la_altagracia = "https://www.airbnb.com/s/La-Altagracia--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=La%20Altagracia%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJQTzPG5sapo4RNWuVsD4KAFg&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
la_romana = "https://www.airbnb.com/s/La-Romana--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=La%20Romana%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJK8xQ8mhUr44R2ZnryF_lSxc&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
la_vega = "https://www.airbnb.com/s/La-Vega--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=La%20Vega%2C%20Dominican%20Republic&place_id=ChIJCxifGZ0ssI4RSNC_MN_oW1s&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
maria_trinidad_sanchez = "https://www.airbnb.com/s/Mar%C3%ADa-Trinidad-S%C3%A1nchez--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Mar%C3%ADa%20Trinidad%20S%C3%A1nchez%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJw6EOdppGro4RMUX_pgQFJ94&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
monsenor_nouel = "https://www.airbnb.com/s/Monse%C3%B1or-Nouel--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Monse%C3%B1or%20Nouel%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJiVTpNTTer44Rt6f5dyEYclo&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
monte_cristi = "https://www.airbnb.com/s/Monte-Cristi--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Monte%20Cristi%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJUwpeiulDsY4RnzqSspIitLk&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
pedernales = "https://www.airbnb.com/s/Pedernales--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Pedernales%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJd-5eMsAxuo4RthOCeyM4jJg&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
peravia = "https://www.airbnb.com/s/Peravia--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Peravia%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJE_8VH35OpY4RcWKcM6lzklU&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
puerto_plata = "https://www.airbnb.com/s/Puerto-Plata--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Puerto%20Plata%2C%20Dominican%20Republic&place_id=ChIJdfpGAD_usY4RZ3TZhgIwwRA&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
samana = "https://www.airbnb.com/s/Samana--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Samana%2C%20Dominican%20Republic&place_id=ChIJIQTGJyvnro4RE5BtH05W3gA&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
san_cristóbal = "https://www.airbnb.com/s/San-Crist%C3%B3bal--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=San%20Crist%C3%B3bal%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJU092ovJepY4Rllgy9Fhg5-U&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
san_jose_de_ocoa = "https://www.airbnb.com/s/San-Jose-de-Ocoa--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=San%20Jose%20de%20Ocoa%2C%20Dominican%20Republic&place_id=ChIJ4QdWseoAsI4RdS7sKWwbxNs&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
san_juan = "https://www.airbnb.com/s/San-Juan--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=San%20Juan%2C%20Dominican%20Republic&place_id=ChIJXaI4WV2IsI4RWY86fbv2OW0&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
san_pedro_de_macoris = "https://www.airbnb.com/s/San-Pedro-de-Macoris--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=San%20Pedro%20de%20Macoris%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJDaK7iJNgr44RxARd5PxCAVo&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
sanchez_ramirez = "https://www.airbnb.com/s/S%C3%A1nchez-Ram%C3%ADrez--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=S%C3%A1nchez%20Ram%C3%ADrez%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJw-gGMw7Gr44RxdP2-rHuZEw&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
santiago = "https://www.airbnb.com/s/Santiago--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Santiago%2C%20Dominican%20Republic&place_id=ChIJn4nlOMjFsY4RKYR2uFmw1HU&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
santiago_rodriguez = "https://www.airbnb.com/s/Santiago-Rodr%C3%ADguez--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Santiago%20Rodr%C3%ADguez%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJnU2mu3UDsY4RtuOgExPlVwM&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
santo_domingo = "https://www.airbnb.com/s/Santo-Domingo--Dominican-Republic/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Santo%20Domingo%2C%20Dominican%20Republic&place_id=ChIJs21C9kZ-r44R0m6IgNibyFo&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
valverde = "https://www.airbnb.com/s/Valverde--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Valverde%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJZ15RkgCjsY4RHx0jwaKlDfw&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
distrito_nacional = "https://www.airbnb.com/s/Distrito-Nacional--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Distrito%20Nacional%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJ9bbx3jiIr44Rn83_cBw_FCk&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
monte_plata = "https://www.airbnb.com/s/Monte-Plata--Rep%C3%BAblica-Dominicana/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-06-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Monte%20Plata%2C%20Rep%C3%BAblica%20Dominicana&place_id=ChIJI4EMHaGYr44RiklvPdBL-xg&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"

provinces = [azua, bahoruco, barahona, dajabon, duarte, el_seibo, elias_piña, 
             espaillat, hato_mayor, hermanas_mirabal, independencia, la_altagracia, 
             la_romana, la_vega, maria_trinidad_sanchez, monsenor_nouel, monte_cristi, 
             pedernales, peravia, puerto_plata, samana, san_cristóbal, san_jose_de_ocoa,
             san_juan, san_pedro_de_macoris, sanchez_ramirez, santiago, santiago_rodriguez,
             santo_domingo, valverde, distrito_nacional, monte_plata]

def get_next_page(url):
    response = session.get(url)
    css_selector = '.l1j9v1wn c1ytbx3a dir dir-ltr'  # Replace with the class selector of the element you're targeting
    element = response.html.find_all(css_selector, first=True)  # Find the first occurrence of the element
    return element.attrs['href']  

session = HTMLSession()
def get_amount_reviews(province_start_link):
    url = 'province_start_link'  # Replace with the URL of the webpage you want to scrape
    response = session.get(url)
    css_selector = '.your-class'  # Replace with the class selector of the element you're targeting
    element = response.html.find_all(css_selector, first=True)  # Find the first occurrence of the element
    attribute_value = element.attrs['href'] 

example = "something 5 reviews"

import pandas as pd
import numpy as np


df = pd.read_csv('ranking_provincias.csv')
# Generate random missing values on column MaxSpeed
mask = np.random.choice([True, False], size=df['PrecioBase'].shape, p=[0.1, 0.9])
mask[mask.all(),-1] = 0
df['PrecioBase'] = df['PrecioBase'].mask(mask)

# Mean Imputation
df_mean = df.copy()
mean_imputer = SimpleImputer(strategy='mean')
df_mean['PrecioBase'] = mean_imputer.fit_transform(df_mean['PrecioBase'].values.reshape(-1,1))
#reviews class t5eq1io r4a59j5 dir dir-ltr
#next page class l1j9v1wn c1ytbx3a dir dir-ltr


