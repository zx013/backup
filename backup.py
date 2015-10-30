#-*- coding:utf-8 -*-
#目前支持若干个文件的备份，相关设置在backup.conf中配置

#异常处理
#微软office支持
#目录备份
#备份恢复
import thread

from Config import Config
from Windows import Windows
from log import debug_log, write_log, get_target_name

class Backup():
	def backup(self, handle, source_file, target_path):
		target_name = get_target_name(source_file)
		handle.upload((source_file, target_name), target_path)
		target_list = handle.show(target_path) #按时间顺序排列
		handle.delete(target_list[self.config.get('basic', handle.get_config_type(), 'number'):])
	
	def backup_file(self, handle, source_file, target_path):
		#检查备份的目标路径
		if not handle.check_path(target_path):
			handle.mkdir(target_path)
		else:
			#有则检查路径下的内容，删除非备份文件
			source_encode = encode_file(source_file)
			target_list = handle.show(target_path)
			target_insert = [] #保留的文件
			target_delete = [] #删除的文件
			for target_file in target_list:
				if source_encode in target_file:
					target_insert.append(target_file)
				else:
					target_delete.append(target_file)
			handle.delete(target_delete)
			
			target_list = target_insert
			if len(target_list):
				source_stat = get_target_name(source_file).split('#')
				target_stat = target_list[0].split('#')
				if source_stat[0] == target_stat[0] and source_stat[2:3] == target_stat[2:3]:
					#目录不为空且最新的备份文件与源文件相同时不备份
					return
		backup(handle, source_file, target_path)

	
	def backup_dir(self, handle):
		pass

	def run(self):
		#读取配置
		self.config = Config()
		self.config.read_config()
		if not self.config.check_config(): return
		
		print self.config.config
		
		#自动保存文档
		windows = Windows(self.config.get('basic', 'base', 'save'))
		thread.start_new_thread(windows.save_file, ())
		
		#硬盘备份
		if self.config.get('basic', 'disk', 'enable') == 'on':
			pass
	
		#百度云备份
		if self.config.get('basic', 'baidu', 'enable') == 'on':
			pass

if __name__ == '__main__':
	backup = Backup()
	backup.run()