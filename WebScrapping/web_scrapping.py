# importing the lib
from functools import cached_property
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import time
import sys
from selenium.webdriver.chrome.service import service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import flask
from flask import request
from flask_cors import CORS, cross_origin
from selenium.webdriver import Remote
import chromedriver_binary
import re
app = flask.Flask(__name__)
CORS(app, support_credentials=True)
app.config["DEBUG"] = True


@app.route('/site_open', methods=['POST'])
@cross_origin(supports_credentials=True)
def site_open():
    print(request.data, file=sys.stderr)
    request_data = request.get_json()
    source_airport = request_data['source']
    destination_airport =request_data['destination']
    doj = request_data['date']
    mode=None
    try:
        mode = request_data['type']
    except:
        mode=None
    person = str(request_data['person'])
    url="https://www.ca.kayak.com/flights/" +str(source_airport) +"-" +str(destination_airport)+ "/"+str(doj)+ "?sort=bestflight_a"

    # options = Options()
    # options.page_load_strategy = 'normal'
    # options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    print(mode)
    driver=None
    if mode=='cicd':
        driver = Remote(
            command_executor='http://selenium__standalone-firefox:4444/wd/hub',
            desired_capabilities={'browserName': 'firefox'}
        )
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

    driver.maximize_window()
    driver.get(url)
    time.sleep(20)
    def click_more():
    
        for val in range(0,1):
            try:
                driver.find_element_by_xpath("//a[@class='moreButton']").click()
                time.sleep(5)
                val = val +1

            except:
                pass
    click_more()
    
    # depart-time base-time
    departure_time=[]
    departure_time= driver.find_elements_by_xpath("//ol[@class='flights']//span[@class='depart-time base-time']")

    arrival_time=[]
    arrival_time= driver.find_elements_by_xpath("//ol[@class='flights']//span[@class='arrival-time base-time']")

    duration =[]
    duration  = driver.find_elements_by_xpath("//ol[@class='flights']//div[@class='section duration allow-multi-modal-icons']//div[@class='top']")

    no_stop = []
    no_stop  = driver.find_elements_by_xpath("//ol[@class='flights']//div[@class='section stops']//div[@class='top']")

    price =[]
    price = driver.find_elements_by_xpath("//div[@class = 'booking']")

    airlines = []
    airlines = driver.find_elements_by_xpath("//span[@class = 'codeshares-airline-names']")

    # departure_time = driver.find_elements_by_xpath("//div[@class='itinerary-depart-time depart-time']")

    price_list=[]
    stops=[]
    for i in range(len(departure_time)):
        departure_time[i]= departure_time[i].get_attribute('innerHTML')
        arrival_time[i] = arrival_time[i].get_attribute('innerHTML')
        duration[i] = duration[i].get_attribute('innerHTML')
        no_stop[i] = no_stop[i].get_attribute('innerHTML')
        l = re.findall("(direct|1|2|3|4|5)",no_stop[i])[0]
        stops.append(l)
        price[i] = price[i].get_attribute('innerHTML')

#         airlines[i] = airlines[i].get_attribute('innerHTML')
        b = re.findall("nbsp\;((\d\d\d)|(\d.\d\d\d)|(\d\d.\d\d\d))",price[i])[0][0]
        price_list.append(b)
    
    for k in range(len(airlines)):
        airlines[k] = airlines[k].get_attribute('innerHTML')
        
    # Creating data frames
    departure = len(departure_time)*[str(source_airport)]
    arrival = len(departure_time)*[str(destination_airport)]
    # a = pd.DataFrame(departure_time,arrival_time,price_list)
    doj1 = len(departure_time)*[doj]
    df  = pd.DataFrame(doj1,columns=["Date"])
    df["Source"] = departure    
    df["Destination"] = arrival
    df["Departure_time"] = departure_time
    df["Arrival_time"] = arrival_time
    df["Duration"] = duration
    df["Stops"] = stops
    df["CAD"]= price_list
    df["Airlines"] = airlines
#     df["Stops"]=df["Stops"].astype(str).str.replace("\n","")
    df["CAD"]=df["CAD"].astype(str).str.replace(",","")
    df["CAD"] = pd.to_numeric(df['CAD'])
#     df["Stops"]=df["Stops"].astype(str).str.replace("stops","")
#     df["Stops"]=df["Stops"].astype(str).str.replace("stop","")
    df["Duration"]=df["Duration"].astype(str).str.replace("\n","")
    df = df.drop(df[(df.Stops =='3') | (df.Airlines == 'Multiple Airlines')].index)
    df= df.drop_duplicates()
    df = df.sort_values(by='CAD')
    df = df.reset_index()
    df.index = df.index +1
    df.pop("index")
    driver.close()


    cache_data = pd.read_csv("kayak1_data.csv")

    cache_data.drop( cache_data.index[ (cache_data['Date'] == doj) & (cache_data['Source']==source_airport) & (cache_data['Destination']== destination_airport) ], inplace=True)

    cache_data = pd.concat( [cache_data, df])

    #cache_data.reset_index(inplace=True)
    cache_data.to_csv("kayak1_data.csv", index=False)
    return df.to_json(orient='records')


@app.route('/site_open/cache', methods=['POST'])
@cross_origin(supports_credentials=True)
def cache():
    print(request.data, file=sys.stderr)
    request_data = request.get_json()
    source_airport = request_data['source']
    destination_airport =request_data['destination']
    doj = request_data['date']
    mode=None
    try:
        mode = request_data['type']
    except:
        mode=None
    person = str(request_data['person'])

    df = pd.read_csv('kayak1_data.csv')
    df1 = df[(df["Source"] == source_airport) & (df["Destination"]==destination_airport) & (df["Date"] == doj)]
    print(df1)
    #df1.reset_index(inplace=True)
    return df1.to_json(orient='records')


app.run()


