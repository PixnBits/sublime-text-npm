import subprocess, json, os
import sublime, sublime_plugin
from .cli import CLI

class NpmCommand(CLI):
	def parse_json(self, json_string):
		#json.loads(str(json_string))
		return json.loads(json_string)

	def run_npm(self, commands):
		active_file_name = self.view.file_name()
		if not active_file_name:
			return [-1, "", "Please open a file in your npm project so npm knows where to run"]
		dir_name = os.path.dirname(active_file_name)
		return_code, out, err = self.execute(commands, dir_name)
		# return the process result
		return [return_code, out, err]

	def output_textarea(self, message):
		window = sublime.active_window()
		output_view = window.get_output_panel("textarea")
		window.run_command("show_panel", {"panel": "output.textarea"})
		output_view.set_read_only(False)
		# sections commented out are the sublime v2 way, AFAIK they're the only bits preventing v2 compatability
		# edit = output_view.begin_edit()
		# output_view.insert(edit, output_view.size(), "Hello, World!")
		output_view.run_command("append", {"characters": message})
		# output_view.end_edit(edit)
		output_view.set_read_only(True)
		# return the process result

	def show_npm_output(self, output):
		return_code, out, err = output
		# TODO: pretty-fy the feedback to the user...err OR out show? npm warnings enough to show err? even use output panel?
		message = ""
		if out:
			message = message + "Out: " + out
		if err:
			message = message + "\nErr: " + err
		#message = "Out: "+out+"\nErr: "+err
		#show results
		self.output_textarea(message)

	def run_npm_and_show(self, commands):
		self.show_npm_output(self.run_npm(commands))
