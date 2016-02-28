import re, os
import sublime, sublime_plugin

from .command import NpmCommand, ScratchWorker

class NpmRunArbitraryCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		window = sublime.active_window()
		window.show_input_panel('npm command:', '', self.have_command_text, None, None)

	def have_command_text(self, command_text):
		# http://en.wikipedia.org/wiki/Shell_injection#Shell_injection
		# maybe use shlex.quote instead?
		# https://docs.python.org/3/library/shlex.html#shlex.quote

		# strip off statement seperators
		# `;` for *nix, `&`, `&&` Windows
		single_command = re.sub(";|&"," ",command_text)
		# strip off other known
		single_command = re.sub("`|\$|\(|\)|\||\<|\>"," ",command_text)
		# strip off leading npm, if present
		single_command = re.sub("^npm\s","",single_command)
		if len(single_command) < 1:
			sublime.status_message("no npm command to run")
			return

		active_file_name = self.view.file_name()
		if not active_file_name:
			return [-1, "", "Please open a file in your npm project so npm knows where to run"]
		dir_name = os.path.dirname(active_file_name)

		# execute_long_running(self, command, cwd, on_readline):
		command_list = re.split("\s+", single_command)
		worker = ScratchWorker()
		worker.create_process(command_list, dir_name)
