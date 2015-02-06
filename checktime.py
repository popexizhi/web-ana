import urllib2  
import sgmllib
import re
import datetime

class checktime():
	def __init__(self,_checkfun):
		self._fun=_checkfun
		self._getvale=""
		self.geterr=""

	def check(self,check_arg):
		self._stattime=datetime.datetime.now()
		try:
			self._getvale=self._fun(check_arg)
			self._endtime=datetime.datetime.now()
			self._usetime=self._endtime-self._stattime

		except urllib2.HTTPError,e:
			print "*"*20
			print e
			print "HTTPError url is %s" % check_arg
			print "*"*20
			self.geterr=e
			self._endtime=datetime.datetime.now()
			self._usetime=datetime.datetime.now()-datetime.datetime.now()
		except urllib2.URLError,e:
			print "*"*20
			print e
			print "URLError url is %s" % check_arg
			print "*"*20
			self.geterr=e
			self._endtime=datetime.datetime.now()
			self._usetime=datetime.datetime.now()-datetime.datetime.now()
		except socket.timeout,e:
			print "*"*20
			print e
			print "socket.error url is %s" % check_arg
			print "*"*20
			self.geterr=e
			self._endtime=datetime.datetime.now()
			self._usetime=datetime.datetime.now()-datetime.datetime.now()

		
		
	def get_time(self):
		print "~"*20
		print "usetime: %s\tstattime:%s\tendtime:%s" % (self._usetime,self._stattime,self._endtime) 
		print "~"*20

	def getusetime(self):
		return self._usetime
		
	
	def getvalue(self):
		return self._getvale
		

	def __iserr(self,reage):
		if ("" == self.geterr):
			return reage
		else:
			return datetime.datetime.now()-datetime.datetime.now()

if __name__ == "__main__":  
	a=checktime(urllib2.urlopen)
	a.check('http://www.99114.com')
	a.get_time()
