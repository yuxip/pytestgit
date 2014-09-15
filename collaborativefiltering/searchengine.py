#!/usr/bin/env python

import urllib2
from BeautifulSoup import *
from urlparse import urljoin

#Create a list of words to ignore

class crawler:

	#initialize the crawler with the name of database
	def __init__(self,dbname):
		pass
	
	def __del__(self):
		pass
	
	def dbcommit(self):
		pass
	
	#Auxilliary function for getting an entry id and adding
	#it if it's not present 
	def getentryid(self,table,field,value,createnew=True):
		return None
	
	#index an individual page
	def addtoindex(self,url,soup):
		print 'Indexing %s' % url
	
	#Extract the text from an HTML page (no tags)
	def gettextonly(self,soup):
		return None
	
	#separate the words by any non-whitespace character
	def separatewords(self,text):
		return None
	
	#Return true if this url is already indexed
	def isindexed(self,url):
		return False
	
	#Add a link between two pages
	def addlinkref(self,urlFrom,urlTo,linkText):
		pass
	
	#Starting with a list of pages, do a breath first search
	#to the given depth, indexing pages as we go
	def crawl(self,pages,depth=2):
		
		for i in range(depth):
			newpages = set()
			for page in pages:
				try:
					c = urllib2.urlopen(page)
				except:
					print "Could not open %s" % page
					continue
				soup = BeautifulSoup(c.read())
				self.addtoindex(page,soup)
				
				links = soup('a')
				for link in links:
					if('href' in dict(link.attrs)):
						#to form the absolute url path
						url = urljoin(page,link['href'])
						if url.find("'")!=-1: continue
						url = url.split('#')[0] #remove location portion
						if url[0:4]=='http' and not self.isindexed(url):
							newpages.add(url)
						linkText = self.gettextonly(link)
						self.addlinkref(page,url,linkText)
				self.dbcommit()
			pages = newpages
	
	#Create database tables
	def createindextables(self):
		pass
