import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint
import newsletter 
import os

PROJECT_NAME = "dailynewsletter"
SOURCE_FILENAME = "googlenews.txt"
MAX_PER_SECTION = 8
google_news_prefix = "https://news.google.com"

# class_link = ".DY5T1d"	#19042023 ZEN
class_link = ".XlKvRb"

# class_ts = ".WW6dff.uQIVzc.Sksgp"
class_ts = ".hvbAAd"

# class_src = ".wEwyrc.AVN2gc.uQIVzc.Sksgp"

# class_hl = ".xrnccd.F6Welf.R7GTQ.keNKEd.j7vNaf" #19042023 ZEN
class_hl = ".PO9Zff.Ccj79.kUVvS"

# class_img = ".tvs3Id.QwxBBf" #19042023 ZEN
class_img = ".K0q4G.P22Vib"

class_title = ".gPFEn"	#added by MBP-Zen

masterlist = []

def read_news_source(filename="googlenews.txt"):
	fullpath = os.path.join(os.path.expanduser("~"), "project", "dailynewsletter", filename)
	print("Opening file : ", fullpath)

	source = ""
	with open(fullpath, "r") as file1:
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
			# news_src = headline.select(class_src)[0]

			#News Link contains URL & Title
			news_link = headline.select(class_link)[0]	#class_link - done

			#News Timestamp
			news_ts = headline.select(class_ts)[0]	#class_ts - done (TIMESTAMP)

			img_src = ""
			news_img = headline.select(class_img)	#class_img - done
			if len(news_img) > 0:
				news_img = news_img[0]
				img_src = news_img.find('img').get('src')
				# img_src = news_img.get("src", "")
			else:
				img_src = ""

			url_part = news_link.find('a').get('href').lstrip(".")
			googlenews_link = google_news_prefix + url_part
			# googlenews_link = google_news_prefix + news_link.get("href","").lstrip(".")
		    
			news_time = news_ts.get("datetime", 0) if news_ts != None else news_ts
			dt = datetime.fromisoformat(news_time.rstrip("Z"))
			dt = dt.strftime("%d/%m/%Y %X")

			# news_title = news_link.find('a').get('aria-label')	#-deleted by MBP-Zen
			news_title = headline.select(class_title)[0].text		#+added by MBP-Zen
		
			# news.update({"section": section, "title": news_link.text, "url": googlenews_link, "img": img_src, "timestamp": dt})
			news.update({"section": section, "title": news_title, "url": googlenews_link, "img": img_src, "timestamp": dt})
			# print(news)
			news_list.append(news.copy())
		except IndexError:
			continue

	return news_list

def display_new():
	allnews = get_news()
	
	for num, news in enumerate(allnews):
		print(num, end="")
		pprint(news)
		print()

def generate_newsletter():
	allnews = get_news()
	newsletter.send_email(allnews)

if __name__ == "__main__":
	generate_newsletter()


