#-*- coding:utf-8 -*-
#百度云网盘模块只提供与备份相关的接口
#参考文章及内容：
#https://github.com/Yangff/node_pcsapi/blob/master/baidulogin.md
#python库baidupcsapi-0.3.5
#文件处理一律用utf-8，只有在打开文件时转换成unicode
import os
import json
import cookielib
import urllib
import urllib2
import hashlib
import time
from log import error_log, make_list, split_file, convert_utf8, convert_unicode


default_headers = {
	'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.2.0',
	'Referer': 'http://pan.baidu.com/disk/home',
	#'x-requested-with': 'XMLHttpRequest',
	'Accept': 'application/json, text/javascript, */*; q=0.8',
	'Accept-language': 'zh-cn, zh;q=0.5',
	#'Accept-encoding': 'gzip, deflate',
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

def loads(data):
	try: return convert_utf8(json.loads(data))
	except: return data

#编码前先将数据转换为str(utf-8)类型
def urlencode(data):
	return urllib.urlencode(convert_utf8(data))


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
class Baidu:
	def __init__(self, username, password):
		self.cookie = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
		self.username = username
		self.password = password

	@error_log('')
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
		self.token = loads(self.request(url).replace("'", '"'))['data']['token']

		#url = 'https://passport.baidu.com/v2/api/?logincheck&token=%stpl=mn&apiver=v3&tt=%s&username=%s&isphone=false&callback=%s' % (self.token, int(time.time()), '', 0)
		#self.request(url)

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
		ret = self.request(url, data=urlencode(data))
		return ret.split('err_no=')[1].split('&')[0]

	#url_type: 'pan'或'pcs'
	#method: 'list, 'file'等
	#params: ?之后的参数
	def post(self, url_type, method, params={}, **kwargv):
		#添加默认参数
		params.update(default_params)
		kwargv.setdefault('headers', {}).update(default_headers)
		if isinstance(kwargv.get('data'), dict): #数据为字典时进行编码
			kwargv['data'] = urlencode(kwargv['data'])
		url = '%s%s?%s' % (default_url[url_type], method, urlencode(params))
		print url
		return loads(self.request(url, **kwargv))

	def get_config_type(self):
		return 'baidu'

	#获得配额信息
	def quota(self):
		return self.post('pan', 'quota', {'method': 'info'})

	#查看目录下的文件
	@error_log([])
	def show(self, target_path):
		res = self.post('pan', 'list', {'dir': target_path})
		target_list = [val['path'] for val in res['list'] if not val['isdir']][::-1] #默认是从小到大排列
		return target_list

	#创建目录
	def mkdir(self, target_path):
		return self.post('pan', 'create', data={'path': target_path, 'isdir': 1})

	#删除文件
	def delete(self, target_list):
		target_list = make_list(target_list)
		return self.post('pan', 'filemanager', {'opera': 'delete'}, data={'filelist': json.dumps(target_list)})
	
	def check_path(self, target_path):
		return not self.get_metas(target_path)['errno']

	#上传文件，传入参数为绝对路径
	#dk.upload(['C:/Users/zzy/Desktop/测试-.－。', 'C:/Users/zzy/Desktop/baidupcsapi-0.3.5.tar.gz'], '/')
	def upload(self, source_list, target_path):
		source_list = make_list(source_list)
		for source_file in source_list:
			try:
				source_file, source_path, source_name, target_name = split_file(source_file)
				with open(convert_unicode(source_file), 'rb') as fp:
					source_data = fp.read()
				content_type, data = encode_multipart_formdata([('file', source_name, source_data)])
				headers = {'Content-Type': content_type, 'Content-length': str(len(data))}
				params = {'method': 'upload', 'dir': target_path, 'ondup': 'overwrite', 'filename': target_name}
				print self.post('pcs', 'file', params, headers=headers, data=data)
			except: pass

	#获取文件或目录的元信息，dlink=1则包含下载链接
	#传入参数无论为utf-8或unicode，均返回unicode
	@error_log({})
	def get_metas(self, target_list, dlink=0):
		target_list = make_list(target_list)
		return self.post('pan', 'filemetas', data={'dlink': dlink, 'target': json.dumps(target_list)})

	#获取下载链接
	#dk.get_link(['/测试-.－。', '/ab'])
	def get_link(self, target_list):
		target_list = make_list(target_list)
		metas = []
		for target_file in target_list:
			try:
				target_file, target_path, target_name, source_name = split_file(target_file)
				meta = self.get_metas([target_file], 1)
				metas.append((source_name, meta['info'][0]['dlink']))
			except: pass
		return metas

	#下载文件
	#dk.download(['/测试-.－。', '/ab'], 'F:/')
	def download(self, target_list, source_path):
		target_list = make_list(target_list)
		dlink_list = self.get_link(target_list)
		for source_name, dlink in dlink_list:
			data = self.request(dlink)
			with open(convert_unicode('%s/%s' % (source_path, source_name)), 'wb') as fp:
				fp.write(data)

if __name__ == '__main__':
	disk = Baidu('baidu_yun_test@sina.com', 'test123456')
	disk.login()
	disk.quota()
	disk.show('/')