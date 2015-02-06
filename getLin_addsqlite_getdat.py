# -*- coding=utf-8 -*-
import urllib2  
import sgmllib
import re,datetime,time
from checktime_sqlte import checktime
from savesqlit import savesqlit 

class LinksParser(sgmllib.SGMLParser):
    #urls = []  
    def __init__(self,basiceurl="http://www.99114.com"):
	sgmllib.SGMLParser.__init__(self)
	self.baiceurl=basiceurl
	self._maxusetimeurl=""
	self.urls=[] 
	#self.urls.append(self.baiceurl)

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
    def _errurl(self,url,x):
	    """处理存在问题的二级资源 """
	    if(""==x.gethttperr()):
		    return 0
	    else:
		    #二级资源存在报错
		    self.url_err_lists.append({'url':url,'err':x.gethttperr()})
		    return 1


    def geturl(self):
	    self.urls_time={}
	    self.url_lists=[] #二级资源排序使用
	    self.url_err_lists=[] #访问存在问题的二级资源列表
	    oldtime=datetime.datetime.now()-datetime.datetime.now()
	    for i in self.urls:
		    
		    senurl=checktime(urllib2.urlopen)
		    senurl.check(i)
		    #处理二级资源为err的内容到self.url_err_lists中
		    if (1 == self._errurl(i,senurl)):
			    continue
		
	            #处理正常返回的二级资源
		    newtime=senurl.getusetime()
		    self.url_lists.append({'url':i,'usetime':newtime})

		    if (oldtime>newtime):
			    #print i
			    #print "usetime is %s" % senurl.getusetime()
			    pass
		    else:
			    oldtime=senurl.getusetime()
			    self._maxusetimeurl=i

	    #self.__getlists()
	    return oldtime,self._maxusetimeurl

    def geturl_xpar(self,percentage):
	    """返回指定percentage率的二级资源时间和url """
	    #获得排序后的二级资源self.getlists()
	    u=self.getlists() 
	    #指定百分比返回
	    date_lists=[]
	    if ((percentage<0) or (percentage>1) ):
		    percentage=1
	    date_lists.append(percentage)
	    time=self.getlistana(date_lists)
	    return time[0]
		
    def __getlists(self):
	    #将二级资源处理分析
	    u=sorted(self.url_lists,key = lambda x:x['usetime'])
	    print "P"*50
	    num=len(u)
	    print num,int(num*0.9)
	    print u[int(num*0.9)]['usetime']
    	    print "P"*50
            f=open("lists\\a.log","w")
		
	    f.write(str(u))
	    f.close()
	
    def getlistana(self,par_list=[1]):
	    date_lists=[]
    	    u=sorted(self.url_lists,key = lambda x:x['usetime'])#将二级资源按使用时间排序
	    num=len(u)						

	    for i in par_list:
		    x=u[int(num*i)]['usetime']
		    date_lists.append(x)

	    return date_lists
    def getlists(self):
	    """返回self.url_lists 排序后的内容 """
	    return sorted(self.url_lists,key = lambda x:x['usetime'])#将二级资源按使用时间排序
    def geterrlists(self):
	    """返回 self.url_err_lists 列表内容 """
	    return  self.url_err_lists

