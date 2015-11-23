#-*- coding:utf-8 -*-
from functools import wraps


def unpack(**kwargs):
	return map(dict, zip(*[[(k, v) for v in vs] for k, vs in kwargs.items()]))

def apply_insert(widget_class):
	def run_func(func):
		@wraps(func)
		def run(self, *args, **kwargs):
			ret = func(self, *args, **kwargs)
			for kwarg in unpack(**kwargs): #根据提供的参数创建子控件
				widget = widget_class()
				self.add_widget(widget)
				widget_func = getattr(widget, func.__name__, None)
				if widget_func:
					widget_func(**kwarg)
			return ret
		return run
	return run_func


#将**kwargs依次应用到children中
def apply_walk(func):
	@wraps(func)
	def run(self, *args, **kwargs):
		ret = func(self, *args, **kwargs)
		for child, kwarg in zip(self.children[::-1], unpack(**kwargs)): #children的顺序是相反的
			child_func = getattr(child, func.__name__, None)
			if child_func: #子控件中存在该方法
				child_func(**kwarg)
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