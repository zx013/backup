#-*- coding:utf-8 -*-

class Base:
	@classmethod
	def isdir(self, target_path):
		return os.path.isdir(target_path)
	
	#备份时间是否是目录
	def restore_isdir(self, target_path):
		return len(self.show(target_path)[0])

	@classmethod
	def walk(self, target_path):
		target_dir, target_file = self.show(target_path)
		yield (target_path, target_dir, target_file)
		for path in target_dir:
			for g in self.walk(path):
				yield g
				
	def restore_walk(self, target_path):
		target_dir, target_file = self.show(target_path)
		backup_dir = []
		backup_file = []
		for path in target_dir:
			#该目录下全部为文件，即对应备份的文件，该目录不遍历
			if len(self.show(path)[0]):
				backup_dir.append(path)
			else:
				backup_file.append(path)
		target_dir, target_file = backup_dir, backup_file
		yield (target_path, target_dir, target_file)
		for path in target_dir:
			for g in self.restore_walk(path):
				yield g