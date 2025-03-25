import csv
import os
import re
import time
from bs4 import BeautifulSoup
from DrissionPage import ChromiumOptions, ChromiumPage, WebPage
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse


def read_file_to_list(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            # 使用列表推导式读取每一行
            content_list = [line.strip() for line in file]
        return content_list

def FlightsPage(departurePlace,arrivePlace,departureDate):
    do1 = ChromiumOptions().set_paths(local_port=9111, user_data_path=r'D:\data1')
    do2 = ChromiumOptions().set_paths(local_port=9112, user_data_path=r'D:\data2')

    page = ChromiumPage(addr_or_opts=do1)
    page_flag = 1
    page.get('https://flights.ctrip.com/online/list/oneway-' + departurePlace + '-' + arrivePlace + '?depdate='+ departureDate + '&cabin=y_s_c_f&adult=1&child=0&infant=0')    
    if page.ele('@text()=阅读并同意携程的服务协议和个人信息保护政策') != None:
        print('close')
        page.close()
        time.sleep(100)
        if page_flag == 1:
            page = ChromiumPage(addr_or_opts=do2)
            page_flag = 2
        else:
            page = ChromiumPage(addr_or_opts=do1)
        page.get('https://flights.ctrip.com/online/list/oneway-' + departurePlace + '-' + arrivePlace + '?depdate='+ departureDate + '&cabin=y_s_c_f&adult=1&child=0&infant=0')
    if page.ele('xpath:/html/body/div[1]/div[2]/div[2]/div/div[6]/div/div/div[2]/div/div[2]/div/div/div[1]') != None:
        print('验证close')
        page.close()
        time.sleep(100)
        if page_flag == 1:
            page = ChromiumPage(addr_or_opts=do2)
        else:
            page = ChromiumPage(addr_or_opts=do1)
        page.get('https://flights.ctrip.com/online/list/oneway-' + departurePlace + '-' + arrivePlace + '?depdate='+ departureDate + '&cabin=y_s_c_f&adult=1&child=0&infant=0')
    
    old_lst_length = 0
    flag = 0
    count = 0
    p = 0
    while True:
        lst = page.s_eles('xpath://*[@id="hp_container"]/div[2]/div/div[3]/div[3]/div[2]/span/div')
        if count > 1:
            break        
        if flag == 0:
            if len(lst) == 0:
                time.sleep(0.5)
                p += 1
                print(1)
                if p >= 2:
                    break

                if page.ele('xpath://*[@id="hp_container"]/div[2]/div/div[2]/div[2]/div/div/div'):
                    count+=1
                    print(2)
                    if count <= 1:
                        page.get('https://flights.ctrip.com/online/list/oneway-&#39'  + departurePlace + '-' + arrivePlace + '?depdate='+ departureDate + '&cabin=y_s_c_f&adult=1&child=0&infant=0')
                continue
            else:
                default_size = len(lst)
                cont = 0
                while True:
                    cont += 1
                    page.scroll.down(400)
                    lst = page.s_eles('xpath://*[@id="hp_container"]/div[2]/div/div[3]/div[3]/div[2]/span/div')
                    if len(lst) != default_size:
                        print("finish first scroll!")
                        break
                    if cont >= 2:
                        break
                flag = 1
        if len(lst) == old_lst_length:
            break
        old_lst_length = len(lst)
        page.scroll.down(600)
        time.sleep(0.75)
        print("scroll again!")
        
    soup=BeautifulSoup(page.html,"html.parser")
    return soup,p


def AirlineNameDiv(FlightsDiv):
    return FlightsDiv.find_all("div",{"class":"airline-name"})

def AirlineNameDivFirst(FlightsDiv):
    return FlightsDiv.find_all("div",{"class":"airline-name"})

def GetDpDiv(FlightsDiv):
    return FlightsDiv.find("div",{"class":"depart-box"})

def GetArrDiv(FlightsDiv):
    return FlightsDiv.find("div",{"class":"arrive-box"})

def GetDpAirport(FlightsDiv):
    return GetDpDiv(FlightsDiv).find("div",{"class":"airport"}).text

def GetDpTime(FlightsDiv):
    return GetDpDiv(FlightsDiv).find("div",{"class":"time"}).text

def GetArrAirport(FlightsDiv):
    return GetArrDiv(FlightsDiv).find("div",{"class":"airport"}).text

def GetArrTime(FlightsDiv):
    return GetArrDiv(FlightsDiv).find("div",{"class":"time"}).text

def GetFlightInformation(FlightsDiv):
    return FlightsDiv.find("div",{"class":"transfer-info-group"}).text

def GetFlightPrice(FlightsDiv):
    return FlightsDiv.find("span",{"class":"price"}).text

def GetFlightLowPrice(FlightsDiv):
    print("\n\n\n\n:",FlightsDiv.find("id",{"class":"travelPackage_price_undefined"}).text)
    return FlightsDiv.find("id",{"class":"travelPackage_price_undefined"}).text

def ReviseResult(FlightsDiv,airlineName):
    result={
    'airline': 'null',
    'departure_airport': 'null',
    'arrival_airport': 'null',
    'departure_time': 'null',
    'arrival_time': 'null',
    'FlightInformation':'null',
    'price': 'null'
    }
    result['airline'] = airlineName
    if 'span' in str(result['airline'][0]):
        result['airline'] = airlineName[0].text
    result['departure_airport']=GetDpAirport(FlightsDiv)
    result['arrival_airport']=GetArrAirport(FlightsDiv)
    result['departure_time']=GetDpTime(FlightsDiv)
    result['arrival_time']=GetArrTime(FlightsDiv)     
    result['FlightInformation']=GetFlightInformation(FlightsDiv)
    result['price']=GetFlightPrice(FlightsDiv)
    if result['price'] == None:
        result['price']=GetFlightLowPrice(FlightsDiv)
    return result

def DataProcessing(FlightsDiv):
    if len(AirlineNameDiv(FlightsDiv)) == 2:
      return  ReviseResult(FlightsDiv,[AirlineNameDiv(FlightsDiv)[0].contents[0],AirlineNameDiv(FlightsDiv)[1].contents[0]])
    elif len(AirlineNameDiv(FlightsDiv)) == 1:
      return  ReviseResult(FlightsDiv,[AirlineNameDiv(FlightsDiv)[0].contents[0]])

def write_to_csv(data, filename, write_header=True):
    # 写入CSV文件的逻辑保持不变，确保写入模式为追加
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if write_header and os.path.getsize(filename) == 0:  # 检查文件是否为空，且需要写入标题
            writer.writerow(['Airline', 'Departure Airport', 'Arrival Airport', 'Departure Time', 'Arrival Time', 'Flight Information', 'Price'])
        writer.writerow([data['airline'], data['departure_airport'], data['arrival_airport'], data['departure_time'], data['arrival_time'], data['FlightInformation'], data['price']])


def AllFlights(allFlightsDiv):
    for FlightsDiv in allFlightsDiv[1:]:
        print(DataProcessing(FlightsDiv))

def query_flights_route(departure_city, arrival_city, departure_date, filename):
    if os.path.isfile(filename):
        print(f"File '{filename}' already exists. Skipping query for {departure_city} to {arrival_city}.")
        return
    
    
    print(f"Querying flights from {departure_city} to {arrival_city} on {departure_date}...")
    soup,p = FlightsPage(departure_city, arrival_city, departure_date)
    
    if p < 2:
        allFlightsDiv = soup.find_all("div", {"class": "flight-box"})


        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if os.path.getsize(filename) == 0:  # 如果文件为空，则写入标题行
                    writer.writerow(['Airline', 'Departure Airport', 'Arrival Airport', 'Departure Time', 'Arrival Time', 'Flight Information', 'Price'])
            for FlightsDiv in allFlightsDiv[1:]:
                flight_data = DataProcessing(FlightsDiv)
                if flight_data != None:
                    writer.writerow([
                        flight_data['airline'],
                        flight_data['departure_airport'],
                        flight_data['arrival_airport'],
                        flight_data['departure_time'],
                        flight_data['arrival_time'],
                        flight_data['FlightInformation'],
                        flight_data['price']
                    ])
    else:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if os.path.getsize(filename) == 0:  # 如果文件为空，则写入标题行
                    writer.writerow(['Airline', 'Departure Airport', 'Arrival Airport', 'Departure Time', 'Arrival Time', 'Flight Information', 'Price'])
        print("there's no data")
        return


def main(departure_city, arrival_city, departure_date):
    filename = f"flights_{departure_city}_{arrival_city}_{departure_date}.csv"
    # 检查文件是否已经存在，如果不存在则提交任务
    if not os.path.isfile(filename):
        print(f"Querying flights from {departure_city} to {arrival_city} on {departure_date}...")
        query_flights_route(departure_city, arrival_city, departure_date,filename)
    else:
        print(f"File '{filename}' already exists. Skipping query for {departure_city} to {arrival_city}.")


url_list = read_file_to_list('71-90.txt')
route_pattern = re.compile(r'/oneway-(\w{3})-(\w{3})')
date_pattern = re.compile(r'depdate=(\d{4}-\d{2}-\d{2})')      

for url in url_list:
    # 解析URL
    parsed_url = urlparse(url)

    # 使用正则表达式匹配出发地、到达地
    route_match = route_pattern.search(parsed_url.path)
    if route_match:
        print(f"Route match: {route_match.group(0)}")
    else:
        print("No route match found.")
        continue  # 如果没有找到路线匹配，跳过这个URL

    # 使用正则表达式匹配日期
    date_match = date_pattern.search(parsed_url.query)

    # 如果找到日期匹配，处理它
    if date_match:
        departureDate = date_match.group(1)
        print(f"Date match: {departureDate}")
    else:
        print("No date match found. URL may be incorrectly formatted or missing the 'depdate' query parameter.")
        # 打印原始URL以帮助调试
        print(f"URL checked: {url}")
        continue  # 如果没有找到日期匹配，跳过这个URL

    # 从route_match中提取出发地和目的地
    departurePlace = route_match.group(1)
    arrivePlace = route_match.group(2)

    # 现在可以安全地调用main函数
    main(departurePlace, arrivePlace, departureDate)
 

# departure_cities = ['bjs', 'can']  # 示例出发城市列表
# arrival_cities = ['bjs', 'can']    # 示例到达城市列表
# departure_dates = ['2024-8-20']    # 示例出发日期列表
# main(departure_cities, arrival_cities, departure_dates)