#-*- coding:utf-8 -*-
#百度云网盘模块只提供与备份相关的接口
#参考文章及内容：
#https://github.com/Yangff/node_pcsapi/blob/master/baidulogin.md
#python库baidupcsapi-0.3.5
try:
	import simplejson as json
except:
	import json
import cookielib
import urllib
import urllib2
import time

#短时间内多次登陆百度账号会导致需要输入验证码，以致无法登陆
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

	#https://pcs.baidu.com/rest/2.0/pcs/{object_name}?{query_string}
	def post_disk(self, object_name, query_string):
		url = 'http://pan.baidu.com/api/%s' % object_name
		return self.post(url, urllib.urlencode(query_string))

	#获得配额信息
	def quota(self):
		return self.post_disk('quota', {'method': 'info'})

	#查看目录下的文件
	def show(self, path='/'):
		return self.post_disk('list', {'dir': path})

	#创建目录
	def mkdir(self, path):
		return self.post_disk('create', {'path': path, 'isdir': 1})
	
	#删除文件
	def delete(self):
		pass

	#上传文件
	def upload(self):
		pass

	#下载文件
	def download(self):
		pass


if __name__ == '__main__':
	disk = BaiduDisk('baidu_yun_test@sina.com', 'test123456')
	disk.login()
	disk.quota()
	disk.show('/')