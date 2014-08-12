import sublime_plugin

from .command import NpmCommand

class NpmListCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		self.show_npm_output(self.list_direct_packages())

	def list_direct_packages(self):
		return self.run_npm(['list', '--depth', '0'])

	def list_direct_packages_data(self):
		code, json_str, err = self.run_npm(['list', '--json', 'true'])
		return self.parse_json(json_str)

class NpmListDeepCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		self.run_npm_and_show(['list'])
