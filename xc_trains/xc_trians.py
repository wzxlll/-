import csv
import os
from bs4 import BeautifulSoup
from DrissionPage import ChromiumOptions, ChromiumPage

def read_file_to_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # 使用列表推导式读取每一行
        url_list = [line.strip() for line in file]
    return url_list

# get_page 负责获取指定url的page对象 并返回一个可操作的page对象
def get_page(url):
    do1 = ChromiumOptions().set_paths(local_port=9112, user_data_path=r'D:\data2')
    page = ChromiumPage(addr_or_opts=do1)
    page.get(url)  # 使用传入的URL
    return page

def extract_data(html_element):
    # 核心字段提取
    card = {
        "车次号": html_element.find("div", class_="checi").get_text(strip=True),
        "出发时间": html_element.find("div", class_="from").find("div", class_="time").text.strip(),
        "到达时间": html_element.find("div", class_="to").find("div", class_="time").text.strip(),
        "出发地点": html_element.find("div", class_="from").find("div", class_="station").text.strip(),
        "到达地点": html_element.find("div", class_="to").find("div", class_="station").text.strip(),
        "运行时间": html_element.find("div", class_="haoshi").text.strip(),
        "价格": html_element.find("div", class_="price").text.strip() + "元"  # 添加货币单位
    }
    
    # 处理可能存在的空值
    if not card["价格"].replace("元", "").replace(".", "").isdigit():
        card["价格"] = "暂无报价"
    
    return card

def get_data(page, url):
    soup = BeautifulSoup(page.html, "html.parser")
    trains_raw = soup.find_all('div', class_='card-white list-item')
    print(f"从URL {url} 中找到 {len(trains_raw)} 条列车信息")
    trains = []
    for div in trains_raw:
        if not div.find_parent('div', class_='transfer-box'):
            trains.append(div)
    
    # 检查文件是否存在，如果不存在则写入表头
    file_exists = os.path.isfile("train_details.csv")
    
    # 以追加模式打开文件
    with open("train_details.csv", "a", newline="", encoding="utf-8-sig") as csvfile:
        columns = ["车次号", "出发时间", "到达时间", "出发地点", "到达地点", "运行时间", "价格"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        
        # 如果文件不存在，写入表头
        if not file_exists:
            writer.writeheader()
        
        # 写入数据
        for div in trains:
            data = extract_data(div)
            writer.writerow(data)  # 使用 writerow 追加数据

    print(f"数据已追加到 train_details.csv")

def __main__():
    # 读取URL列表
    url_list = read_file_to_list("urls.txt")  # 假设URL列表保存在 urls.txt 文件中
    
    for url in url_list:
        page = get_page(url)
        get_data(page, url)

__main__()