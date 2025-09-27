import requests
from bs4 import BeautifulSoup
import re
import json


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def downloadDoubanPicture(url, saveName):
    req = requests.get(url,headers=headers)
    finaPath = f"pic/douban/{saveName}"
    with open(f"./static/{finaPath}", "wb") as f:
        f.write(req.content)

class Douban():
    def _reqIndex(self):
        req = requests.get("https://movie.douban.com/", headers =headers)
        return BeautifulSoup(req.content.decode(), "html5lib")

    def __init__(self):
        pass
    #获取一周热门榜单
    def getRankWeek(self):
        content = self._reqIndex().select(".billboard-bd a")
        return map(lambda x: x.getText(), content)


    def getHoting(self):
        comli = self._reqIndex().select(".screening-bd .ui-slide-content .ui-slide-item")
        hotsList = []
        for li in comli:
            try:
                img = li.select_one("img")["src"]
                link = li.select_one("a")["href"]
                title = li["data-title"]
                rate = li["data-rate"]
#
                res = re.search("https?://movie.douban.com/subject/([0-9]{1,})",
                                link)
                id = res.groups()[0]

                img = downloadDoubanPicture(img,f"hoting/{id}.jpg")

                hotsList.append({
                    "img": img,
                    "link": link,
                    "title": title,
                    "rate": rate,
                    "id": id,
                })
            except:
                pass
        print(hotsList)
#
        return hotsList
#
    def getHotMovie(self):
        req = requests.get("https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0",headers=headers)
        #print(req.json())["subjects"]
        jsonData = json.loads(req.content)
#
#
        for index, item in enumerate(jsonData["subjects"]):
            img = downloadDoubanPicture(item["cover"], f"HotMovie/{item['id']}.jpg")
            jsonData["subjects"][index]["img"] = img
#
        return jsonData["subjects"]
#
#
    def getHotTV(self):
        req = requests.get("https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0",headers=headers)
    # print(req.json())["subjects"]
        jsonData = json.loads(req.content)

        for index, item in enumerate(jsonData["subjects"]):
            img = downloadDoubanPicture(item["cover"], f"HotTv/{item['id']}.jpg")
            jsonData["subjects"][index]["img"] = img
#
        return jsonData["subjects"]

def downloadDoubanPicture(url, saveName):
    req = requests.get(url,headers=headers)
    finaPath = f"pic/douban/{saveName}"
    with open(f"./static/{finaPath}", "wb") as f:
        f.write(req.content)
#
    return finaPath


douban = Douban()
# douban.getHoting()
import db

for movie in douban.getRankWeek():
    db.doubanDB.saveRankWeek(movie)

for movie in douban.getHoting():
    db.doubanDB.saveHoting(movie)

for movie in douban.getHotMovie():
    db.doubanDB.saveHotMovie(movie)

for movie in douban.getHotTV():
    db.doubanDB.saveHotTV(movie)
