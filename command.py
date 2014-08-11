import subprocess, json
import sublime, sublime_plugin

class NpmCommand(object):
	def parse_json(self, json_string):
		json.loads(str(json_string))

	#TODO def find_npm(self)
		#find npm's bin path so we don't need to use `shell=True` with subprocess
		#self.npm_path = ...

	def run_npm(self, commands):
		file_name = self.view.file_name()
		sublime.status_message("file_name? "+str(file_name))
		#proc = subprocess.Popen(['echo','blue'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#proc = subprocess.Popen(['npm']+commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=file_name)
		#proc = subprocess.Popen([ 'cd', file_name,'\n;\n', 'npm']+commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=file_name)
		proc = subprocess.Popen([ 'dir' ], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=file_name)
		out, err = proc.communicate()
		return_code = proc.poll()
		# works: subprocess.call(['npm', 'version'], shell=True)
		#sublime.status_message("proc exited with code "+str(return_code))
		#show results
		window = sublime.active_window()
		output_view = window.get_output_panel("textarea")
		window.run_command("show_panel", {"panel": "output.textarea"})
		output_view.set_read_only(False)
		# edit = output_view.begin_edit()
		# output_view.insert(edit, output_view.size(), "Hello, World!")
		#output_view.run_command("append", {"characters": "Installing package '"+pkg+"'..."})
		output_view.run_command("append", {"characters": "Out: "+out.decode("utf-8")})
		#output_view.run_command("append", {"characters": "Out: "+self.parse_json(out)})
		output_view.run_command("append", {"characters": "Err: "+err.decode("utf-8")})
		# output_view.end_edit(edit)
		output_view.set_read_only(True)
		# return the process result
		return_code