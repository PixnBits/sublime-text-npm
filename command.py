import subprocess, json, os
import sublime, sublime_plugin
from .cli import CLI

class NpmCommand(CLI):
	def parse_json(self, json_string):
		#json.loads(str(json_string))
		return json.loads(json_string)

	def get_dir_name(self):
		active_file_name = self.view.file_name()
		if not active_file_name:
			sublime.error_message("Please open a file in your npm project so npm knows where to run")
			return None
		return os.path.dirname(active_file_name)

	def run_npm(self, commands):
		dir_name = self.get_dir_name()
		if not dir_name:
			return [-1, "", "Please open a file in your npm project so npm knows where to run"]
		return_code, out, err = self.execute(commands, dir_name)
		# return the process result
		return [return_code, out, err]

	def output_textarea(self, message):
		window = sublime.active_window()
		output_view = window.get_output_panel("textarea")
		window.run_command("show_panel", {"panel": "output.textarea"})
		output_view.set_read_only(False)
		# sections commented out are the sublime v2 way, AFAIK they're the only bits preventing v2 compatibility
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

	# adapted from https://github.com/kemayo/sublime-text-git/blob/64ec693f43b4803690e5d92852e41975f3b8855a/git.py#L199
	def scratch(self, output=False, title=False):
		window = sublime.active_window()
		scratch_file = window.new_file()
		if title:
			scratch_file.set_name(title)
		scratch_file.set_scratch(True)
		if output:
			self.scratch_append(scratch_file, output)
		scratch_file.set_read_only(True)
		return scratch_file

	def scratch_append(self, scratch_file, output):
		window = sublime.active_window()
		window.run_command( "npm_scratch_append", {"scratch_file_id":scratch_file.id(), "output":output} )

	# can't find a sublime API call for this
	def get_view_by_id(self, vid):
		if not vid:
			return None
		for window in sublime.windows():
			for view in window.views():
				if view.id() == vid:
					return view
		return None

# http://stackoverflow.com/a/20808586
class NpmScratchAppendCommand(sublime_plugin.TextCommand):
	def run(self, edit, scratch_file_id, output):
		scratch_file = NpmCommand.get_view_by_id(self, scratch_file_id)
		if scratch_file:
			scratch_file.set_read_only(False)
			scratch_file.insert(edit, scratch_file.size(), output)
			scratch_file.set_read_only(True)


# list of ScratchWorker instances
scratch_workers = []

class ScratchWorker(NpmCommand, sublime_plugin.EventListener):

	def __init__(self):
		# add us to the list
		global scratch_workers
		scratch_workers.append(self)

	def __del__(self):
		# remove us from the list
		global scratch_workers
		if self in scratch_workers:
		  scratch_workers.remove(self)

	def create_process(self, command_list, dir_name):
		self.set_scratch_file(self.scratch(None, "npm "+ (" ".join(command_list)) ))
		self.set_process(self.execute_long_running(command_list, dir_name, self.update_scratch_output, self.update_scratch_status))
		self.update_scratch_status()

	def set_process(self, cli_long):
		self.process = cli_long

	def set_scratch_file(self, scratch_file):
		self.scratch_file = scratch_file
		self.scratch_name = scratch_file.name()

	def update_scratch_output(self, message):
		self.scratch_append(self.scratch_file, message)

	def update_scratch_status(self, status=None):
		name = self.scratch_name
		if 0 == status:
			# successful exit
			name += " [Finished]"
		elif not status:
			# running
			name += " [Running]"
		else:
			# error exit
			name += " [Error]"
		self.scratch_file.set_name(name)

	def on_close(self, view):
		# static method, self isn't actually an instance of ScratchWorker
		# find a worker in scratch_workers that has the view closed
		# I'm no Python guru, and Python's utilities to do this are full of wats
		# hence the debug messages are commented out, rather than removed
		#print("ScratchWorker on_close")
		focused_worker = None
		global scratch_workers
		for worker in scratch_workers:
			if not hasattr(worker, 'scratch_file'):
				continue
			if worker.scratch_file == view:
				focused_worker = worker
				#print('found our worker')
				break

		if not focused_worker:
			#print("closed view not in list")
			return

		#print("view closed "+str(focused_worker))
		# stop the process
		focused_worker.stop()
		# remove ourself from the scratch_workers list
		scratch_workers.remove(focused_worker)

	def stop(self):
		self.process.stop();
