import sqlite3
import re

class savesqlit():
	def __init__(self,dbname='tests.db',testid="1"):
		self.db=dbname
		self.testid=testid

	def create_datas(self,sql="CREATE TABLE sencond_url_usetime (url text, usetime text,errmassage text,ID text)"):
		#create
		
		try:
			self.conn=sqlite3.connect(self.db)
			self.conn.execute(sql)
			self.conn.close()
		except:
			print "create table err"
			pass



	def add_datas(self,datas,dbname='sencond_url_usetime',dbcol='url, usetime,errmassage,ID'):
		#insert {}
		#Opened database
		self.conn=sqlite3.connect(self.db)
		#create table

		#save dates
		try:
			for key in datas:
				usetime_errmassage=re.sub("\t","','",datas[key]) # #sub usetime and errmassage 
				#print usetime_errmassage
				
				sql="insert into "+dbname+"("+dbcol+")"+" VALUES ( '"+key+"','"+usetime_errmassage+"','"+self.testid+"')"
				#print sql
				self.conn.execute(sql)
				self.conn.commit()
		except BaseException,e:
			
			print "except %s" % e
		finally:
			self.conn.close()


	def inster_data(self,data,dbname='sencond_url_usetime',dbcol='url, usetime,errmassage,ID'):
		#insert 
		#Opened database
		self.conn=sqlite3.connect(self.db)
		#create table

		#save dates
		try:
			#print re.sub("\'","",data)
			sql="insert into "+dbname+"("+dbcol+")"+" VALUES ( "+re.sub("\'","",data)+")"
			#print sql
			self.conn.execute(sql)
			self.conn.commit()

		except BaseException,e:
			
			print "except %s" % e
		finally:
			self.conn.close()


	
	def add_totle(self,datas):
		#create table
		create_sql='''CREATE TABLE sum_test
                               (start text,tot_usetime text,first_usetime text, sec_Max_usetime text, securl text,ID text)'''
		self.create_datas(create_sql)

		#save sql
		insert_datas=datas
		dbname="sum_test"
		dbcol="start,tot_usetime,first_usetime,sec_Max_usetime,securl,ID"
		self.inster_data(insert_datas,dbname,dbcol)


if __name__=="__main__":
	a=savesqlit()
	a.create_datas()
	#datas={'http://www.99114.com/sadfd16': '2014-11-20 12:23:44.273000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd17': '2014-11-20 12:23:44.334000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd14': '2014-11-20 12:23:44.168000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd15': '2014-11-20 12:23:44.231000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd12': '2014-11-20 12:23:44.043000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd13': '2014-11-20 12:23:44.106000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd10': '2014-11-20 12:23:43.919000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd11': '2014-11-20 12:23:43.981000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd18': '2014-11-20 12:23:44.400000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd19': '2014-11-20 12:23:44.444000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd4': '2014-11-20 12:23:42.976000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd5': '2014-11-20 12:23:43.631000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd6': '2014-11-20 12:23:43.692000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd7': '2014-11-20 12:23:43.734000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd1': '2014-11-20 12:23:42.437000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd2': '2014-11-20 12:23:42.703000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd3': '2014-11-20 12:23:42.850000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd8': '2014-11-20 12:23:43.794000\tHTTP Error 404: Not Found', 'http://www.99114.com/sadfd9': '2014-11-20 12:23:43.856000\tHTTP Error 404: Not Found'}

	#a.add_datas(datas)
	totle_data='"31:43.8","00:01.2","00:01.0","00:00.1","http://img.99114.com/2014/1/10/9/41267231.gif","maintestID"'
	a.add_totle(totle_data)		
