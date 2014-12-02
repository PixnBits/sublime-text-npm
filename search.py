import re
import sublime, sublime_plugin

from .command import NpmCommand

class NpmSearch(NpmCommand):
	def prompt_for_package_name(self, on_done, on_change=None, on_cancel=None):
		selected_text = []
		window = sublime.active_window()
		active_view = window.active_view()
		for region in active_view.sel():
			if not region.empty():
				selected_text.append(active_view.substr(region))
		selected_text = ' '.join(selected_text).replace('\n',' ').replace('\r',' ')
		window.show_input_panel('search npm for', selected_text, on_done, on_change, on_cancel)


class NpmSearchCommand(NpmSearch, sublime_plugin.TextCommand):
	def run(self, edit):
		self.prompt_for_package_name(self.search_done)

	def search_done(self, package_name):
		#TODO show loading bar text
		#search_int, search_full_text, search_err = self.run_npm(['search', '--long', package_name])
		search_int, search_full_text, search_err = self.run_npm(['search', package_name])
		if search_err:
			self.output_textarea("search_err:\n"+search_err)
		elif search_full_text:
			search_lines = search_full_text.splitlines()
			# first two results may be search updating
			npm_http_request = re.compile("^npm http ")
			while npm_http_request.match(search_lines[0]):
				del search_lines[0]
			# find out how wide the columns are
			search_headers = re.split("(\\w+\\s+)", search_lines[0])
			del search_lines[0]; #remove column header quick
			# use widths to determine indices to split at
			column_indices = [0]
			for header in search_headers:
				header_len = len(header)
				if header_len > 0:
					column_indices.append(column_indices[-1]+header_len)
			print("column_indices: "+str(column_indices))
			# now build list of dicts containing results by column
			lines = []
			for search_line in search_lines:
				if npm_http_request.match(search_line):
					continue
				line = {}
				line['name'] = search_line[column_indices[0]:column_indices[1]].strip()
				line['description'] = search_line[column_indices[1]:column_indices[2]].strip()
				line['author'] = search_line[column_indices[2]:column_indices[3]].strip()
				line['date'] = search_line[column_indices[3]:column_indices[4]].strip()
				line['version'] = search_line[column_indices[4]:column_indices[5]].strip()
				line['keywords'] = search_line[column_indices[5]:column_indices[6]].strip()
				lines.append(line)
			# store package names if the user selects one (take actions with that package)
			self.package_names = []
			search_results = []
			for line in lines:
				self.package_names.append(line['name'])
				search_results.append([line['name'] + '(v'+line['version']+')',  line['description'], line['date']+', '+line['author'] ])
			# if there are no results, inform the user
			if len(search_results) < 1:
				search_results = ['(No Results)']
			# show our formatted results to the user
			window = sublime.active_window()
			window.show_quick_panel(search_results, self.show_package_commands, sublime.MONOSPACE_FONT)

	def show_package_commands(self, index):
		if index < 0 or len(self.package_names) < 1:
			return
		package_name = self.package_names[index]
		sublime.status_message("selected package "+package_name+" (TODO: allow installs)")