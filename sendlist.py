#-*- coding=utf-8 -*-
from getLin_addsqlite_getdat import basicUrl
import re,threading,time
import os

class sendlist():
	def __init__(self,filename="url_list.log"):
		self.urlfilename=filename
		self.urls=[]
		self._geturls()
		#self.urls=["http://www.99114.com","http://shop.99114.com/41316287/pd75458314.html"]
		self.step=2*60 # step 120s
		
		
	def _geturls(self):
		x=open(self.urlfilename)
		urls=x.read()
		x.close()
		for t in urls.split("\n"):
			if ("" == t):
				#处理文件中空行和文件尾部分
				pass
			else:
				self.urls.append(t)
	def doing_test(self):
		while(1):
			self.doing_list()
			time.sleep(self.step)
			

		#print self.urls
	def doing_list(self):
		num=self.step
		threads=[]
		for url in self.urls:
			thread=doing_l(url)
			thread.start()
			threads.append(thread)

class doing_l(threading.Thread):
	def __init__(self,url):
		threading.Thread.__init__(self)
		self.url=url
	
	def __addfiledef(self,filename,filedef="time,usetime,basic,err"):
		""" 为文件首行加入文件说明 """
		#只处理新创建的文件
		if (False == (os.path.isfile(filename)) ): #如果不存在就返回False 
			f=open(filename,"a")
			f.write(filedef+"\n")
			f.close()


	def run(self):
		#x_path="D:\\PROGRA~2\\EASYPH~1.1\\www\\testjs\\"
		#x_path="/data/webserver/apache-tomcat-8.0.15/webapps/testjs/"
		x_path="lists\\"
		DBA_path="lists_DBA\\"
		#DBA_path="/data/monitor/nrpe/logs/"
		t=basicUrl(self.url)
		t.getbasictime()
		print "$"*20
		g_date=t.getdatDate()	#DBA监控使用
		print g_date
		g_date_selfjs=t.getdatDate(",")	#自监控使用

		g_anadate=t.getanaDate()	#二级资源分段分析使用
		print g_anadate
		g_sencoddate=t.getlists()+t.geterrlists()	#二级资源详情和err部分
		print g_sencoddate

		#相同文件操作加锁处理
		#保存文件内容
		new_filename=re.sub("http://|/|\r","_",self.url)
		new_filename=DBA_path+new_filename+".dat"
		self.__addfiledef(new_filename)
		f=open(new_filename,"a")
		f.write(g_date)
		f.close()
		#增加自监控js使用
		new_filename_selfjs=re.sub("http://|/|\r","_",self.url)
		new_filename_selfjs=x_path+"ALL_"+new_filename_selfjs+".log"
		self.__addfiledef(new_filename_selfjs)
		f=open(new_filename_selfjs,"a")
		f.write(g_date_selfjs)
		f.close()		

		#保存分析文件内容
		new_anafilename=re.sub("http://|/|\r","_",self.url)
		filedef="time,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95"
		new_anafilename=x_path+new_anafilename+".log"
		self.__addfiledef(new_anafilename,filedef)
		f=open(new_anafilename,"a")
		f.write(g_anadate)
		f.close()

		#保存二级资源内容
		new_anafilename=re.sub("http://|/|\r","_",self.url)
		new_anafilename=x_path+new_anafilename+"_sencod.log"
		f=open(new_anafilename,"a")
		f.write(g_sencoddate)
		f.close()
	

if __name__=="__main__":
	a=sendlist()
	a.doing_test()
	
