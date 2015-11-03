#-*- coding:utf-8 -*-
import os
import re

from log import convert, convert_encode, convert_decode

def split(source_file):
	return os.path.split(source_file)

def isdir(source_file):
	return os.path.isdir(convert_decode(source_file, 'utf-8'))

#重新封装系统的walk
def walk(target_path):
	target_path = convert_decode(target_path, 'utf-8')
	target_list = os.walk(target_path)
	for target_file in target_list:
		target_file = convert_encode(convert_decode(target_file, 'gbk'), 'utf-8')
		yield convert(target_file, lambda x: type(x) not in (tuple, list, dict), lambda x: x.replace('\\', '/'))

#判断data是否匹配到re_list正则表达式中的一个
def search(re_list, data):
	if not re_list: return False
	for r in re_list:
		try:
			if re.search(r, data): return True
		except: pass
	return False