import urllib2  
import sgmllib
import re,datetime,time
from checktime import checktime

class LinksParser(sgmllib.SGMLParser):
    urls = []  
    def __init__(self,basiceurl="http://www.99114.com"):
	sgmllib.SGMLParser.__init__(self)
	self.baiceurl=basiceurl
	 

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
			    print i
			    print "usetime is %s" % senurl.getusetime()
		    else:
			    oldtime=senurl.getusetime()

	    return oldtime

class basicUrl():
	def __init__(self,basicurl):
		self._basicurl=basicurl
		#self._basiccon="" #url con
		self._basictime=datetime.datetime.now()-datetime.datetime.now()
		self._basictime=datetime.datetime.now()-datetime.datetime.now()

	def getbasictime(self):
		a=checktime(urllib2.urlopen)
		a.check(self._basicurl)
		self._basiccon=a.getvalue()
		self._basictime=a.getusetime()

	def __getsencondtime(self):
		value=self._basiccon.read()
		p=LinksParser()
		p.feed(value)
		f.close()
		#[next] how to get total


def test_link():	
	url='http://www.99114.com'
	#url="http://shop.99114.com/41300055"
	p =  LinksParser(url) 
    	time_start=datetime.datetime.now()
    	f = urllib2.urlopen(url)  
    	time_end=datetime.datetime.now()
    	time_using=time_end-time_start
    	print "start time is:%s" % time_start
    	print "end time is %s" % time_end
    	print "use time is:%s" % time_using
    	value = f.read()  
    	#print value  
    	p.feed(value)  
	secondtime=p.geturl()
	print "secondurl usetime is %s" % secondtime
	toturl=p.geturltot()
    	#for url in p.urls:  
		#print "url is: %s" % url  
          
    	f.close()  
    	p.close()
	print "url :%s \t usetime is: %s \t toturl:%s" % (url,time_using+secondtime,toturl )

if __name__ == "__main__" :
	
	check_time=60	#check 60*2=120min
	step=2*60 #step 120s
	for a in range(1,check_time):
		starttime=datetime.datetime.now()
		print "&"*30
		print "ID:%s\tTESTSTART TIME:%s" % (a,starttime)
		test_link() # check
		print "&"*30

		time.sleep(step)







