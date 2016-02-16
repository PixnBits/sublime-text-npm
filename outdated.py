import sublime, sublime_plugin

from .command import NpmCommand

class NpmOutdated(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		self.run_npm_and_show(['outdated'])
