# departurePlace = {'bjs','sha','tsn','ckg','sjw','shp','shf','tyn','dat','cih','het','bav','xil','hlh','hld','wua','cif','tgo','nzh','hrb','ndg','mdg','jmu','hek','cgq','jil','ynj','she','dlc','ddg','iob','jng','chg','nkg','lyg','ntg','czx','xuz','ynz','wux','foc','xmn','wus','jjn','kow','hgh','wnz','ngb','yiw','hsn','juz','hyn','khn','jdz','jiu','jgs','tna','weh','tao','ynt','jng','wef','doy','lyi','hfe','txn','fug','aqg','cgo','nny','lya','ayn','csx','dyg','cgd','hny','hjj','llf','dax','wuh','yih','xfn','shs','enh','can','zuh','szx','swa','mxz','zha','shg','xin','nng','kwl','lzh','wuz','bhy','hak','syx','ctu','lzo','ybp','mig','jzh','pzi','dax','wxn','xic','nao','gys','kwe','zyi','ava','ten','kmg','ljg','jhg','dlu','sym','bsd','lnj','zat','yua','lum','dig','lxa','bpx','acx','urc','khg','yin','krl','aku','htn','aat','hmi','kry','fyn','tcg','kca','iqm','sia','eny','aka','uyn','hzg','dnh','jgn','chw','iqn','lhw','xnn','goq','inc','hkg','mfm'}
# arrivePlace = {'bjs','sha','tsn','ckg','sjw','shp','shf','tyn','dat','cih','het','bav','xil','hlh','hld','wua','cif','tgo','nzh','hrb','ndg','mdg','jmu','hek','cgq','jil','ynj','she','dlc','ddg','iob','jng','chg','nkg','lyg','ntg','czx','xuz','ynz','wux','foc','xmn','wus','jjn','kow','hgh','wnz','ngb','yiw','hsn','juz','hyn','khn','jdz','jiu','jgs','tna','weh','tao','ynt','jng','wef','doy','lyi','hfe','txn','fug','aqg','cgo','nny','lya','ayn','csx','dyg','cgd','hny','hjj','llf','dax','wuh','yih','xfn','shs','enh','can','zuh','szx','swa','mxz','zha','shg','xin','nng','kwl','lzh','wuz','bhy','hak','syx','ctu','lzo','ybp','mig','jzh','pzi','dax','wxn','xic','nao','gys','kwe','zyi','ava','ten','kmg','ljg','jhg','dlu','sym','bsd','lnj','zat','yua','lum','dig','lxa','bpx','acx','urc','khg','yin','krl','aku','htn','aat','hmi','kry','fyn','tcg','kca','iqm','sia','eny','aka','uyn','hzg','dnh','jgn','chw','iqn','lhw','xnn','goq','inc','hkg','mfm'}
# departureDate = {}

# 'https://flights.ctrip.com/online/list/oneway-' + departurePlace + '-' + arrivePlace + '?depdate='+ departureDate + '&cabin=y_s_c_f&adult=1&child=0&infant=0'

# 导入所需模块
import itertools

