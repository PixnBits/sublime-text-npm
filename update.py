import sublime, sublime_plugin

from .command import NpmCommand
from .list import NpmList

class NpmUpdateCommand(NpmCommand, sublime_plugin.TextCommand):
	def run(self, edit):
		dependencies = NpmList.list(self, 0)
		if isinstance(dependencies, dict) and len(dependencies.keys()) > 0:
			self.package_names = [True]
			self.package_titles = ['Update All']
			dependency_names = dependencies.keys()
			for dependency_name in dependency_names:
				dep_ver = dependencies[dependency_name]
				self.package_names.append(dependency_name)
				self.package_titles.append(dependency_name + " ("+dep_ver+")")
		else:
			# no dependencies found
			self.package_names = [False]
			self.package_titles = ['(No Packages Found)']
		window = sublime.active_window()
		window.show_quick_panel(self.package_titles, self.update_package, sublime.MONOSPACE_FONT)

	def update_package(self, selection):
		selected_package_name = self.package_names[selection]
		#self.output_textarea("selection? "+str(selected_package_name))
		if isinstance(selected_package_name, str):
			# update specific dependency
			return_code, out, err = self.run_npm(['update', selected_package_name])
			if 0 is return_code:
				sublime.status_message("Package `"+selected_package_name+"` up to date")
			else:
				self.show_npm_output([return_code, out, err])
		elif True == selected_package_name:
			# update all dependencies
			self.run_npm_and_show(['update'])
		#else:
			#nothing selected, do nothing
		selected_package_name
