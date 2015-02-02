import re, os
import sublime, sublime_plugin

from .command import NpmCommand
from .run_arbitrary import NpmRunArbitraryWorker

class NpmRunTestCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		active_file_name = self.view.file_name()
		if not active_file_name:
			return [-1, "", "Please open a file in your npm project so npm knows where to run"]
		dir_name = os.path.dirname(active_file_name)

		# execute_long_running(self, command, cwd, on_readline):
		worker = NpmRunArbitraryWorker()
		command_list = ['test']
		worker.set_scratch_file(self.scratch(None, "npm "+ (" ".join(command_list)) ))
		worker.set_process(self.execute_long_running(command_list, dir_name, worker.update_scratch_output, worker.update_scratch_status))
		worker.update_scratch_status()
