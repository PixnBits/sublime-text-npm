import re, os
import sublime, sublime_plugin

from .command import NpmCommand

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
		worker = NpmRunArbitraryWorker()
		command_list = re.split("\s+", single_command)
		worker.set_scratch_file(self.scratch(None, "npm "+ (" ".join(command_list)) ))
		worker.set_process(self.execute_long_running(command_list, dir_name, worker.update_scratch_output, worker.update_scratch_status))
		worker.update_scratch_status()


# list of NpmRunArbitraryWorker instances
running_arbitrary_workers = []

class NpmRunArbitraryWorker(NpmCommand, sublime_plugin.EventListener):

	def __init__(self):
		# add us to the list
		global running_arbitrary_workers
		running_arbitrary_workers.append(self)

	def __del__(self):
		# remove us from the list
		global running_arbitrary_workers
		running_arbitrary_workers.remove(self)

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
		# static method, self isn't actually an instance of NpmRunArbitraryWorker
		# find a worker in running_arbitrary_workers that has the view closed
		# I'm no Python guru, and Python's utilities to do this are full of wats
		# hence the debug messages are commented out, rather than removed
		#print("NpmRunArbitraryWorker on_close")
		focused_worker = None
		global running_arbitrary_workers
		for worker in running_arbitrary_workers:
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
		# remove ourself from the running_arbitrary_workers list
		running_arbitrary_workers.remove(focused_worker)

	def stop(self):
		self.process.stop();
