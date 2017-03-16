import re, os
import sublime, sublime_plugin

from .command import NpmCommand, ScratchWorker

class NpmRunScript(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		# get the list of scripts
		(exit_code, run_list_json, err) = self.run_npm(['run', '--json'])
		if exit_code > 0:
			print(err)
			return
		run_list_raw = self.parse_json(run_list_json)
		# transform to sublime's API
		self.run_list = []
		for script_name in run_list_raw:
			self.run_list.append([script_name, run_list_raw[script_name]])
		# show the scripts to the user
		window = sublime.active_window()
		window.show_quick_panel(self.run_list, self.run_script)

	def run_script(self, selected_index):
		if selected_index == -1:
			return
		script_name = self.run_list[selected_index][0]
		dir_name = self.get_dir_name()
		if not dir_name:
			return
		worker = ScratchWorker()
		worker.create_process(['run', script_name], dir_name)
