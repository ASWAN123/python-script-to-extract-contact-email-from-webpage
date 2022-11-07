import grequests
from bs4 import BeautifulSoup
import csv 
import re 
from tldextract import extract
from tinydb import TinyDB, Query
db = TinyDB('db.json')


reobj = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}\b",re.IGNORECASE)
with open ('urls.txt' , "r" , encoding="utf8") as myfile:
    data1 = myfile.read().splitlines()
    recipient_lst = [string for string in data1 if string != ""]
    data = sorted(set(recipient_lst))

key = 0 # in case the code stop change with number in the output
workers = 100  # how many url to scrape per single run

for i in range(key , len(data[key:len(data)]) , workers ) :
	chunk = data[key:key + workers]
	res = (grequests.get(u , stream=True , timeout = 10) for u in chunk)
	y  = grequests.map(res)
	print(key+workers)
	for content in y :
		target = []
		try:
			link = content.url
			soup = BeautifulSoup(content.text , 'html.parser')
			urls = soup.find_all('a' ,href=True)
			for  each  in urls :
				if  'mailto:' in each['href']:
					content_mail = each['href']
					email = re.findall(reobj, str(content_mail))
					target = email
					if len(target) > 0:
						db.insert({ 'url': link , 'contact_email':target })

		except:pass

print('all data has been extracted')
