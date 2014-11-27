import sublime, sublime_plugin

from .command import NpmCommand

class NpmInstall(NpmCommand):
	def prompt_for_package_name(self, on_done, on_change=None, on_cancel=None):
		#sublime.status_message("npm install...something")
		#self.view.insert(edit, 0, "Hello, World!")
		window = sublime.active_window()
		#window.show_quick_panel(['hi there','how\s the melting going?'], None, sublime.MONOSPACE_FONT)
		#window.show_quick_panel([], None, sublime.MONOSPACE_FONT)
		#window.show_input_panel(caption, initial_text, on_done, on_change, on_cancel)
		window.show_input_panel('install package', '', on_done, on_change, on_cancel)


class NpmInstallCommand(NpmInstall, sublime_plugin.TextCommand):
	def run(self, edit):
		self.prompt_for_package_name(self.install_done)

	def install_done(self, package_name):
		# there might be >1 package name specified, split() is whitespace
		self.run_npm_and_show(['install']+package_name.split())


class NpmInstallSaveCommand(NpmInstall, sublime_plugin.TextCommand):
	def run(self, edit):
		self.prompt_for_package_name(self.install_done)

	def install_done(self, package_name):
		self.run_npm_and_show(['install']+package_name.split()+['--save'])


class NpmInstallSaveDevCommand(NpmInstall, sublime_plugin.TextCommand):
	def run(self, edit):
		self.prompt_for_package_name(self.install_done)

	def install_done(self, package_name):
		self.run_npm_and_show(['install']+package_name.split()+['--save-dev'])