import sublime, sublime_plugin

from .command import NpmCommand
from .list import NpmList

#TODO: DRY this up

#class NpmRm(NpmCommand):

class NpmRmCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		# need only `list` but use show helper function too
		NpmList.list_and_show(self, 0, self.show_edit_options)

	def show_edit_options(self, package_name_index):
		if package_name_index < 0:
			return
		selected_package_name = self.package_names[package_name_index]
		if isinstance(selected_package_name, str):
			# remove specific package
			return_code, out, err = self.run_npm(['rm', selected_package_name])
			if 0 is return_code:
				sublime.status_message("Package `"+selected_package_name+"` removed/uninstalled")
			else:
				self.show_npm_output([return_code, out, err])
		elif True == selected_package_name:
			# remove all packages
			self.run_npm_and_show(['rm'])
		#else:
			#nothing selected, do nothing
		return selected_package_name

class NpmRmSavedCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		# need only `list` but use show helper function too
		NpmList.list_and_show(self, 0, self.show_edit_options)

	def show_edit_options(self, package_name_index):
		if package_name_index < 0:
			return
		selected_package_name = self.package_names[package_name_index]
		if isinstance(selected_package_name, str):
			# remove specific dependency
			# per https://github.com/npm/npm/issues/2452 we use the same `--save-*` flags
			return_code, out, err = self.run_npm(['uninstall', '--save', '--save-dev', '--save-optional', selected_package_name])
			if 0 is return_code:
				sublime.status_message("Package `"+selected_package_name+"` removed/uninstalled")
			else:
				self.show_npm_output([return_code, out, err])
		elif True == selected_package_name:
			# remove all dependencies
			self.run_npm_and_show(['uninstall', '--save', '--save-dev', '--save-optional'])
		#else:
			#nothing selected, do nothing
		return selected_package_name