#-*- coding:utf-8 -*-
from functools import wraps


def unpack(**kwargs):
	return map(dict, zip(*[[(k, v) for v in vs] for k, vs in kwargs.items()]))

def apply_insert(widget_class):
	def run_func(func):
		@wraps(func)
		def run(self, *args, **kwargs):
			ret = func(self, *args, **kwargs)
			for kwarg in unpack(**kwargs): #根据提供的参数插入子控件
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
		unpack_child = self.children[::-1]
		unpack_kwargs = unpack(**kwargs)
		if len(unpack_kwargs) > len(unpack_child):
			apply_args(self, **unpack_kwargs[-1])
		for child, kwarg in zip(unpack_child, unpack_kwargs): #children的顺序是相反的
			child_func = getattr(child, func.__name__, None)
			if child_func: #子控件中存在该方法
				child_func(**kwarg)
		return ret
	return run

#将**kwargs中的数据转换为类中的属性
def apply_args(self, **kwargs):
	for key, value in kwargs.items():
		setattr(self, key, value)