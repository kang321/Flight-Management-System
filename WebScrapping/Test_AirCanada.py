# coding: utf-8

# In[11]:
import requests
from requests_html import HTMLSession
import unittest
from unittest.mock import patch
import nest_asyncio
import re
import random
from datetime import datetime
from datetime import date
import pandas as pd
# source = "YYZ"
# destination = "DEL"
# date = "03/07/2022"


import sys


class Travel:
    def __init__(self, date, source, destination, Departure_time, Arrival_time, Duration, Stops, CAD, Airlines):
        self.date = date
        self.source = source
        self.destination = destination
        self.Departure_time = Departure_time
        self.Arrival_time = Arrival_time
        self.Duration = Duration
        self.Stops = Stops
        self.CAD = CAD
        self.Airlines = Airlines

    def url_validity(self):
        # url = "https://www.aircanada.com/ca/en/aco/home/app.html#/search?org1="+self.source+"&dest1="+self.destination+"&orgType1=A&destType1=A&departure1="+self.date+"&marketCode=INT&numberOfAdults="+self.person+"&numberOfYouth=0&numberOfChildren=0&numberOfInfants=0&numberOfInfantsOnSeat=0&tripType=O&isFlexible=false"
        
        url = "https://www.ca.kayak.com/flights/" + self.source + "-" + self.destination + "/" + self.date.replace("/",
                                                                                                                   "-") + "2022-05-30?sort=bestflight_a"
        nest_asyncio.apply()

        session = HTMLSession()
        # print(session.get(url))
        try:
            r = session.get(url)
        except:
            return 'Bad Response!'
        # print(r)

        if r.ok:
            return 'positive response'
        else:
            return 'Bad Response!'

    def date_validity(self):
        # format = "%m/%d/%Y"
        format = "%d-%m-%Y"
        # checking if format matches the date
        res = True
        try:
            res = bool(datetime.strptime(self.date, format))
        except ValueError:
            res = False
        return res

    def backdate_validaity(self):
        # format = "%m/%d/%Y"
        Flag = False
        date1 = str(date.today())
        date2 = str(self.date)
        y1, m1, d1 = date1[0:4], date1[5:7], date1[8:10]
        d2, m2, y2 = date2[0:2], date2[3:5], date2[6:10]
        b1 = date(int(y1), int(m1), int(d1))
        b2 = date(int(y2), int(m2), int(d2))
        try:
            Flag = bool(b1 > b2)
        except ValueError:
            Flag = False
        return Flag

    def source_airport_validation(self):

        airport_list = ["DEL", "BOM", "BLR", "AMD", "IXC", "YYZ", "YYC", "YVR", "YQB", "YHZ"]
        Flag = False

        try:
            if self.source in airport_list:
                Flag = True
        except ValueError:
            Flag = False
        return Flag

    def destination_airport_validation(self):

        airport_list = ["DEL", "BOM", "BLR", "AMD", "IXC", "YYZ", "YYC", "YVR", "YQB", "YHZ"]
        Flag = False

        try:
            if self.destination in airport_list:
                Flag = True
        except ValueError:
            Flag = False
        return Flag

    def departure_time_validation(self):
        pattern_match = re.match(r'^\d\d?:\d\d?\s[ap]\.m\.\s*$', self.Departure_time)
        Flag = False

        try:
            if (pattern_match):
                Flag = True
        except ValueError:
            Flag = False
        return Flag

    def arrival_time_validation(self):
        pattern_match = re.match(r'^\d\d?:\d\d?\s[ap]\.m\.\s*$', self.Arrival_time)
        Flag = False

        try:
            if (pattern_match):
                Flag = True
        except ValueError:
            Flag = False
        return Flag

    def duration_validation(self):
        pattern_match = re.match(r'^\d\d?h\s\d\d?m\s*$', self.Duration)
        Flag = False

        try:
            if (pattern_match):
                Flag = True
        except ValueError:
            Flag = False
        return Flag

    def no_of_stops_validation(self):
        pattern_match = re.match(r'^\d\s*$', self.Stops)
        Flag = False

        try:
            if (pattern_match):
                Flag = True
        except ValueError:
            Flag = False
        return Flag

    def cost_format_validation(self):
        pattern_match = re.match(r'^\d+\s*$', self.CAD)
        Flag = False

        try:
            if (pattern_match):
                Flag = True
        except ValueError:
            Flag = False
        return Flag


