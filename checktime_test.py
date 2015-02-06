from checktime_sqlte import checktime
import unittest
import urllib2  

class test_checktime(unittest.TestCase):
	def test_basic(self):
		a=checktime(urllib2.urlopen)
		a.check('http://www.99114.com')
		a.get_time()
	
	def test_MOREERR(self):
		#HTTP404 test
		a=checktime(urllib2.urlopen)
		for i in range(1,20):
			url='http://www.99114.com/sadfd'+str(i)
			a.check(url)
			a.get_time()
			a.save_check_err(tcid=str("unittest"+str(i)))
		#print checktime.geterrs

if __name__ == "__main__":
	unittest.main()
