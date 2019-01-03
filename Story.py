import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import os, sys
import time

##################
#判断URL能否打开
##################
def get_one_page(url):
	try:
		response=requests.get(url)
		if response.status_code==200:
			return response.text
		return None
	except RequestException:
		return None
		
#######################
#解析单个网页s
#######################
def parse_one_page(html):
	doc = pq(html)
	title=doc('.articleTitle h2')
	write_to_file_list('\n\n\n\n\n')
	write_to_file_list(title.text())
	article=doc('.articleCon p')
	write_to_file_list('\n\n')
	write_to_file_list(article.text())
	
########################
#Str方式保存文本内容
########################
def write_to_file_list(content):
	with open('story_tmp.txt','a',encoding='utf-8') as f:
		f.write(content)
		f.close()

##############################
#获取单个网页的HTML
##############################
def web_pages_url(offset):
	url='https://www.huaxiangju.com'+str(offset)
	get_one_page(url)
	html=pq(url,encoding='gbk')
	parse_one_page(html)

##############################
#获取单个故事的名字和章节URL
##############################
def one_story(url):
	story = pq(url,encoding='gbk')
	per=story('.chapterCon ul li a').items()
	f = open("story_url_tmp.txt","w")
	for i in per:
		offset=i.attr('href')
		f.write(offset+'\n')
	f.close()
	print('单个故事的章节URL保存成功')
	f = open("story_url_tmp.txt","r")
	get = f.read()
	result = get.split('\n')
	for i in range(0, result.__len__())[::-1]:
		if len(result[i]):
			print('正在解析网页：'+result[i])
			web_pages_url(result[i])
	f.close()
	s_name=story('.bookPhr h2')
	rename_file(s_name.text())
	os.remove('story_url_tmp.txt')
	time.sleep(600)
	

##############################
#修改文件名字
##############################
def rename_file(story_name):
	newname=story_name+'.txt'
	os.rename('story_tmp.txt',newname)
	print(newname+' download successfully')
	


##############################
#保存所有故事的主URL
##############################
def read_story_url():
	f = open("all_url_tmp.txt","r")
	get = f.read()
	result = get.split('\n')
	for i in range(0, result.__len__()):
		if len(result[i]):
			one_story(result[i])
	f.close()
	os.remove('all_url_tmp.txt')


##############################
#保存所有故事的主URL
##############################
def main(offset):
	url='https://www.huaxiangju.com/all/0_allvisit_0_0_0_0_2_0_'+str(offset)+'.html'
	index_url = pq(url,encoding='gbk')
	storys_url=index_url('.listRightBottom ul li h2 a').items()
	f = open("all_url_tmp.txt","a+")
	for i in storys_url:
		one_story=i.attr('href')
		f.write(one_story+'\n')
	f.close()
	
	

##############################
#主函数施加偏移范围
##############################
if __name__=='__main__':
	for i in range(100):
		main(i+1)
	print('所有故事的URL保存成功')
	read_story_url()
