import requests
import re
from json import JSONDecodeError
import json

first_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9047'

#获取城市编码
def getCity_Code(first_url,cityName):
    dic = {'cityName': '', 'cityCode': '', 'message': '', 'error': ''}
    try:
        reponse = requests.get(first_url)
        html = reponse.text
        city_index = html.index(cityName) + len(cityName) + 1
        cityCode = html[city_index:].split('|')[0]
        dic['cityName'] = cityName
        dic['cityCode'] = cityCode
        dic['message'] = 'Success'
        dic['error'] = False
        return dic
    except ValueError:
        dic['cityName'] = cityName
        dic['cityCode'] = 'null'
        dic['message'] = '无法找到对应城市'
        dic['error'] = True
        return dic

#获取开头相同的城市，并给予提示
def findOtherCity(cityName):
    FirstName = cityName[0:1]
    retest = r'\|' + FirstName + '(.*?)\|'
    first_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9047'
    reponse = requests.get(first_url)
    html = reponse.text
    cityList = re.findall(retest, html)
    print('你可能要找的以下这些城市')
    for city in cityList:
        print(FirstName+city)

#获取所有的售票信息
def getTcikerResult(StartStation,EndStation,Date):
    dic = {'result': '','error': ''}
    sec_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date='+Date+'&leftTicketDTO.from_station=' + StartStation + '&leftTicketDTO.to_station=' + EndStation + '&purpose_codes=ADULT'
    reponse = requests.get(sec_url)
    html = reponse.text
    # 查询结果解码成元组输出
    try:
        searchDic = json.loads(html)

        searchLen = len(searchDic['data']['result'])
        if searchLen > 0:
            # 长度大于零表示存在数据
            searchResult = searchDic['data']['result']

        else:
            dic = {'result': '无直达车次', 'error': False}
            return dic
        searchResult = searchDic['data']['result']

        dic = {'result': searchResult, 'error': True}
        return dic
    #可能存在转换json错误
    except JSONDecodeError:
        dic = {'result': '无直达车次', 'error': False}
        return dic


#将车次信息转换成字典格式
def PrintTciker(FromCityName,FromCityCode,ToCityName,ToCityCode,Date):
    dic = getTcikerResult(FromCityCode, ToCityCode,Date )
    list = []
    if dic['error']:
        for results in dic['result']:
            tickerDic = {'startCityName': '',
                         'startcityCode': '',
                         'endCityName': '',
                         'endCityCode': '',
                         'TrainName': '',
                         'StartDate': '',
                         'StartTime': '',
                         'EndTime': '',
                         'Ls': '',
                         'DayDown': '',
                         'business': '',  # 商务座
                         'One': '',  # 一等座
                         'Two': '',  # 二等座
                         'High_grade': '',  # 高级软卧
                         'solf_sleeper': '',  # 软卧
                         'solf_seet': '',  # 软座
                         'tourist_car': '',  # 硬卧
                         'hard_seats': '',  # 硬座
                         'no_seet': '',  # 无座
                         'dongwo': '',  # 动卧
                         'other': ''  # 其他
                         }
            result = results.split('|')
            tickerDic['startCityName'] = FromCityName
            tickerDic['startcityCode'] = FromCityCode
            tickerDic['endCityName'] = ToCityName
            tickerDic['endCityCode'] = ToCityCode
            tickerDic['TrainName'] = result[3]
            tickerDic['StartDate'] = CityName1
            tickerDic['StartTime'] = result[8]
            tickerDic['EndTime'] = result[9]
            tickerDic['Ls'] = result[10]
            tickerDic['DayDown'] = result[11]
            tickerDic['business'] = result[32]
            tickerDic['One'] = result[31]
            tickerDic['Two'] = result[30]
            tickerDic['High_grade'] = result[29]
            tickerDic['solf_sleeper'] = result[23]
            tickerDic['solf_seet'] = result[24]
            tickerDic['tourist_car'] = result[28]
            tickerDic['hard_seats'] = result[21]
            tickerDic['no_seet'] = result[26]
            tickerDic['dongwo'] = result[27]
            tickerDic['other'] = result[22]
            list.append(tickerDic)
    else:
        return(dic)
    dic['result'] = list
    dic['error'] = True
    return dic

#将城市转为编码
def StringToCode(CityList):
    CityDic = {'FromCity':'','FromCityCode':'','ToCity':'','ToCityCode':''}
    index = 1
    for city in CityList:
        dic = getCity_Code(first_url, city)
        if dic['error']:
            print(dic['message'] + "(" + dic["cityName"] + ")。请确认后重新输入")
            findOtherCity(CityName1)
            exit()
        else:
            if index == 1:
                CityDic['FromCity']=city
                CityDic['FromCityCode'] = dic['cityCode']
            else:
                CityDic['ToCity'] = city
                CityDic['ToCityCode'] = dic['cityCode']
        index=index+1
    return CityDic


if __name__=='__main__':
    CityName1 = input("请输入出发地:")
    CityName2 = input("请输入目的地:")
    Date = input('请输入出发日期(例如2018-02-10):')
    #加上参数校验
    print('数据查询中，请稍后.......')

    CityList = (CityName1,CityName2)

    CityDic = StringToCode(CityList)


    list = PrintTciker(CityDic['FromCity'],CityDic['FromCityCode'],CityDic['ToCity'],CityDic['ToCityCode'],Date)

    if list['error']:
        fileName = Date + ':' + CityName1 + '到' + CityName2 + '车票查询.txt'
        f = open(fileName, 'w')
        for infos in list['result']:
            str1 = '车次:'+infos['TrainName']+',出发站:'+infos['startCityName']+',目的地:'+infos['endCityName']+',出发时间:'+infos['StartTime']+',到达时间:'+infos['EndTime']+',历时:'+infos['Ls']+'h,\n'
            str2 = '座位情况: 商务座:「'+(infos['business'] or '---')+'」,一等座:「'+(infos['One'] or '---')+'」,二等座:「'+(infos['Two'] or '---')+'」,动卧:「'+(infos['dongwo'] or '---')+'」,高级软卧:「'+(infos['High_grade'] or '---')+'」,软卧:「'+(infos['solf_sleeper'] or '---')+'」,软座:「'+(infos['solf_seet'] or '---')+'」,硬卧:「'+(infos['tourist_car'] or '---')+'」,硬座:「'+(infos['hard_seats'] or '---')+'」,无座:「'+(infos['no_seet'] or '---')+'」,其他:「'+(infos['other'] or '---')+'」\n'
            str3 = '=============================================================\n'
            f.write(str1+str2+str3)
        print('数据输出完成')
        f.close()
    else:
        print(list['result'])