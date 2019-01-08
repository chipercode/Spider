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
	
def check_url(urls):
	url=urls	
	try:
		response = requests.get(url=url,headers=headers)
		response.encoding='gbk'
		return response.text
	except requests.exceptions.RequestException as e:
		print('重试打开链接：'+url)
		return check_url(url)
##############################
#修改文件名字
##############################
def rename_file(story_name):
	newname=story_name+'.txt'
	os.rename('story_tmp.txt',newname)
	print(newname+' download successfully')		
		
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
	doc=check_url(url)
	if doc:
		html=pq(doc)
		title=html('.articleTitle h2')
		write_to_file_list('\n\n\n\n\n')
		write_to_file_list('【'+title.text()+'】')
		article=html('.articleCon p')
		write_to_file_list('\n\n')
		write_to_file_list(article.text())
	else:
		print('无法打开链接，故事章节抓取失败')
		
		
##################
#下载封面图片
##################
def get_img(url):
	doc=check_url(url)
	if doc:
		img=pq(doc)		#指定编码要在解析的时候加入
		img_tag=img('.bookImg img')
		print(img_tag)
		img_src=img_tag.attr('src')
		img_title=img_tag.attr('alt')
		img_url=('https://www.huaxiangju.com'+img_src)
		img_content=requests.get(img_url,headers=headers)
		with open(img_title+'.jpg','wb') as f:
			f.write(img_content.content)		#写入二进制文件要加'.content'
			f.close()
		print('故事封面抓取成功')
	else:
		print('无法打开链接，封面图片抓取失败')	
	
##############################
#获取单个故事的名字和章节URL
##############################
def one_story(url):
	doc=check_url(url)
	if doc:
		story = pq(doc)
		per=story('.chapterCon ul li a').items()
		f = open("story_url_tmp.txt","w")
		for i in per:
			offset=i.attr('href')
			f.write('\n'+offset)		#倒序之后因第一个换行符产生的空行被放在在末尾
		f.close()
		print('单个故事的章节URL保存成功')
		f = open("story_url_tmp.txt","r")
		get = f.read()
		result = get.split('\n')
		for i in range(-1,-len(result),-1):
			#print('正在解析网页：'+result[i])
			web_pages_url(result[i])
			#print('解析完成')		#貌似可以修复文件IO错误。不能！
		f.close()
		s_name=story('.bookPhr h2')
		rename_file(s_name.text())
		os.remove('story_url_tmp.txt')
	else:
		print('无法打开该链接，小说故事抓取失败')
	
##############################
#读取所有故事的主URL
##############################
def read_story_url():
	f = open("all_url_tmp.txt","r")
	get = f.read()
	result = get.split('\n')
	for i in range(0, len(result)-1,1):
		get_img(result[i])
		one_story(result[i])
		#print('sleep 10 minutes')
		#time.sleep(700)
	f.close()
	os.remove('all_url_tmp.txt')	
	
	
##############################
#保存所有故事的主URL
##############################
def main(offset):
	url='https://www.huaxiangju.com/all/0_allvisit_0_0_0_0_2_0_'+str(offset)+'.html'
	doc=check_url(url)
	if doc:
		html = pq(doc)
		storys_url=html('.listRightBottom ul li h2 a').items()
		f = open("all_url_tmp.txt","a+")
		for i in storys_url:
			one_story=i.attr('href')
			f.write(one_story+'\n')
					
		f.close()
	else:
		print('所有小说的索引抓取失败')
	
	
	
##############################
#主函数
##############################
if __name__=='__main__':
	for i in range(1,700,1):
		main(i)
	print('所有故事的URL保存成功')
	#time.sleep(610)
	read_story_url()