class basicUrl():
	def __init__(self,basicurl):
		self._basicurl=basicurl
		#self._basiccon="" #url con
		self.httpcode="0"

		self._basictime=datetime.datetime.now()-datetime.datetime.now()
		self._basictime=datetime.datetime.now()-datetime.datetime.now()
		self._sencodusetime=datetime.datetime.now()-datetime.datetime.now()
		self._toturl=1

		#分析数据参数
		self.parents=[0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95] #要分析的资源百分比
		self.parents_lists=[]
		self.sencod_lists=[] #二级资源列表

	def getbasictime(self):
		"""[popexizhi add] 19/12/14 dba交流结果，对5xx,4xx server 的返回值使用时间用120标识
		# 当前修改位置为访问all url的设置位置，潜在问题是如果非basic地址存在4xxx 或 5xx 就使整个返回time为过大内容
		# 依赖条件("" == self.geterr) 
		  self._usetime=120s
		"""
		self._stattime=datetime.datetime.now()
		a=checktime(urllib2.urlopen)
		a.check(self._basicurl)
		self._basiccon=a.getvalue()
		self._basictime=a.getusetime()
		if (""==a.gethttperr() ):
			#get sencond
			self.__getsencondtime()
		
			#save db
			#save err
			#a.save_check_err(tcid=str("TCID:"+str(self._stattime)))
		else:
			#获得e中的异常码,设置为httpcode
			(code,con)=str(a.gethttperr()).split(":")
			self.httpcode=re.sub(re.compile("\D"),"",code)
			#设置usetime=120s 
			self._totusetime=datetime.timedelta(seconds=120)
			self._basictime=datetime.timedelta(seconds=120)



	def __getsencondtime(self):
		value=self._basiccon.read()
		p=LinksParser(self._basicurl)
		p.feed(value)
		
		#[next] how to get total
		self._sencodMAXusetime,self._senMAXurl=p.geturl()
		self._sencodusetime=p.geturl_xpar(float(self.parents[-1])) #当前使用分析数据中的最大分析内容
		self._toturl=self._toturl+p.geturltot() 
		self._endtime= datetime.datetime.now()
		self.parents_lists=p.getlistana(self.parents) #获得二级资源数据
		self.sencod_lists=p.getlists() #获得二级资源列表
		self.sencod_err_lists=p.geterrlists()#获得存在问题的二级资源列表
		p.close()
		self._totusetime=self._basictime+self._sencodusetime
	
	def getresult(self):
		#save db
		a=savesqlit("check.db")
		data='"%s","%s","%s","%s","%s","%s"' % (str(self._stattime),str(self._totusetime),str(self._basictime),str(self._sencodusetime),self._senMAXurl,self._basicurl+"["+str(self._stattime)+"]")
		#print "%"*20
		#print "data is %s" % data
		a.add_totle(data)
		#print totle
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

	def getSumDate(self,spl="\t\t"):
		
		data=str(self._stattime)+spl+str(self._totusetime)+spl+str(self._basictime)+spl+str(self._sencodusetime)+spl+str(self._senMAXurl)+"\n"
		return data

	def getdatDate(self,spl="||"):
		
		return_errcode=self.httpcode
		time_date=str(self._stattime.year)+"-"+str(self._stattime.month)+"-"+str(self._stattime.day)\
				+" "+str(self._stattime.hour)+":"+str(self._stattime.minute)+":"+str(self._stattime.second)

		data=time_date+spl\
				+str(float(self._totusetime.seconds)+0.000001*float(self._totusetime.microseconds))+spl\
				+str(float(self._basictime.seconds)+0.000001*float(self._basictime.microseconds))+spl\
				+return_errcode+"\n"

		return data
	
	def getanaDate(self,spl=","):
		"""获得资源分析数据列表 """
		


		time_date=str(self._stattime.year)+"-"+str(self._stattime.month)+"-"+str(self._stattime.day)\
				+" "+str(self._stattime.hour)+":"+str(self._stattime.minute)+":"+str(self._stattime.second)
		anadate="\n"+time_date
		#获得指定资源的分析数据

		for i in self.parents_lists:
			anadate=anadate+spl\
					+str(\
					float(self._basictime.seconds)+0.000001*float(self._basictime.microseconds)\
					+float(i.seconds)+0.000001*float(i.microseconds))
		#120sbasictime处理
		if (0 == len(self.parents_lists)):
			outtime=spl+"120"
			anadate=anadate+outtime
			
		
		
		#拼装分析数据
		#save
		#f=open("lists\\analists.log","a")
		#f.write(anadate)sorted(self.url_lists,key = lambda x:x['usetime'])#将二级资源按使用时间排序
		#f.close()
		return anadate
	def getlists(self,spl="\t"):
		"""拼装资源内容 """
		
		time_date=str(self._stattime.year)+"-"+str(self._stattime.month)+"-"+str(self._stattime.day)\
				+" "+str(self._stattime.hour)+":"+str(self._stattime.minute)+":"+str(self._stattime.second)
		anadate="\n"+time_date
		for i in self.sencod_lists:
			url=i['url']
			usetime=i['usetime']
			anadate=anadate+spl+url+spl+str(usetime)+"\n"
		return anadate
	def geterrlists(self,spl="\n"+"*"*20+"\n"):
		"""拼装错误列表资源 """
		
		time_date=str(self._stattime.year)+"-"+str(self._stattime.month)+"-"+str(self._stattime.day)\
				+" "+str(self._stattime.hour)+":"+str(self._stattime.minute)+":"+str(self._stattime.second)
		errlists="\n"+time_date
		for i in self.sencod_err_lists:
			url=i['url']
			err=i['err']
			errlists=errlists+spl+url+spl+str(err)+"\n"
		return errlists

if __name__ == "__main__" :
	url="http://www.99114.com"
	#url="http://shop.99114.com/41316287/pd75458314.html"
	check_time=50 #check 60*2=120min
	step=10 #step 120s
	getdata=""
	for a_num in range(1,check_time):
		starttime=datetime.datetime.now()
		#print "&"*30
		#print "ID:%s\tTESTSTART TIME:%s" % (a,starttime)
		 
		# check
		a=basicUrl(url)
		a.getbasictime()
		a.getresult()
		getdata=getdata+a.getSumDate()+"\t"+str(a_num)
		
		print "&"*30
		print a.getdatDate()
		a.getanaDate()
		f=open("test.dat","a")
		f.write(a.getdatDate())
		f.close()
		time.sleep(step)
	

	
	#print getdata
	#f=open("testdate.csv","w")
	#f.write(getdata)
	#f.close()






