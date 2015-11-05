#-*- coding:utf-8 -*-
import os
import hashlib
import re
import time

from log import error_log

#()
#[(), (), ()]
#x
#[x, x, ()]
#整个输入列表为list，内部指定名称用tuple
#将单个元素或元组打包成列表
def make_list(source_file):
	if isinstance(source_file, list): return source_file
	else: return [source_file]

#'/root/ab' -> '/root/ab/', '/root', 'ab', 'ab'
#('/root/ab', 'cd') -> '/root/ab/', '/root', 'ab', 'cd'
def split_file(source_file):
	if isinstance(source_file, tuple):
		source_file, target_name = source_file
		source_path, source_name = os.path.split(source_file)
	else:
		source_path, source_name = os.path.split(source_file)
		target_name = source_name
	return source_file, source_path, source_name, target_name

#f1结果为真时，将data经过f2进行转换
#lambda x: isinstance(x, str), lambda x: x.decode('utf-8')
#lambda x: isinstance(x, unicode), lambda x: x.encode('utf-8')
def convert(data, f1, f2):
	if f1(data):
		data = f2(data)
	elif isinstance(data, tuple):
		data = list(data)
		for n, v in enumerate(data):
			data[n] = convert(v, f1, f2)
		data = tuple(data)
	elif isinstance(data, list):
		for n, v in enumerate(data):
			data[n] = convert(v, f1, f2)
	elif isinstance(data, dict):
		for k, v in data.items():
			del data[k]
			data[convert(k, f1, f2)] = convert(v, f1, f2)
	return data

#转换为utf-8编码
def convert_encode(data, code):
	return convert(data, lambda x: isinstance(x, unicode), lambda x: x.encode(code))

#转换为unicode编码
def convert_decode(data, code):
	return convert(data, lambda x: isinstance(x, str), lambda x: x.decode(code))

#用method方法对输入参数编码	
def code(method):
	def run_func(func):
		def run(*argv, **kwargv):
			return func(*convert_encode(list(argv), method), **convert_encode(kwargv, method)) #不用list新建就不会编解码
		run.__name__ = func.__name__
		return run
	return run_func

#将为数字的字符串转换为数字
def convert_int(data):
	return convert(data, lambda x: 'isdigit' in dir(x) and x.isdigit(), int)


#计算文件md5
def get_md5(source_file):
	md5 = hashlib.md5()
	with open(convert_decode(source_file, 'utf-8'), 'rb') as fp:
		while 1:
			data = fp.read(1024 * 1024)
			md5.update(data)
			if not data: break	
	return md5.hexdigest()

#获取文件名称，名称#时间#md5#大小
@error_log('')
def get_target_name(source_file):
	size = os.path.getsize(source_file)
	md5 = get_md5(source_file)
	clock = time.strftime('%Y-%m-%d@%H-%M-%S', time.localtime())
	#return '%s#%s#%s#%s' % (encode_file(source_file), clock, md5, size)
	return '%s#%s#%s' % (clock, md5, size)


#重新封装系统的walk
def walk(target_path):
	#传入参数为utf-8，中文字符才会是gbk，传入参数为unicode，中文字符也为unicode
	target_list = os.walk(target_path)
	for target_file in target_list:
		yield convert(target_file, lambda x: type(x) not in (tuple, list, dict), lambda x: x.replace('\\', '/'))

#判断data是否匹配到re_list正则表达式中的一个
def search(re_list, data):
	if not re_list: return False
	for r in re_list:
		try:
			if re.search(r, data): return True
		except: pass
	return False