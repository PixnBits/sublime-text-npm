import subprocess, json
import sublime, sublime_plugin

from npm.command import NpmCommand

class NpmListCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		self.run_npm(['list', '--depth', '0'])

class NpmListDeepCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		self.run_npm(['list'])
