import urllib.request
from lxml import html
import re
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import urljoin
import os, sys
from bs4 import BeautifulSoup
import requests
from PIL import Image
	
def parse(url):
	req = urllib.request.Request(url)
	resp = urllib.request.urlopen(req)
	page = urlopen(url)
	charset = resp.headers.get_content_charset()
	soup = BeautifulSoup(page, 'html.parser')
	print(charset)
	respData = resp.read().decode()
	pattern = re.compile(r'<title.*>\s*(?P<title>.*?)\s*</title>', re.I|re.M)
	title = pattern.search(respData).group('title').strip()
	name = title + ".txt"
	print(name)
	select = soup.findAll(["p", "h1", "h2"])
	f = open(name, 'tw', encoding='utf-8')
	for temp in select:
		f.write(temp.get_text())
		f.write('\n')
	f.close()
	
	t = 1
	counter = 0
	f = urllib.request.urlopen(url)
	soup = BeautifulSoup(f, 'html.parser')
	for i in soup.findAll('img', attrs={'src': re.compile('(?i)(jpg|png)$')}):
		if(counter < 20):
			full_url = urljoin(url, i['src'])
			print("image URL: " + full_url)
			y = urllib.request.urlopen(full_url)
			t=t+1
			with open('downloaded_images/'+str(t)+'.png' , "wb") as code:
				code.write(y.read())
			counter+=1
			
	print('finished')
	return 0;

print('Введите путь')
url = input()
parse(url)
response = requests.get(url)  
html = html.fromstring(response.text)
f = open('links.txt', 'w')
i = 0
for a in html.iter("a"):
	if(i < 10):
		link = urljoin(url, a.get("href"))
		print(link)
		parse(link)
		f.write(link)
		f.write('\n')
		i += 1

		
f.close()		
input()
