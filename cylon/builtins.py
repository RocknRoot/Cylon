import logging
from cylon.command import Plugin, Public, Private

class Help(Public):

  def help(self, body, from_user, chat_type, args):
    msg = "\nCylon help:\n  Available modules:\n"
    if not self.request_is_private:
      array = ['publics']
    else:
      array = ['publics', 'privates']
    for type_ in array:
      for module_name in self.modules[type_]:
        msg = msg + "    %s -> %s %s help\n" % (module_name, self.settings.command_prefix, module_name)
    return msg

class Mod(Private):

  def help(self, body, from_user, chat_type, args):
    msg = "\nmodule builtin:\n\
    mod help - display help\n\
    mod list - list modules\n\
    mod add <module_name> - load module dynamically\n\
    mod rm  <module_name> - remove module from loaded module\n"
    return msg

  def list(self, *args):
    msg = "\n"
    for type_ in list(self.modules.viewkeys()):
      msg = msg + type_ + ":\n"
      for module_name in self.modules[type_]:
        msg = msg + "    - %s\n" % module_name
    return msg

  def add(self, *args):
    return "Not implemented."

  def rm(self, *args):
    return "Not implemented."


