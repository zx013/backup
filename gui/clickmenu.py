from kivy.logger import Logger
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty


class ClickMenu(GridLayout):
    attach_to = ObjectProperty(None)
    _window = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self._parent = None
        super(ClickMenu, self).__init__(**kwargs)

    def _search_window(self):
        # get window to attach to
        window = None
        if self.attach_to is not None:
            window = self.attach_to.get_parent_window()
            if not window:
                window = self.attach_to.get_root_window()
        if not window:
            from kivy.core.window import Window
            window = Window
        return window

    def open(self, *largs):
        if self._window is not None:
            Logger.warning('ModalView: you can only open once.')
            return self
        # search window
        self._window = self._search_window()
        if not self._window:
            Logger.warning('ModalView: cannot open view, no window found.')
            return self
        self._window.add_widget(self)

        return self

    def dismiss(self, *largs, **kwargs):
        if self._window is None:
            return self
        self._window.remove_widget(self)
        self._window = None
        return self
