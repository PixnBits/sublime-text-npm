import re
import sublime, sublime_plugin

from .command import NpmCommand

class NpmList(NpmCommand):
	def list(self, depth=0):
		command = ['list', '--json', 'true']
		if isinstance(depth, int):
			if depth < 0:
				depth = 0
			command.append('--depth')
			command.append(str(depth))
		proc_code, list_json_text, list_err = self.run_npm(command)
		# remove non-json lines from list_json_text
		# such as `npm ERR! missing: hapi@^6.5.1, required by your-project@0.0.0`
		npm_line = re.compile("(\r|\n)npm.+?(\r|\n)")
		while re.search(npm_line, list_json_text):
			list_json_text = re.sub(npm_line, '\n', list_json_text)
		list_json_text = re.sub("(\n|\r)npm$", '\n', list_json_text)
		if list_json_text:
			list_json = self.parse_json(list_json_text)
			# parse into a dict of key=pkg_name, val=version
			pkg_list = {}
			NpmList.add_to_dep_list(self, pkg_list, list_json)
			return pkg_list
		elif list_err:
			return list_err
		else:
			return None

	def add_to_dep_list(self, pkg_list, list_json):
		if 'dependencies' in list_json:
			dependencies = list_json['dependencies']
			for dep in dependencies:
				dep_data = dependencies[dep]
				if 'version' in dep_data:
					pkg_list[dep] = dep_data['version']
				elif 'required' in dep_data:
					# TODO: show message to user (req'd packages not installed), maybe in status bar?
					pkg_list[dep] = dep_data['required']
				else:
					pkg_list[dep] = True
				if 'dependencies' in dep_data:
					self.add_to_dep_list(pkg_list, dep_data)
		return pkg_list

	def list_and_show(self, depth=0, on_done=None):
		pkg_list = self.list(depth)
		self.package_names = []
		packages = []
		for pkg in pkg_list:
			self.package_names.append(pkg)
			packages.append([pkg, pkg_list[pkg]])
		if len(packages) < 1:
			self.package_names.append(False)
			packages.append('(None)');
		#show quick panel
		window = sublime.active_window()
		window.show_quick_panel(packages, on_done, sublime.MONOSPACE_FONT)

class NpmListCommand(NpmList, sublime_plugin.TextCommand):
	def run(self, edit):
		self.list_and_show(0, self.show_edit_options)

	def show_edit_options(self, package_name_index):
		# TODO
		sublime.status_message("package_name_index: "+str(package_name_index))

class NpmListDeepCommand(NpmList, sublime_plugin.TextCommand):
	def run(self, edit):
		self.list_and_show(None)
