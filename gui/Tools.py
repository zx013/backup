#-*- coding:utf-8 -*-
from functools import wraps


def unpack(**kwargs):
	return map(dict, zip(*[[(k, v) for v in vs] for k, vs in kwargs.items()]))

def apply_insert(widget_class):
	def run_func(func):
		@wraps(func)
		def run(self, *args, **kwargs):
			ret = func(self, *args, **kwargs)
			for kwarg in unpack(**kwargs): #根据提供的参数插入子节点
				widget = widget_class()
				self.add_widget(widget)
				widget_func = getattr(widget, func.__name__, None)
				if widget_func:
					widget_func(**kwarg)
			return ret
		return run
	return run_func

#提供的参数少于节点数，将最后一个参数应用到所有节点
#提供的参数多于节点数，将最后一个参数应用到当前节点
def apply_delete(func):
	@wraps(func)
	def run(self, *args, **kwargs):
		ret = func(self, *args, **kwargs)
		unpack_child = self.children[::-1]
		unpack_kwargs = unpack(**kwargs)
		if len(unpack_kwargs) > len(unpack_child):
			delete_args(self, **unpack_kwargs[-1])
		else:
			if len(unpack_kwargs) < len(unpack_child):
				unpack_kwargs += [unpack_kwargs[-1]] * (len(unpack_child) - len(unpack_kwargs))
			for child, kwarg in zip(unpack_child, unpack_kwargs): #children的顺序是相反的
				child_func = getattr(child, func.__name__, None)
				if child_func: #子控件中存在该方法
					child_func(**kwarg)
		return ret
	return run


#将**kwargs依次应用到children中
def apply_walk(func):
	@wraps(func)
	def run(self, *args, **kwargs):
		ret = func(self, *args, **kwargs)
		unpack_child = self.children[::-1]
		unpack_kwargs = unpack(**kwargs)
		if len(unpack_kwargs) > len(unpack_child):
			insert_args(self, **unpack_kwargs[-1])
		for child, kwarg in zip(unpack_child, unpack_kwargs): #children的顺序是相反的
			child_func = getattr(child, func.__name__, None)
			if child_func: #子控件中存在该方法
				child_func(**kwarg)
		return ret
	return run

#将**kwargs中的数据转换为类中的属性
def insert_args(self, **kwargs):
	for key, value in kwargs.items():
		setattr(self, key, value)

#属性和键值相等或属性在键值中时移除该节点
def delete_args(self, **kwargs):
	for key, value in kwargs.items():
		try:
			if getattr(self, key) == value or getattr(self, key) in value:
				self.parent.remove_widget(self)
				return
		except:
			pass