#-*- coding:utf-8 -*-
#百度云网盘模块只提供与备份相关的接口
#参考文章及内容：
#https://github.com/Yangff/node_pcsapi/blob/master/baidulogin.md
#python库baidupcsapi-0.3.5
import os
import json
import cookielib
import urllib
import urllib2
import hashlib
import time


default_headers = {
	'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.2.0',
	'Referer': 'http://pan.baidu.com/disk/home',
	#'x-requested-with': 'XMLHttpRequest',
	'Accept': 'application/json, text/javascript, */*; q=0.8',
	'Accept-language': 'zh-cn, zh;q=0.5',
	'Accept-encoding': 'gzip, deflate',
	'Pragma': 'no-cache',
	'Cache-control': 'no-cache',
}

default_params = {
	'app_id': '250528'
}

default_url = {
	'pan': 'http://pan.baidu.com/api/',
	'pcs': 'http://c.pcs.baidu.com/rest/2.0/pcs/'
}


def get_md5(data):
	md5 = hashlib.md5()
	md5.update(data)
	return md5.hexdigest()

def encode_multipart_formdata(files):
	BOUNDARY = b'----------ThIs_Is_tHe_bouNdaRY_$'
	S_BOUNDARY = b'--' + BOUNDARY
	E_BOUNARY = S_BOUNDARY + b'--'
	CRLF = b'\r\n'
	BLANK = b''
	l = []
	for (key, filename, content) in files:
		l.append(S_BOUNDARY)
		l.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
		l.append(BLANK)
		l.append(content)
	l.append(E_BOUNARY)
	l.append(BLANK)
	body = CRLF.join(l)
	content_type = 'multipart/form-data; boundary=%s' % BOUNDARY.decode()
	return content_type, body


#短时间内多次登陆百度账号会导致需要输入验证码，以致无法登陆
class BaiduDisk:
	def __init__(self, username, password):
		self.cookie = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
		self.username = username
		self.password = password

	def request(self, url, **kvargv):
		req = urllib2.Request(url=url, **kvargv)
		res = self.opener.open(req).read()
		return res

	def login(self):
		#获取cookie
		url = 'http://www.baidu.com'
		self.request(url)

		#获取token
		url = 'https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&class=login&tt=%s&logintype=dialogLogin&callback=%s' % (int(time.time()), 0)
		self.token = json.loads(self.request(url).replace("'", '"'))['data']['token']

		url = 'https://passport.baidu.com/v2/api/?logincheck&token=%stpl=mn&apiver=v3&tt=%s&username=%s&isphone=false&callback=%s' % (self.token, int(time.time()), '', 0)
		self.request(url)

		url = 'https://passport.baidu.com/v2/api/?login'
		data = {
			'staticpage': 'http://www.baidu.com/cache/user/html/v3Jump.html',
			'charset': 'UTF-8',
			'token': self.token,
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
		ret = self.request(url, data=urllib.urlencode(data))
		return ret.split('err_no=')[1].split('&')[0]

	#url_type: 'pan'或'pcs'
	#method: 'list, 'file'等
	#params: ?之后的参数
	def post(self, url_type, method, params={}, **kwargv):
		#添加默认参数
		params.update(default_params)
		kwargv.setdefault('headers', {}).update(default_headers)
		if isinstance(kwargv.get('data'), dict): #数据为字典时进行编码
			kwargv['data'] = urllib.urlencode(kwargv['data'])
		url = '%s%s?%s' % (default_url[url_type], method, urllib.urlencode(params))
		print url
		return self.request(url, **kwargv)

	#获得配额信息
	def quota(self):
		return self.post('pan', 'quota', {'method': 'info'})

	#查看目录下的文件
	def show(self, path='/'):
		return self.post('pan', 'list', {'dir': '/'})

	#比较文件
	def compare(self):
		pass

	#创建目录
	def mkdir(self, path):
		return self.post('pan', 'create', data={'path': path, 'isdir': 1})

	#删除文件
	def delete(self, file_list):
		return self.post('pan', 'filemanager', {'opera': 'delete'}, data={'filelist': json.dumps(file_list)})

	#上传文件，传入参数为绝对路径
	#dk.upload(['C:/Users/zzy/Desktop/测试-.－。', 'C:/Users/zzy/Desktop/baidupcsapi-0.3.5.tar.gz'], '/')
	def upload(self, file_list, path):
		for file_full in file_list:
			file_path, file_name = os.path.split(file_full)
			with open(file_full.decode('utf-8'), 'rb') as fp:
				file_data = fp.read()
			content_type, data = encode_multipart_formdata([('file', file_name, file_data)])
			headers = {'Content-Type': content_type, 'Content-length': str(len(data))}
			params = {'method': 'upload', 'dir': path, 'ondup': 'overwrite', 'filename': file_name}
			print self.post('pcs', 'file', params, headers=headers, data=data)

	#获取文件或目录的元信息，dlink=1则包含下载链接
	def get_metas(self, file_list, dlink):
		return self.post('pan', 'filemetas', data={'dlink': dlink, 'target': json.dumps(file_list)})
	
	#获取下载链接
	#dk.get_link(['/测试-.－。', '/ab'])
	def get_link(self, file_list):
		metas = []
		for file_full in file_list:
			try:
				file_path, file_name = os.path.split(file_full)
				meta = json.loads(self.get_metas([file_full], 1))
				metas.append((file_name, meta['info'][0]['dlink']))
			except: pass
		return metas

	#下载文件
	#dk.download(['/测试-.－。', '/ab'], 'F:/')
	def download(self, file_list, path):
		dlink_list = self.get_link(file_list)
		for file_name, dlink in dlink_list:
			data = self.request(dlink)
			with open(('%s/%s' % (path, file_name)).decode('utf-8'), 'wb') as fp:
				fp.write(data)

if __name__ == '__main__':
	disk = BaiduDisk('baidu_yun_test@sina.com', 'test123456')
	disk.login()
	disk.quota()
	disk.show('/')