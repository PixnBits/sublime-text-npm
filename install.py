import sublime, sublime_plugin

from .command import NpmCommand

class NpmInstall(NpmCommand):
	def prompt_for_package_name(self, on_done, on_change=None, on_cancel=None):
		selected_text = []
		window = sublime.active_window()
		active_view = window.active_view()
		for region in active_view.sel():
			if not region.empty():
				selected_text.append(active_view.substr(region))
		selected_text = ' '.join(selected_text).replace('\n',' ').replace('\r',' ')
		window.show_input_panel('install package', selected_text, on_done, on_change, on_cancel)

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