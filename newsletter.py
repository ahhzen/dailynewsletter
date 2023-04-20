import smtplib
import credential
from datetime import datetime
from email.message import EmailMessage
from string import Template
from pathlib import Path
import os

# path_item = [Path().home(), "Documents", "Python Projects", "Project_Webscrapper", "news_template.html"]
path_item = [Path().home(), "project", "dailynewsletter", "news_template.html"]
# path_item = [Path().home(), "project", "scrapper", "news_template.html"]

li = "<li><h3>LISTITEM</h3></li>"
def populate_template(news_data):
	todaynow = datetime.now().strftime("%d/%m/%Y %X")
	section = ""
	news_li_html = ""
	for item in news_data:
		if section != item.get("section"):
			section = item.get("section")
			section_item = f"<h2> {section} </h2>"
			news_li_html += section_item

		news_img = item.get("img", "")
		img_tag = ""
		if len(news_img) > 0: 
			img_tag = f"<img src='{news_img}'>"

		news_url = item.get("url")
		news_title = item.get("title")
		news_item = f"<a href='{news_url}'>{img_tag} {news_title} </a>"

		# listitem = li.replace("IMG", img_tag)
		listitem = li.replace("LISTITEM", news_item)

		news_li_html += listitem

	news_detail = {"datetime": todaynow, "news_list": news_li_html}

	# news_template = Template(Path("news_template.html").read_text())
	path_template = ""
	for item in path_item:
		path_template = Path(path_template, item)
	print(f"Opening template file : {path_template}")
	news_template = Template(path_template.read_text())
	news_template = news_template.substitute(news_detail)
	return news_template

def send_email(news_data):

	email = EmailMessage()
	email["from"] = "PiZen"
	email["to"] = os.getenv("MAIL_LIST").split(":")	
	email["subject"] = "News Around the World NOW!"

	news_template = populate_template(news_data)
	email.set_content(news_template,"HTML")

	with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
	    smtp.ehlo()
	    smtp.starttls()
	    smtp.login(credential.username, credential.password)
	    smtp.send_message(email)
	    print("Daily News Letter is Sent")
