# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import codecs
import os

class MM:
	def __init__(self):
		self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
		self.user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
		self.headers = {"User-Agent":self.user_agent}
	#获取索引页的内容
	def getOnePage(self, pageIndex):
		url = self.siteURL + "?page=" + str(pageIndex)
		request = urllib2.Request(url, headers = self.headers)
		response = urllib2.urlopen(request)
		content = response.read().decode("gbk")
		return content
	#获取页面的信息
	def getPageInfo(self, pageIndex):
		page = self.getOnePage(pageIndex)
		if not page:
			print "page open fail!"
			return None
		else:
			print "page:", pageIndex
		pattern = re.compile('<.*?class="lady-avatar">.*?<img src="(.*?)".*?<a class="lady-name" href="(.*?)".*?>(.*?)</a>.*?<em>.*?<strong>(\d*)</strong>.*?<span>(.*?)</span>'+
			'.*?</p>.*?<p>.*?<em>(.*?)</em>.*?<div class="pic w610">.*?<a href="(.*?)"', re.S)
		items = re.findall(pattern, page)
		return items
	#保存个人信息
	def saveInfo(self, tab, name):
		fileName = name+"/"+name+".txt"
		fp = codecs.open(fileName, "w", "utf-8")
		fp.write((tab[2]+"\r\n"))
		fp.write((tab[3]+"\r\n"))
		fp.write((tab[4]+"\r\n"))
		fp.write((tab[5]+"\r\n"))
		fp.close()
	def makeDir(self, path):
		path = path.strip()
		isExist = os.path.exists(path)
		if not isExist:
			os.mkdir(path)
	def getImages(self, url):
		url = "http:"+url
		response = urllib2.urlopen(url)
		content = response.read()
		pattern = re.compile(':&quot;//(.*?).jpg', re.S)
		items = re.findall(pattern, content)
		return items

	def saveImage(self, url, name, index):
		imgurl = "http://"+url+".jpg"
		fileName = name+"/"+name+str(index)+'.jpg'
		u = urllib.urlopen(imgurl)
		data = u.read()
		fp = open(fileName, "wb")
		fp.write(data)
		fp.close()
	#开始获取 #item[0]:icon item[1]:个人主页 item[2]:名字 item[3]:年龄 item[4]:城市 item[5]:职业 item[6]:图册
	def start(self):
		for pageIndex in range(1, 3):
			items = self.getPageInfo(pageIndex)
			for item in items:
				self.makeDir(item[2])
				self.saveInfo(item, item[2])
				imgs = self.getImages(item[6])
				index = 1
				for imgurl in imgs:
					self.saveImage(imgurl, item[2], index)
					index += 1

instance = MM()
instance.start()
