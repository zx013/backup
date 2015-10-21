#-*- coding:utf-8 -*-
try:
	import simplejson as json
except:
	import json
import cookielib
import urllib
import urllib2
import time

class BaiduDisk:
	def __init__(self, username, password):
		cookie = cookielib.LWPCookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		self.username = username
		self.password = password
		
	def post(self, url, data=None):
		req = urllib2.Request(url=url, data=data)
		#res = urllib2.urlopen(req).read()
		res = self.opener.open(req).read()
		return res
		 
	def login(self):
		#获取cookie
		url = 'http://www.baidu.com'
		self.post(url)
		
		#获取token
		url = 'https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&class=login&tt=%s&logintype=dialogLogin&callback=%s' % (int(time.time()), 0)
		token = json.loads(self.post(url).replace("'", '"'))['data']['token']
		
		url = 'https://passport.baidu.com/v2/api/?logincheck&token=%stpl=mn&apiver=v3&tt=%s&username=%s&isphone=false&callback=%s' % (token, int(time.time()), '', 0)
		self.post(url)
		
		url = 'https://passport.baidu.com/v2/api/?login'
		data = {
			'staticpage': 'http://www.baidu.com/cache/user/html/v3Jump.html',
			'charset': 'UTF-8',
			'token': token,
			'tpl': 'mn',
			'apiver': 'v3',
			'tt': int(time.time()),
			'codestring': '',
			'isPhone': 'false',
			'safeflg': '0',
			'u': 'http://www.baidu.com/',
			'quick_user': '0',
			'usernamelogin': '1',
			'splogin': 'rate',
			'username': self.username,
			'password': self.password,
			'verifycode': '',
			'mem_pass': 'on',
			'ppui_logintime': '5000',
			'callback': 'parent.bd__pcbs__oa36qm'
		}
		ret = self.post(url, urllib.urlencode(data))
		return ret.split('err_no=')[1].split('&')[0]
	
	def show(self):
		url = 'http://pan.baidu.com/api/quota?' + urllib.urlencode({'method': 'info'})
		print self.post(url)
		
	def upload(self):
		pass
		#url = 'https://c.pcs.baidu.com/rest/2.0/pcs/quota?%s' % urllib.urlencode()

	def dowlload(self):
		pass
		
		
if __name__ == '__main__':
	disk = BaiduDisk('username', 'password')
	disk.login()
	disk.show()