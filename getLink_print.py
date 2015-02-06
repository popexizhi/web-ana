import urllib2  
import sgmllib
import re,datetime,time
from checktime import checktime

class LinksParser(sgmllib.SGMLParser):
    urls = []  
    def __init__(self,basiceurl="http://www.99114.com"):
	sgmllib.SGMLParser.__init__(self)
	self.baiceurl=basiceurl
	self._maxusetimeurl=""
	 

    def geturltot(self):
	return len(self.urls)

    def do_script(self, attrs):
	baiceurl=self.baiceurl
	#js
        for name, value in attrs:  
            if name == 'src' and value not in self.urls:  
                if value.startswith('/static'):
			self.urls.append(baiceurl+value)  
	                #print baiceurl+value
		else:
			if re.search('99114',value):
				self.urls.append(value)
				#print value
			
            else:  
                continue  
            return
     
    def do_link(self, attrs):
	baiceurl=self.baiceurl
	#<link>
        for name, value in attrs:  
            if name == 'href' and value not in self.urls:  
                if value.startswith('/static'):
			self.urls.append(baiceurl+value)  
	                #print baiceurl+value
		else:
			if re.search('99114',value):
				self.urls.append(value)
				#print value
			
            else:  
                continue  
            return

    def do_img(self, attrs):
	baiceurl=self.baiceurl
	#<img>
        for name, value in attrs:  
            if name == 'src' and value  not in self.urls and baiceurl+value  not in self.urls and baiceurl+'/'+value not in self.urls:  
                if value.startswith('/static'):
			self.urls.append(baiceurl+value)  
	                #print baiceurl+value
		else:
			if re.search('99114',value):
				self.urls.append(value)
				#print value
			if value.startswith('images'):
				self.urls.append(baiceurl+'/'+value)
				#print baiceurl+'/'+value

			
            else:  
                continue  
            return
    def geturl(self):
	    oldtime=datetime.datetime.now()-datetime.datetime.now()
	    for i in self.urls:
		    senurl=checktime(urllib2.urlopen)
		    senurl.check(i)
		    if (oldtime>senurl.getusetime()):
			    #print i
			    #print "usetime is %s" % senurl.getusetime()
			    pass
		    else:
			    oldtime=senurl.getusetime()
			    self._maxusetimeurl=i

	    return oldtime,self._maxusetimeurl

class basicUrl():
	def __init__(self,basicurl):
		self._basicurl=basicurl
		#self._basiccon="" #url con

		self._basictime=datetime.datetime.now()-datetime.datetime.now()
		self._basictime=datetime.datetime.now()-datetime.datetime.now()
		self._sencodusetime=datetime.datetime.now()-datetime.datetime.now()
		self._toturl=1

	def getbasictime(self):
		self._stattime=datetime.datetime.now()
		a=checktime(urllib2.urlopen)
		a.check(self._basicurl)
		self._basiccon=a.getvalue()
		self._basictime=a.getusetime()

		#get sencond
		self.__getsencondtime()

	def __getsencondtime(self):
		value=self._basiccon.read()
		p=LinksParser()
		p.feed(value)
		
		#[next] how to get total
		self._sencodusetime,self._senMAXurl=p.geturl()
		self._toturl=self._toturl+p.geturltot() 
		self._endtime= datetime.datetime.now()
		p.close()
		self._totusetime=self._basictime+self._sencodusetime
	
	def getresult(self):

		print "*"*20
		print "url is: %s" % self._basicurl
    		print "start time is:%s" % self._stattime
    		print "end time is %s" % self._endtime
    		print "first url use time is:%s" % self._basictime
		print "sencond url use time MAX is %s" % self._senMAXurl
		print "second url max use time is %s" % self._sencodusetime
		print "total USE TIME is %s" % self._totusetime
		print "total get url is %s" % self._toturl
		#print "\t"+"$"*10
		#print "\t"+"err url"
		print "*"*20



if __name__ == "__main__" :
	#url="http://www.99114.com"
	url="http://shop.99114.com/41316287/pd75458314.html"
	check_time=3	#check 60*2=120min
	step=2*60 #step 120s
	for a in range(1,check_time):
		starttime=datetime.datetime.now()
		print "&"*30
		print "ID:%s\tTESTSTART TIME:%s" % (a,starttime)
		 
		# check
		a=basicUrl(url)
		a.getbasictime()
		a.getresult()

		print "&"*30

		time.sleep(step)







