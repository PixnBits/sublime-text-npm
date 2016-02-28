import re, os
import sublime, sublime_plugin

from .command import NpmCommand, ScratchWorker

class NpmRunTestCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		active_file_name = self.view.file_name()
		if not active_file_name:
			return [-1, "", "Please open a file in your npm project so npm knows where to run"]
		dir_name = os.path.dirname(active_file_name)

		# execute_long_running(self, command, cwd, on_readline):
		command_list = ['test']
		worker = ScratchWorker()
		worker.create_process(command_list, dir_name)
