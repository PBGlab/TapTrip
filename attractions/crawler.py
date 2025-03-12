from bs4 import BeautifulSoup
import requests
import json
from collections import defaultdict


# 目標網站:台灣觀光局
url = "https://www.taiwan.net.tw/"
headers = {"User-Agent": "Mozilla/5.0"}
# 資料容器
data = {}
# 儲存基本資料
cities = []  # 各縣市
attractionsNames = []  # 景點名稱
attractionsLinks = []  # 景點連結
imageLinks = []  # 景點圖片連結
hashtagg = []  # 景點介紹
googlemaplinks = [] # 景點GOOGLE MAP
locations = [] # 景點經緯度

for i in range(4):
    URL = url+"m1.aspx?sNo=000050"+str(i+1)
    r = requests.get(URL,headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.select("ul.grid.circularbtn-list a")
    for title in titles:
        cityName = title.get("title").strip()
        cities.append(cityName)
        print("city: "+ cityName)
        print("="*100)
        if cityName not in data:
            data[cityName] = []
        URL = "https://www.taiwan.net.tw/"+title.get("href")
        r = requests.get(URL,headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        names = soup.select("div.card-wrap")
        hashtags = soup.select("div.hashtag")
        for name,hashtag in zip(names,hashtags):
            links = name.find_all("a",href=True)
            hashtagg.append(hashtag.text)
            if len(links) > 1:
                URL = "https://www.taiwan.net.tw/"+links[0].get("href")
                attractionsLinks.append(URL)
                attractionsNames.append(links[0].get("title").strip())
                r = requests.get(URL,headers=headers)
                soup = BeautifulSoup(r.text, "html.parser")
                address = soup.select_one("dl.info-table dd a.tel-link.address")
                image = soup.select_one("ul.album li img")
                try:
                    img_src = image.get("data-src", image.get("src"))
                except:
                    img_src = "https://www.taiwan.net.tw/images/noPic.jpg"
                imageLinks.append(img_src)
                ad = address.get("href")
                googlemaplinks.append(ad)
                locations.append(ad[46:-18])
                data[cityName].append({
                    "name": links[0].get("title").strip(),
                    "link": URL,
                    "image": img_src,
                    "hashtag": hashtag.text,
                    "googlemap": ad,
                    "location": ad[46:-18] })

                print("name: "+ links[0].get("title").strip())
                print("link: "+ URL)
                print("image: "+ img_src)
                print("hashtag: "+ hashtag.text)
                print("googlemap: "+ ad)
                print("location: "+ ad[46:-18])
                print("-" * 110)

print(len(attractionsNames))
print(len(attractionsLinks))
print(len(imageLinks))
print(len(hashtagg))
print(len(googlemaplinks))
print(len(locations))

# 存成 JSON 檔案
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("爬取完成！資料已儲存到 data.json")