#-*- coding:utf-8 -*-
#日志模块，日志默认为info和error，在目录tmp下
#set_log设置日志参数
#debug_log打印日志
#write_log将日志写入文件
#error_log捕获异常的装饰器，出现异常时返回默认值
import os
import sys
import hashlib
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

#f1结果为真时，将data经过f2进行转换
#lambda x: isinstance(x, str), lambda x: x.decode('utf-8')
#lambda x: isinstance(x, unicode), lambda x: x.encode('utf-8')
def convert(data, f1, f2):
	if f1(data):
		data = f2(data)
	elif isinstance(data, list):
		for n, v in enumerate(data):
			data[n] = convert(v, f1, f2)
	elif isinstance(data, dict):
		for k, v in data.items():
			del data[k]
			data[convert(k, f1, f2)] = convert(v, f1, f2)
	return data

#转换为utf-8编码
def convert_utf8(data):
	return convert(data, lambda x: isinstance(x, unicode), lambda x: x.encode('utf-8'))

#转换为unicode编码
def convert_unicode(data):
	return convert(data, lambda x: isinstance(x, str), lambda x: x.decode('utf-8'))

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
	with open(convert_unicode(source_file), 'rb') as fp:
		while 1:
			data = fp.read(1024 * 1024)
			md5.update(data)
			if not data: break	
	return md5.hexdigest()

#获取文件名称，名称#时间#md5#大小
@error_log('')
def get_target_name(source_file):
	source_file = convert_unicode(source_file)
	size = os.path.getsize(source_file)
	md5 = get_md5(source_file)
	clock = time.strftime('%Y-%m-%d@%H-%M-%S', time.localtime())
	return '%s#%s#%s#%s' % (encode_file(source_file), clock, md5, size)

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