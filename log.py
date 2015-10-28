#-*- coding:utf-8 -*-
#日志模块，日志默认为info和error，在目录tmp下
#set_log设置日志参数
#debug_log打印日志
#write_log将日志写入文件
#check_input检查输入参数的装饰器
#error_log捕获异常的装饰器，出现异常时返回默认值
import os
import sys
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

#检查传入值是否在一定范围内
#@check_input(min=1, max=10, inside=(1, 2), outside=(0,))
#input_data = {'min': 1, 'max': 10, 'inside': (1, 2), 'outside': (0,)}
#base, 存在时超出范围则返回base，不存在时超出范围则默认执行
#min, 值最小为1
#max, 值最大为10
#inside, 值在(1, 2)之中
#outside, 值不在(0,)之中
def check_input(**input_data):
	def run_func(func):
		base_check = input_data.has_key('base')
		base_data = input_data.get('base')
		min_data = input_data.get('min')
		max_data = input_data.get('max')
		inside_data = input_data.get('inside')
		outside_data = input_data.get('outside')
		def run(*argv, **kwargv):
			write_msg = []
			val = set(argv) | set([val for key, val in kwargv.items()])
			if min_data is not None and min(val) < min_data:
				write_msg.append('min=%s' % str(min_data))
			if max_data is not None and max(val) > max_data:
				write_msg.append('max=%s' % str(max_data))
			if inside_data is not None and val | set(inside_data) != set(inside_data):
				write_msg.append('inside=%s' % str(inside_data))
			if outside_data is not None and val & set(outside_data) != set():
				write_msg.append('outside=%s' % str(outside_data))
			if len(write_msg) > 0:
				try: raise Exception
				except: f = sys.exc_info()[2].tb_frame.f_back
				log = '[%s -> %s] %s [%s] - parameter warning, argv=%s, kwargv=%s: ' % (f.f_code.co_filename, func.__name__, time.strftime('%Y-%m-%d %X', time.localtime()), str(f.f_lineno), str(argv), str(kwargv))
				for msg in write_msg: write_log_inside('info', '%s%s' % (log, msg))
				if base_check: return base_data
			return func(*argv, **kwargv)
		run.__name__ = func.__name__
		return run
	return run_func

#tp为True时，将列表，字典等出现的字符串全部转换为unicode
def convert(data, tp=True):
	if isinstance(data, str):
		if tp: data = data.decode('utf-8')
	elif isinstance(data, unicode):
		if not tp: data = data.encode('utf-8')
	elif isinstance(data, list):
		for n, v in enumerate(data):
			data[n] = convert(v, tp)
	elif isinstance(data, dict):
		for k, v in data.items():
			del data[k]
			data[convert(k, tp)] = convert(v, tp)
	return data

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

@error_log()
@check_input(base='abc', min=2, max=0, inside=(2, 3), outside=(1, 2))
def fun1(*argv, **kwargv):
	print argv, kwargv
	raise

if __name__ == '__main__':
	print fun1(1)