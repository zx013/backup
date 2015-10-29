#-*- coding:utf-8 -*-
#目前支持若干个文件的备份，相关设置在backup.conf中配置

#异常处理
#微软office支持
#目录备份
#备份恢复
import thread

from Config import Config
from Windows import Windows
from log import debug_log, write_log, error_log, sync

def Backup():
	def backup(self, handle, source_file, target_path):
		handle.upload([source_file, target_name], target_path)
		file_list = handle.show(target_path) #按时间顺序排列
		handle.delete(file_list[self.config['basic'][handle.get_config_type()]['number']:])
	
	def backup_file(self, handle, source_file, target_path):
		#检查备份的目标路径
		if not handle.check_path(target_path):
			handle.mkdir(target_path)
		else:
			#有则检查路径下的内容，删除非备份文件
			file_list = handle.show(target_path)
			#获取目标路径中最后的备份文件状态，md5等
			#比较文件状态
				#相等则跳过
				#不相等则备份
		#备份完成检查备份数量
	
	def backup_dir(self, handle):
		pass

	def run(self):
		#读取配置
		self.config = Config()
		self.config.read_config()
		
		#自动保存文档
		windows = Windows(self.config['basic']['base']['save'])
		thread.start_new_thread(windows.save_file, ())
		
		#硬盘备份
		if self.config['basic']['disk']['enable'] == 'on':
			pass
	
		#百度云备份
		if self.config['basic']['baidu']['enable'] == 'on':
			pass

if __name__ == '__main__':
	backup = Backup()
	backup.run()