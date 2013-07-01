import logging
from cylon.plugin import Plugin, Public, Private

class Help(Public):

  def help(self, body, from_user, chat_type, args):
    msg = "\nCylon help:\n  Available plugins:\n"
    if not self.request_is_private:
      array = ['publics']
    else:
      array = ['publics', 'privates']
    for type_ in array:
      for plugin_name in self.modules[type_]:
        msg = msg + "    %s -> %s %s help\n" % (plugin_name, self.settings.command_prefix, plugin_name)
    return msg

class Plug(Private):

  def help(self, body, from_user, chat_type, args):
    msg = "\nplugin builtin:\n\
    plug help - display help\n\
    plug list - list plugins\n\
    plug load <plugin_name> - load plugin dynamically\n\
    plug unload  <plugin_name> - unload plugin from loaded plugins\n"
    return msg

  def list(self, body, from_user, chat_type, args):
    msg = "\n"
    for type_ in list(self.modules.viewkeys()):
      msg = msg + type_ + ":\n"
      for plugin_name in self.modules[type_]:
        msg = msg + "    - %s\n" % plugin_name
    return msg

  def load(self, body, from_user, chat_type, args):
    return "Not implemented."

  def unload(self, body, from_user, chat_type, args):
    return "Not implemented."


