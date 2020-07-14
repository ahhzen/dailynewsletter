import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint
import newsletter 

MAX_PER_SECTION = 8
google_news_prefix = "https://news.google.com"
class_link = ".DY5T1d"
class_ts = ".WW6dff.uQIVzc.Sksgp"
class_src = ".wEwyrc.AVN2gc.uQIVzc.Sksgp"
class_hl = ".xrnccd.F6Welf.R7GTQ.keNKEd.j7vNaf"
class_img = ".tvs3Id.QwxBBf"
masterlist = []

def read_news_source(filename="./googlenews.txt"):
    source = ""
    with open(filename, "r") as file1:
        lines = file1.readlines()
        for line in lines:
            source += line

        file1.close()
    
    return json.loads(source).get("GoogleNews")

def get_news():
	news_sources = read_news_source()
	masterlist = []
	for src in news_sources:
		for section, url in src.items():	
			print(f"Read from {section} section")
			masterlist.extend(get_news_data(url, section, MAX_PER_SECTION))
	return masterlist

def get_news_data(url, section, maxhl=0):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
	headlines = soup.select(class_hl)
	news_list = []
	if maxhl <= 0:
		maxhl = len(headlines)

	for headline in headlines[:maxhl]:
		try:
			news = dict()
			news_src = headline.select(class_src)[0]
			news_ts = headline.select(class_ts)[0]
		    
			news_img = headline.select(class_img)
			if len(news_img) > 0:
			    news_img = news_img[0]
			    img_src = news_img.get("src", "")
			else:
				img_src = ""

			news_link = headline.select(class_link)[0]
		    
			googlenews_link = google_news_prefix + news_link.get("href","").lstrip(".")
		    
			news_time = news_ts.get("datetime", 0) if news_ts != None else news_ts
			dt = datetime.fromisoformat(news_time.rstrip("Z"))
			dt = dt.strftime("%d/%m/%Y %X")
		    
			news.update({"section": section, "title": news_link.text, "url": googlenews_link, "img": img_src, "timestamp": dt})
			news_list.append(news.copy())
		except IndexError:
			continue

	return news_list

def display_new():
	allnews = get_news()
	newsletter.send_email(allnews)
	
	# for num, news in enumerate(allnews):
	# 	print(num, end="")
	# 	pprint(news)
	# 	print()

if __name__ == "__main__":
	display_new()


