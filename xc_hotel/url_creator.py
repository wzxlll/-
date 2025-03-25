from datetime import datetime, timedelta
from urllib.parse import quote

# 输入日期范围
start_date_str = input("请输入开始日期（格式：YYYY-MM-DD）：")
end_date_str = input("请输入结束日期（格式：YYYY-MM-DD）：")

start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

# 生成所有checkin日期
dates = []
current_date = start_date
while current_date <= end_date:
    dates.append(current_date)
    current_date += timedelta(days=1)

# 生成URL列表
urls = []
for city_id in range(1, 601):  # cityid 范围是 1-600
    for checkin_date in dates:
        checkout_date = checkin_date + timedelta(days=1)
        checkin_str = checkin_date.strftime("%Y/%m/%d")
        checkout_str = checkout_date.strftime("%Y/%m/%d")
        # 替换cityid和日期
        url = f"https://hotels.ctrip.com/hotels/list?countryId=1&city={city_id}&checkin={checkin_str}&checkout={checkout_str}&display={city_id}&domestic=1&"
        urls.append(url)

# 保存到文件
with open('生成的URL.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(urls))

print(f"已生成 {len(urls)} 条URL，保存至文件：urls.txt")