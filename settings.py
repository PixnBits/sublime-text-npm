# copied from sublime gulp
# https://github.com/NicoSantangelo/sublime-gulp/blob/6231c3c8181e1785f7ff3d297c18d842f03ff755/settings.py
# The MIT License (MIT)
#
# Copyright (c) 2014 Nicolás Santángelo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sublime

class Settings():
    def __init__(self):
        active_view = sublime.active_window().active_view()
        self.user_settings = sublime.load_settings("npm.sublime-settings")
        self.sources = [active_view.settings(), ProjectData(), self.user_settings]

    def get(self, key, default=None):
        return next((settings.get(key, default) for settings in self.sources if settings.has(key)), None)

    def get_from_user_settings(self, key, default=None):
        return self.user_settings.get(key, default)

    def has(self, key):
        return any(settings.has(key) for settings in self.sources)


class ProjectData():
    def __init__(self):
        self._project_data = sublime.active_window().project_data().get('Gulp', {}) if int(sublime.version()) >= 3000 else {}

    def get(self, key, default):
        return self._project_data.get(key, default)

    def has(self, key):
        return key in self._project_data
