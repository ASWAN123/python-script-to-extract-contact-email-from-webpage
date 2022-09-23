from concurrent.futures.thread import ThreadPoolExecutor
from  concurrent.futures import  as_completed
import  requests 
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


import random
import time 


def scraper(url):
	timee  = [ 1, 2, 4 ,5 ]
	time.sleep(random.choice(timee))
	try:
		target = []
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
		res = requests.get(url , headers = headers , stream=True , timeout = 10)
		status = res.status_code
		if  status == 200 :
			soup = BeautifulSoup(res.text , 'html.parser')
			Urls = soup.find_all('a' ,href=True)
			for  each  in Urls :
				if  'mailto:' in each['href']:
					content_mail = each['href']
					email = re.findall(reobj, str(content_mail))
					target = email
					
		if len(target) == 0 :
			emails = re.findall(reobj, res.text)
			mylist = sorted(set(emails))
			if len(mylist) == 0:
				pass
			else:
				em = []
				for  each  in mylist :
					tsd, td, tsu = extract(url)
					url1 = td + '.' + tsu
					valid = [".com", ".net", ".org", ".co", ".us", ".xyz", ".online", ".top", ".site", ".shop", ".club", ".vip", ".app", ".store", ".live", ".de", ".cn", ".uk", ".ca", ".nl", ".ru", ".br", ".fr", ".eu", ".it", ".au"]
					if url1.split('.')[0].lower() in each.lower() or any(ext in each.lower() for ext in valid ) :
						em.append(each)
				return url , em

		else:
			return url , target
	except:
		return 


key = 0
workers = 10
futures = []

with ThreadPoolExecutor( max_workers=  workers ) as executor:
    urls = data[key:]
    for  url  in  urls :
    	future= executor.submit(scraper , url )
    	futures.append(future)
    	if len(futures) == workers :
    		for future in as_completed(futures):
    			if  future.result() != None :
    				db.insert({'url':future.result()[0], 'contact_email':future.result()[1] })
    		key += workers
    		print(key)
    		futures = []



    	






