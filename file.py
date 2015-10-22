#-*- coding:utf-8 -*-
from log import debug_log, write_log, error_log, sync


#write_log('info', 'delete %s' % file_name)
#class_name, func_name, *argv

#备份流程，设定同一框架，根据不同备份类型创建对应的备份接口

#检查备份路径，不存在则创建
#获取备份路径下的文件列表，检查是否为备份文件
#删除不是备份生成的文件
#检查目标文件创建时间大小等参数，与备份文件比较，确定是否需要备份
#需要备份时，进行备份
#获取备份路径下的文件列表，删除超出范围的备份文件

class Disk:
	#查看文件，按文件名排序
	def show(self):
		return os.listdir(file_setting['path'])
	
	#比较备份文件和目标文件
	def compare(self, in_file, out_file):
		stat1 = os.stat(in_file)
		stat2 = os.stat(out_file)
		if stat1[-2] != stat2[-2] or stat1[:-3] != stat2[:-3]: return False

		return True
	
	#创建目录
	def mkdir(self, path):
		os.mkdir(path)

	#删除文件
	def delete(self, file_name):
		os.remove('%s%s' % (file_setting['path'], file_name))
		
	#备份文件
	def upload(self, in_file, out_file):
		os.system('copy /Y %s %s 1>nul' % (in_file, out_file))

	#恢复文件
	def download(self):
		pass