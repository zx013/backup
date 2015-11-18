#-*- coding:utf-8 -*-
from functools import wraps

def unpack(**kwargs):
	return map(dict, zip(*[[(k, v) for v in vs] for k, vs in kwargs.items()]))

#将**kwargs依次应用到children中
def apply_walk(func):
	@wraps(func)
	def run(self, *args, **kwargs):
		ret = func(self, *args, **kwargs)
		for child, kwarg in zip(self.children[::-1], unpack(**kwargs)): #children的顺序是相反的
			if getattr(child, func.__name__, None): #子控件中存在该方法
				eval('child.%s' % func.__name__)(**kwarg)
		return ret
	return run

#将**kwargs中的数据转换为类中的属性
def apply_args(func):
	@wraps(func)
	def run(self, *args, **kwargs):
		ret = func(self, *args, **kwargs)
		for key, value in kwargs.items():
				setattr(self, key, value)
		return ret
	return run