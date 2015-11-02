#-*- coding:utf-8 -*-
#日志模块，日志默认为info和error，在目录tmp下
#set_log设置日志参数
#debug_log打印日志
#write_log将日志写入文件
#error_log捕获异常的装饰器，出现异常时返回默认值
import os
import sys
import hashlib
import re
import time

global log_list
log_list = {}

def set_log(name, path, data):
	global log_list
	if not os.path.exists(path):
		os.mkdir(path)
	log_list[name] = {'path': '%s/%s' % (path, name), 'data': data}

#import时设置
set_log('info', 'tmp', 10)
set_log('error', 'tmp', 0)

#检查日志
def check_log(name):
	global log_list
	size = log_list.get(name, {}).get('data', 10) * 1024 * 1024
	if size > 0:
		path = str(log_list.get(name, {}).get('path'))
		try: base_size = os.path.getsize(path) #目录不存在会出错
		except: base_size = 0
		if base_size > size: os.remove(path)

def debug_log(log):
	print log

def write_log_inside(name, log):
	path = log_list.get(name, {}).get('path')
	if path is None: return
	check_log(name)
	if os.path.exists(str(path)): tp = 'a' #存在则追加，不存在则创建
	else: tp = 'w'
	
	#在2.5之前的版本没有with
	try: fp = open(path, tp)
	except: return #打开失败直接返回
	try: fp.write('%s\r\n' % log) #写入失败
	except: pass
	fp.close()

def write_log(name, log):
	try: raise Exception
	except: f = sys.exc_info()[2].tb_frame.f_back
	log = '[%s -> %s] %s [%s] - %s' % (f.f_code.co_filename, f.f_code.co_name, time.strftime('%Y-%m-%d %X', time.localtime()), str(f.f_lineno), str(log))
	write_log_inside(name, log)

def error_log(base=None):
	def run_func(func):
		def run(*argv, **kwargv):
			try:
				return func(*argv, **kwargv)
			except Exception, ex:
				try: raise Exception
				except: f = sys.exc_info()[2].tb_frame.f_back
				#logging模块2.4版本无法获取函数名称
				#获取的函数名称为func的函数名称，行号为调用func所在的位置，用logging模块获取的行号为调用debug等函数所在的位置，多个装饰器时第一个装饰器获取的行号正确，其它的为装饰器中调用函数的行号
				log = '[%s -> %s] %s [%s] - %s' % (f.f_code.co_filename, func.__name__, time.strftime('%Y-%m-%d %X', time.localtime()), str(f.f_lineno), str(ex))

				write_log_inside('error', log)
				debug_log(func.__name__ + ' : ERROR')
				debug_log('Exception : ' + str(ex))
				return base
		run.__name__ = func.__name__
		return run
	return run_func
	
def sync(lock):
	def run_func(func):
		def run(*argv, **kwargv):
			lock.acquire()
			try:
				return func(*argv,**kwargv)
			finally:
				lock.release()
		run.__name__ = func.__name__
		return run
	return run_func


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
		
def code(method, enable):
	def run_func(func):
		def run(*argv, **kwargv):
			if enable: convert = convert_encode
			else: convert = convert_decode
			return func(*convert(list(argv), method), **convert(kwargv, method)) #不用list新建就不会编解码
		run.__name__ = func.__name__
		return run
	return run_func

#将为数字的字符串转换为数字
def convert_int(data):
	return convert(data, lambda x: 'isdigit' in dir(x) and x.isdigit(), int)
	
#将文件名中字符进行转义，输入为unicode则转换为utf-8再转义
def encode_file(s):
	return ''.join(map(lambda x: x if 'a' <= x <= 'z' or 'A' <= x <= 'Z' else hex(ord(x)).replace('0x', '%'), s))

#根据文件转义字符串恢复文件名，输出为utf-8则转换为unicode
def decode_file(s):
	return ''.join([s[0]] + map(lambda x: '%s%s' % (chr(int(x[:2], 16)), x[2:]), s.split('%')[1:]))

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
	source_encode = convert_decode(source_file, 'utf-8')
	size = os.path.getsize(source_encode)
	md5 = get_md5(source_encode)
	clock = time.strftime('%Y-%m-%d@%H-%M-%S', time.localtime())
	return '%s#%s#%s#%s' % (encode_file(source_file), clock, md5, size)

#重新封装系统的walk
def walk(target_path):
	target_list = os.walk(target_path)
	for target_file in target_list:
		target_file = convert_encode(convert_decode(target_file, 'gbk'), 'utf-8')
		yield convert(target_file, lambda x: type(x) not in (tuple, list, dict), lambda x: x.replace('\\', '/'))

#判断data是否匹配到re_list正则表达式中的一个
def search(re_list, data):
	for r in re_list:
		try:
			if re.search(r, data): return True
		except: pass
	return False
