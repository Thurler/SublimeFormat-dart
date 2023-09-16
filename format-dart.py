import sublime, sublime_plugin
import subprocess

class FormatDartCommand(sublime_plugin.TextCommand):
  tmp_filepath = "/tmp/sublime-dart-format.dart"

  def execShell(self, command):
    proc = subprocess.Popen(
      command,
      shell=True,
      bufsize=-1,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      stdin=subprocess.PIPE,
    )
    return proc.communicate()

  def run(self, edit):
    region = sublime.Region(0, self.view.size())
    with open(self.tmp_filepath, 'w') as f:
      f.write(self.view.substr(region))
    output, error = self.execShell("dartformat " + self.tmp_filepath)
    if error:
      sublime.error_message(error.decode('utf-8'))
    else:
      self.view.replace(edit, region, output.decode('utf-8'))

class AutoRunDartFormatOnSave(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    file_path = view.file_name()
    if not file_path:
      return
    if file_path.split('.')[-1] != "dart":
      return
    view.run_command("format_dart")