departurePlace = {'bjs','sha','tsn','ckg','sjw','shp','shf','tyn','dat','cih','het','bav','xil','hlh','hld','wua','cif','tgo','nzh','hrb','ndg','mdg','jmu','hek','cgq','jil','ynj','she','dlc','ddg','iob','jng','chg','nkg','lyg','ntg','czx','xuz','ynz','wux','foc','xmn','wus','jjn','kow','hgh','wnz','ngb','yiw','hsn','juz','hyn','khn','jdz','jiu','jgs','tna','weh','tao','ynt','jng','wef','doy','lyi','hfe','txn','fug','aqg','cgo','nny','lya','ayn','csx','dyg','cgd','hny','hjj','llf','dax','wuh','yih','xfn','shs','enh','can','zuh','szx','swa','mxz','zha','shg','xin','nng','kwl','lzh','wuz','bhy','hak','syx','ctu','lzo','ybp','mig','jzh','pzi','dax','wxn','xic','nao','gys','kwe','zyi','ava','ten','kmg','ljg','jhg','dlu','sym','bsd','lnj','zat','yua','lum','dig','lxa','bpx','acx','urc','khg','yin','krl','aku','htn','aat','hmi','kry','fyn','tcg','kca','iqm','sia','eny','aka','uyn','hzg','dnh','jgn','chw','iqn','lhw','xnn','goq','inc','hkg','mfm'}
arrivePlace = {'bjs','sha','tsn','ckg','sjw','shp','shf','tyn','dat','cih','het','bav','xil','hlh','hld','wua','cif','tgo','nzh','hrb','ndg','mdg','jmu','hek','cgq','jil','ynj','she','dlc','ddg','iob','jng','chg','nkg','lyg','ntg','czx','xuz','ynz','wux','foc','xmn','wus','jjn','kow','hgh','wnz','ngb','yiw','hsn','juz','hyn','khn','jdz','jiu','jgs','tna','weh','tao','ynt','jng','wef','doy','lyi','hfe','txn','fug','aqg','cgo','nny','lya','ayn','csx','dyg','cgd','hny','hjj','llf','dax','wuh','yih','xfn','shs','enh','can','zuh','szx','swa','mxz','zha','shg','xin','nng','kwl','lzh','wuz','bhy','hak','syx','ctu','lzo','ybp','mig','jzh','pzi','dax','wxn','xic','nao','gys','kwe','zyi','ava','ten','kmg','ljg','jhg','dlu','sym','bsd','lnj','zat','yua','lum','dig','lxa','bpx','acx','urc','khg','yin','krl','aku','htn','aat','hmi','kry','fyn','tcg','kca','iqm','sia','eny','aka','uyn','hzg','dnh','jgn','chw','iqn','lhw','xnn','goq','inc','hkg','mfm'}
departureDates = {'2025-01-01','2025-01-02','2025-01-03','2025-01-04','2025-01-05','2025-01-06','2025-01-07','2025-01-08','2025-01-09','2025-01-010','2025-01-11','2025-01-12','2025-01-13','2025-01-14','2025-01-15','2025-01-16','2025-01-17','2025-01-18','2025-01-19','2025-01-20','2025-01-21','2025-01-22','2025-01-23','2025-01-24','2025-01-25','2025-01-26','2025-01-27','2025-01-28','2025-01-29','2025-01-30','2025-01-31'}

# 基础URL
base_url = 'https://flights.ctrip.com/online/list/oneway-'

# 生成所有可能的城市对
city_pairs = list(itertools.product(departurePlace, arrivePlace))
# 过滤掉出发地和目的地相同的情况
filtered_pairs = [pair for pair in city_pairs if pair[0] != pair[1]]

# 为每个城市对和每个出发日期生成URL
urls = []
for dep, arr in filtered_pairs:
    for date in departureDates:
        url = f"{base_url}{dep}-{arr}?depdate={date}&cabin=y_s_c_f&adult=1&child=0&infant=0"
        urls.append(url)

# 指定文件份数，这里直接设置为一个示例值
num_files = 300  # 示例文件份数

# 计算每份文件应有的URL数量
urls_per_file = len(urls) // num_files
remaining_urls = len(urls) % num_files

# 将URL列表写入文件
def write_urls_to_files(urls, num_files, urls_per_file, remaining_urls):
    for i in range(num_files):
        # 计算每份文件的起始和结束索引
        start_index = i * urls_per_file
        if i < remaining_urls:
            end_index = start_index + urls_per_file + 1
        else:
            end_index = start_index + urls_per_file
        
        filename = f'xc_{i+1}.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            for url in urls[start_index:end_index]:
                file.write(url + '\n')
        print(f"文件 '{filename}' 已写入完成，包含 {end_index - start_index} 个URL。")

# 写入文件
write_urls_to_files(urls, num_files, urls_per_file, remaining_urls)