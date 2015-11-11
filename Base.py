#-*- coding:utf-8 -*-

class Base:
	@classmethod
	def walk(self, target_path):
		target_dir, target_file = self.show(target_path)
		yield (target_path, target_dir, target_file)
		for path in target_dir:
			for g in self.walk('%s/%s' % (target_path, path)):
				yield g