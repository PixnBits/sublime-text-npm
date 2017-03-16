import sublime, sublime_plugin

from .command import NpmCommand


class NpmRepoPackageCommand(NpmCommand, sublime_plugin.TextCommand):
  def run(self, edit):
    selected_text = []
    window = sublime.active_window()
    active_view = window.active_view()
    for region in active_view.sel():
      if not region.empty():
        selected_text.append(active_view.substr(region))
    selected_text = ' '.join(selected_text).replace('\n',' ').replace('\r',' ')
    window.show_input_panel('repository of package', selected_text, self.got_package_name, None, None)

  def got_package_name(self, package_name):
    self.run_npm(['repo', package_name])
