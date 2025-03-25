import ast
from itertools import permutations

def generate_urls():
    # 读取城市列表
    with open('cities.txt', 'r', encoding='utf-8') as f:
        cities_content = f.read().strip()
    cities = ast.literal_eval(cities_content)
    
    # 获取用户输入的日期
    d_date = input("请输入出发日期（格式为YYYY-MM-DD，例如2025-04-22）：")
    
    # 生成所有可能的起止城市组合
    city_pairs = permutations(cities, 2)
    
    # 生成URL列表
    urls = [
        f"https://trains.ctrip.com/webapp/train/list?ticketType=0&dStation={d_city}&aStation={a_city}&dDate={d_date}"
        for d_city, a_city in city_pairs
    ]
    
    # 将URL写入文件
    with open('urls.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(urls))
    
    print(f"已生成{len(urls)}条URL，保存到urls.txt")

if __name__ == "__main__":
    generate_urls()