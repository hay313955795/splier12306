#\|成(.*?)\|


import requests
import re


def findOtherCity(cityName):
    cityName = '成都上'
    FirstName = cityName[0:1]
    retest = r'\|'+FirstName+'(.*?)\|'
    first_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9047'

    reponse = requests.get(first_url)
    html = reponse.text

    cityList = re.findall(retest,html)

    return cityList