class TestAirCanada(unittest.TestCase):
    mode = ""
    def setUp(self):
        print('setUp')
        self.travel1 = Travel("22-03-2022", "DEL", "YYZ", "9:50 p.m.", "3:40 p.m.", "27h 20m", "2", "917",
                              "Gulf Air, Air Transat")
        self.travel2 = Travel("30-02-2022", "NYC", "YYZ", "9:50p.m.", "1:55 p.m.", "25h  35m", "22", "1026",
                              "Gulf Air, Air Canada")
        self.travel3 = Travel("02-02-2021", "DEL", "YYZ", "8:00 a.m.", "8:15 p.m.", "21h 45m", "1", "CAD", "LOT")
        self.travel4 = Travel("04-04-2022", "DEL", "BJW", "11:35 p.m.", "1:09 pm.", "23h 04m", "1", "1145",
                              "United Airlines")
        # self.travel1 = Travel("03/09/2022", "DEL", "YYZ", "9:50 p.m.", "3:40 p.m.", "27h 20m", "2", "917", "Gulf Air, Air Transat")
        # self.travel2 = Travel("02/30/2022", "DEL", "YYZ", "9:50 p.m.", "1:55 p.m.", "25h 35m", "2", "1026", "Gulf Air, Air Canada")
        # self.travel3 = Travel("02/09/2021", "DEL", "YYZ", "8:00 a.m.", "8:15 p.m.", "21h 45m", "1", "1121", "LOT")
        # self.travel4 = Travel("04/09/2022", "DEL", "YYZ", "11:35 p.m.","1:09 p.m.", "23h 04m", "1", "1145", "United Airlines")

    def tearDown(self):
        print('tearDown\n')

    def test_url_validity(self):
        print('test_url_validity')
        # print(self.travel1.url_validity())
        print(self.travel1.url_validity())
        self.assertEqual(self.travel1.url_validity(), 'positive response')

    def test_date_format_check(self):
        print('test_datformate_check')
        # print(self.travel2.url_validity())
        self.assertEqual(self.travel1.date_validity(), True)
        self.assertEqual(self.travel2.date_validity(), False)

    def test_back_date_check(self):
        print("check for backdate")
        self.assertEqual(self.travel3.backdate_validaity(), True)
        self.assertEqual(self.travel4.backdate_validaity(), False)

    def test_source_airport(self):
        print("source airport validation")
        self.assertEqual(self.travel1.source_airport_validation(), True)
        self.assertEqual(self.travel2.source_airport_validation(), False)

    def test_Destination_airport(self):
        print("Destination airport validation")
        self.assertEqual(self.travel3.destination_airport_validation(), True)
        self.assertEqual(self.travel4.destination_airport_validation(), False)

    def test_departure_time(self):
        print("Departure time validation")
        self.assertEqual(self.travel1.departure_time_validation(), True)
        self.assertEqual(self.travel2.departure_time_validation(), False)

    def test_arrival_time(self):
        print("Arrival time validation")
        self.assertEqual(self.travel3.arrival_time_validation(), True)
        self.assertEqual(self.travel4.arrival_time_validation(), False)

    def test_duration(self):
        print('validate duration')
        self.assertEqual(self.travel1.duration_validation(), True)
        self.assertEqual(self.travel2.duration_validation(), False)

    def test_stopage_validation(self):
        print('validate duration')
        self.assertEqual(self.travel1.no_of_stops_validation(), True)
        self.assertEqual(self.travel2.no_of_stops_validation(), False)

    def test_cost_format(self):
        print('validate duration')
        self.assertEqual(self.travel3.cost_format_validation(), False)
        self.assertEqual(self.travel4.cost_format_validation(), True)

    def test_response_type(self):
        temp = requests.post('http://127.0.0.1:5000/site_open', json=
        {

            "source": "YYZ",
            "destination": "DEL",
            "date": "2022-05-30",
            "person": "1",
            "type": self.mode
        })
        self.assertGreater(len(temp.json()), 0)


    def test_response_type_wrong(self):
        temp = requests.post('http://127.0.0.1:5000/site_open', json=
        {

            "source": "YYZ36",
            "destination": "DEL",
            "date": "2022-05-30",
            "person": "1",
            "type": self.mode
        })

        self.assertEqual(temp.status_code, 500)

    # def test_response_type_sorted(self):

    #     temp = requests.post('http://127.0.0.1:5000/site_open' , json =
    #      {
    #             "source" : "YYZ",
    #             "destination" : "DEL",
    #             "date" : "2022-05-30",
    #             "person": "1"
    #      })

    #     self.assertLess( list(map(int, re.findall(r'\d+', temp.json()[0]['Economy_Class'])))[0] ,  list(map(int, re.findall(r'\d+', temp.json()[-1]['Economy_Class'])))[0] )


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestAirCanada.mode = sys.argv.pop()
    unittest.main()


