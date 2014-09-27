#!/usr/bin/env python
#document filtering using naive bayes
import re
import math

def getwords(doc):
	splitter = re.compile('\\W*')
	#split the words by non-alpha characters
	words = [s.lower() for s in splitter.split(doc) \
			if len(s)>2 and len(s)<20]
	
	#return the UNIQUE set of words only
	return dict([(w,1) for w in words])

def sampletrain(c1):
	c1.train('Nobody owns the water.','good')
	c1.train('the quick rabbit jumps fences','good')
	c1.train('buy pharmaceuticals now','bad')
	c1.train('make quick money at the online casino','bad')
	c1.train('the quick brown fox jumps','good')


class classifier:
	
	def __init__(self,getfeatures,filename=None):

		#Counts of feature/categroy combinations
		self.fc={}
		#Counts of documents in each category
		self.cc={}
		self.getfeatures = getfeatures
	
	#increase the count of a feature/categroy pair
	def incf(self,f,cat):
		
		self.fc.setdefault(f,{})
		self.fc[f].setdefault(cat,0)
		self.fc[f][cat]+=1
	
	#increase the count of a category
	def incc(self,cat):
		
		self.cc.setdefault(cat,0)
		self.cc[cat]+=1
	
	#the number of times a feature has appeared in a categroy
	def fcount(self,f,cat):
		
		if f in self.fc and cat in self.fc[f]:
			return float(self.fc[f][cat])
		return 0.0
	
	#the number of items in a categroy
	def catcount(self,cat):
			
		if cat in self.cc:
			return float(self.cc[cat])
		return 0
	
	#the total number of items
	def totalcount(self):
		return sum(self.cc.values());
	
	#the list of all categories
	def categories(self):
		return self.cc.keys()
	
	def train(self,item,cat):
	
		features = self.getfeatures(item)
		#Increment the count for every feature with this categroy
		for f in features:
			self.incf(f,cat)
		#increment the count for this categroy
		self.incc(cat)
	
	
	#returns P(word|category)
	def fprob(self,f,cat):
		
		# no feature belongs to category 'cat'
		if self.catcount(cat)==0: return 0
		
		#The total number of times this feature appeared (0 or 1 for each document) in this
		#category divided by the total number of items in this category
		return self.fcount(f,cat)/self.catcount(cat)
	
	#adjusted P(word|category) to account for docuemnt nots seen
	def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
		
		#Calculate current probability
		basicprob = prf(f,cat)
		
		#Count the number of times this feature has appeared in all
		#categories
		totals=sum([self.fcount(f,c) for c in self.categories()])
		
		#Calculate the weighted average
		bp=((weight*ap)+(totals*basicprob))/(weight+totals)
		
		return bp
	
class naivebayes(classifier):
	
	def __init__(self,getfeatures):
		
		classifier.__init__(self,getfeatures)
		self.thresholds={}
	
	def setthreshold(self,cat,t):
			
		self.thresholds[cat]=t
	
	def getthreshold(self,cat):
		
		if cat not in self.thresholds: return 1.0
		return self.thresholds[cat]	
	
	def docprob(self,item,cat):
		
		features = self.getfeatures(item)
		
		#Multiply the probailities of all the feature together
		p = 1
		for f in features: p *= self.weightedprob(f,cat,self.fprob)
		
		return p
	
	def prob(self,item,cat):
		
		catprob = self.catcount(cat)/self.totalcount() #prior probability
		docprob = self.docprob(item,cat)
		
		return docprob*catprob	
	
	def classify(self,item,default=None):
		
		probs = {}
	
		#Find the category with the highest probability
		max = 0.0
		for cat in self.categories():
			probs[cat] = self.prob(item,cat)
			if probs[cat] > max:
				max = probs[cat]
				best = cat
		
		#make sure the probability exceeds threshold*next best
		for cat in probs:
			if cat==best: continue
			if probs[cat]*self.getthreshold(best)>probs[best]: return default
		return best

		
		
