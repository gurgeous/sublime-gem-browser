import os
import pipes
import re
import sublime
import sublime_plugin
import subprocess

# NOTE: this is unsupported and only works on Mac OS with rbenv. Feel free to edit...

class ListGemsCommand(sublime_plugin.WindowCommand):
  """
  Quickly jump to a ruby gem from the current Gemfile.
  """

  # this
  BUNDLE = os.environ["HOME"] + "/.rbenv/shims/bundle"
  SUBL = "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"

  def run(self):
    self.gems = self.load_gems()
    if self.gems == None:
      return
    self.window.show_quick_panel(self.gems, self.on_done)

  def on_done(self, picked):
    if picked == -1:
      return

    # get gem path
    name = re.search("[^ ]+", self.gems[picked]).group()
    path = self.run_command(self.BUNDLE + " show " + name)
    if path == None:
      print("Here's what I got from bundle show:")
      print(path)
      sublime.error_message("Couldn't get gem path from bundler.")
      return

    # now open it
    path = path.strip()
    subprocess.Popen([self.SUBL, "-n", path])

  #
  # helpers
  #

  def load_gems(self):
    gems = self.run_command(self.BUNDLE + " list")
    gems = re.findall("^  \* (.*)$", gems, re.MULTILINE)
    if gems == [ ]:
      print("Here's what I got from bundle list:")
      print(gems)
      sublime.error_message("Couldn't get gems from bundle list.")
      return
    return gems

  def run_command(self, command):
    root = self.window.folders()[0]
    process = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True, cwd = root)
    output = process.communicate()[0]
    output = str(output, encoding = "utf-8")
    if output != "":
      return output
