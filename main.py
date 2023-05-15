import requests
import time
from bs4 import BeautifulSoup
from  requests_html import HTMLSession

#corotos
#import corotos_onqueue
#import corotos_saveposts
#import corotos_saveposts_errors

#supercasas
#import supercasas_onqueue
#import supercasas_saveposts
#import supercasas_saveposts_errors

#mercadolibre
#import mercadolibre_onqueue
#import mercadolibre_savepost
#import mercadolibre_savepost_errors

s = HTMLSession()

def get_US_to_DOP_exchange_rate():
    r = s.get("https://www.google.com/search?client=firefox-b-d&q=dolar+a+peso+dominicano")
    r.html.render(sleep=1)    
    page_html = r.html
    er  = page_html.find('.b1hJbf')
    data_exchange_rate = str(er[0])
    return float("{:.2f}".format(float(data_exchange_rate[data_exchange_rate.index("data-exchange-rate='")+20:-2])))

#print(get_US_to_DOP_exchange_rate())
#if __name__ == '__main__':
    #while(True):
        #onqueue - scripts
        #supercasas_onqueue.get_on_queue()
        #corotos_onqueue.get_on_queue()
        #mercadolibre_onqueue.get_posts_on_queue()

        #saveposts - scripts
        #supercasas_saveposts.get_save_post()
        #corotos_saveposts.get_save_post()
        #mercadolibre_savepost.get_save_post()

        #try saving error posts
        #supercasas_saveposts_errors.get_save_posts_errors()
        #corotos_saveposts_errors.get_saveposts_errors()
        #mercadolibre_savepost_errors.get_save_posts_errors()

        #time.sleep(10 * 60)
        
import pickle as pkl
import numpy as np
filenm = 'LR_model.pickle'
lr_pickle = pkl.load(open(filenm, 'rb'))

def predict_my_rental(rooms,bathrooms,squarefootage,province,banos,
                      aguaPotable,aireAcondicionado,areaJuegosInfantiles,
                      areaServicio,ascensor,balcon,cisterna,controlAcceso,
                      cuartoServicio,estarFamiliar,estudio,gazebo,gimnasio,
                      inversor,jacuzzi,lobby,patio,picuzzi,piscina,plantaElectrica,
                      pozo,satelite,sauna,seguridad,shutters,terraza,vestidores):
    
    filenm = 'LR_model.pickle'
    lr_pickle = pkl.load(open(filenm, 'rb'))
    _input = np.array([[rooms,bathrooms,squarefootage,province,banos,
                        aguaPotable,aireAcondicionado,areaJuegosInfantiles,
                        areaServicio,ascensor,balcon,cisterna,controlAcceso,
                        cuartoServicio,estarFamiliar,estudio,gazebo,gimnasio,
                        inversor,jacuzzi,lobby,patio,picuzzi,piscina,plantaElectrica,
                        pozo,satelite,sauna,seguridad,shutters,terraza,vestidores]])
    
    return lr_pickle.predict(_input)[0]
#examples
#price: 89166.0, || 1.0,1.5,78.0,5,1,1,1,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,0,1,1,0,0,0,1,0,0,1
# #price: 70252.0, || 2.0,2.5,160.0,5,1,0,0,1,0,1,1,1,1,1,0,1,0,1,0,0,1,0,0,1,1,0,0,0,1,0,1,1
print(predict_my_rental(2.0,2.5,160.0,5,1,0,0,1,0,1,1,1,1,1,0,1,0,1,0,0,1,0,0,1,1,0,0,0,1,0,1,1))