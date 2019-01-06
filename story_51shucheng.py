import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import os, sys
import time
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9',
	'Connection':'close'
	}
	
def check_url(url):
	response = requests.get(url=url,headers=headers)
	response.encoding='UTF-8'
	if response.status_code!=404:
		while response.status_code!=200:
				print('暂停抓取文字一分钟')
				print('【'+url+'】')
				time.sleep(60)
				response=requests.get(url,headers=headers)
		return response.text
	else:
		print('无法打开该链接：'+url)
		return 0

def story_url():
	url='http://www.51shucheng.net/zuojia'
	doc=check_url(url)
	html=pq(doc)
	auth_list=html('.mulu-list ul li a').items()
	for i in auth_list:
		auth_one=i.attr('href')
		doc=check_url(auth_one)
		html=pq(doc)
		story_list=html('td h2 a').items()
		for i in story_list:
			story_one=i.attr('href')
			doc=check_url(story_one)
			html=pq(doc)
			juan_list=html('.mulu-title h2').items()
			for i in juan_list:
				story_name=i.text()
				print(i.text())
				chap_list=html('.mulu-list ul li a').items()
				for i in chap_list:
					chap_one=i.attr('href')
					doc=check_url(chap_one)
					html=pq(doc)
					h1_name=html('h1')
					chap_title=(h1_name.text())
					write_to_file_list('\n\n\n【'+chap_title+'】\n\n\n',story_name)
					neirong=html('.neirong p').items()
					for i in neirong:
						write_to_file_list('    '+i.text()+'\n\n',story_name)



	
	

def write_to_file_list(content,story_name):
	with open(story_name+'.txt','a',encoding='utf-8') as f:
		f.write(content)
		f.close()

		
		


if __name__=='__main__':
	story_url()




























