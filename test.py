import requests

payload = {
    'leftTicketDTO.train_date': '2018-02-12',
    'leftTicketDTO.from_station': 'VRH',
    'leftTicketDTO.to_station': 'HGH',
    'purpose_codes': 'ADULT'
}
print(payload)
url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ'
reqs = requests.get(url,  params=payload)#, params=payload
print(reqs.url)
print(reqs.text)