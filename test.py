# http://www.softwareishard.com/blog/firebug/http-archive-specification/
# http://blog.csdn.net/kazeik/article/details/8773573

import urllib2  
import sgmllib
import re
import datetime

class LinksParser(sgmllib.SGMLParser):  
    urls = []  
    def do_a(self, attrs):  
        for name, value in attrs:  
            if name == 'href' and value not in self.urls:  
                if value.startswith('http'):
			if re.search('99114',value):
				self.urls.append(value)  
                    		#print value
			else:
				pass
		else:
			pass
            else:  
                continue  
            return  
  
if __name__ == "__main__":  
    # str = ""  
    # if str.strip() is '':  
        # print "str is None"  
    # else:  
        # print "str is no None"  
  
  
    p =  LinksParser() 
    time_start=datetime.datetime.now()
    f = urllib2.urlopen('http://www.99114.com')  
    time_end=datetime.datetime.now()
    time_using=time_end-time_start
    print "start time is:%s" % time_start
    print "end time is %s" % time_end
    print "use time is:%s" % time_using
    value = f.read()  
    #print value  
    p.feed(value)  
      
    #for url in p.urls:  
        #print url  
          
    f.close()  
    p.close()  

