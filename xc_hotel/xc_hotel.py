import csv
import os
from bs4 import BeautifulSoup
from DrissionPage import ChromiumOptions, ChromiumPage
from time import sleep

hotel_name, address, score = [], [], []
room_name, room_price = [], []
room_info = []
    

def read_file_to_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # 使用列表推导式读取每一行
        url_list = [line.strip() for line in file]
    return url_list

# get_page 负责获取指定url的page对象 并返回一个可操作的page对象
def get_page(url):
    do1 = ChromiumOptions().set_paths(local_port=9112, user_data_path=r'D:\data2')
    page = ChromiumPage(addr_or_opts=do1)
    page.get(url) #              //*[@id="hotels-destination"]
    city_ele = page.s_ele('xpath://*[@id="hotels-destination"]')
    city = city_ele.attr('value')#//*[@id="ibu_hotel_container"]/div/section/div[2]/ul/li[5]/div/div[2]/div[2]/div[2]/div[2]/div/span
    date_ele = page.s_ele('xpath://*[@id="ibu_hotel_container"]/div/div[1]/ul/li[2]/div/div[1]/input')
    date = date_ele.attr('value')
    return page, city, date

# get_soup 负责获取指定page对象的soup return一个soup交由下一个函数处理
def get_soup(page):
    page.wait.new_tab()
    tab1 = page.latest_tab
    detailed_url = tab1.url
    with open('detailed_urls.txt', 'a', encoding='utf-8') as file:
        file.write(detailed_url + '\n')
    # tab1.scroll.down(500)
    sleep(1)
    tab1.scroll.down(500)
    # sleep(1)
    soup = BeautifulSoup(tab1.html, "html.parser")
    tab1.close()
    return soup

# get_whole_page 负责获取页面中可以点击的每一个酒店 限制在每个城市300个酒店
def get_whole_page(page, city, date):
    # sleep(4)
    page.scroll.down(845)
    for i in range(5,305):
        #                    //*[@id="ibu_hotel_container"]/div/section/div[2]/ul/div[2]/div/span
        if page.s_ele('xpath://*[@id="ibu_hotel_container"]/div/section/div[2]/ul/div[2]/div/span') == None:
            serach_more_ele = page.s_ele('xpath://*[@id="ibu_hotel_container"]/div/section/div[2]/ul/div[2]/div/span')
            page.actions.click(serach_more_ele)
        ele = page.ele(f'xpath://*[@id="ibu_hotel_container"]/div/section/div[2]/ul/li[{i}]/div/div[2]/div[2]/div[2]/div[2]/div/span')
        #                      //*[@id="ibu_hotel_container"]/div/section/div[2]/ul/li[5]/div/div[2]/div[2]/div[2]/div[2]/div/span
        page.actions.click(ele)
        # sleep(4)
        soup = get_soup(page)
        if i != 5:
            tab1 = page.latest_tab
            tab1.close()
        hotel_detailed_info(soup)
        page.scroll.down(265)
        # 检查文件是否存在，如果不存在则写入表头
        file_exists = os.path.isfile(f'{city}-{date}.csv')
        with open(f'{city}-{date}.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                # 写入表头
                writer.writerow(['酒店名称', '地址', '评分', '房型价格列表'])
            # 写入酒店信息
            writer.writerow([hotel_name[-1], address[-1], score[-1], room_info])




# hotel_detailed_info 负责获取每一个酒店的详细信息 包括：名称 地址 评分 房型：价格（作为列表存储）
def hotel_detailed_info(soup):
    hotel_name.append(soup.find('h1', class_='detail-headline_name').text)
    address.append(soup.find('span', class_='detail-headline_position_text').text)
    score.append(soup.find('b', class_='detail-headreview_score_value').text)
    soup =soup.find_all('div',class_="commonRoomCard__BpNjl")
    # print(len(soup))
    for room in soup:
        room_name = room.find('span', class_='commonRoomCard-title__iYBn2')
        # room_price_raw = room.find('div', class_='saleRoomItemBox-priceBox-displayPrice__gWiOr')
        room_price = room.select_one('.saleRoomItemBox-priceBox-displayPrice__gWiOr > span')
        if room_name and room_price:
            room_info.append(f"{room_name.text}:{room_price.text}")
    

# 主函数综合每一个函数进行运行
def main():
    url_list = read_file_to_list('input.txt')
    for url in url_list:
        page, city, date = get_page(url)
        get_whole_page(page, city, date)


if __name__ == '__main__':
    main()