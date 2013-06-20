import imp
import glob
import sys
import logging
from os.path import exists
from abc import ABCMeta, abstractmethod

class Plugin:

    __metaclass__ = ABCMeta
    plugins = {}
    settings = {}
    connection = None

    def __init__(self):
      mod_name = self.__class__.__name__
      logging.info("Plugin %s loaded." % mod_name)

    def wrapper(self, func, body, from_, chat_type, args):
      Method = getattr(self, func)
      return Method(body, from_, chat_type, args)

    def default(self, *args):
      return self.help(None, None, None, args)

    # This method has to be defined in plugins to help he users.
    @abstractmethod
    def help(self):
      pass

class Public(Plugin):

    __metaclass__ = ABCMeta

    def is_public(self):
      return True

    def is_private(self):
      return False

    @abstractmethod
    def help(self):
      pass

class Private(Plugin):

    __metaclass__ = ABCMeta

    def is_public(self):
      return False

    def is_private(self):
      return True

    @abstractmethod
    def help(self):
      pass


class Loader:

  BUILTINS = ['mod', 'help']
  BUILTIN_PLUGINS = 'cylon.builtins'

  @staticmethod
  def get_modules(plugins_dir, plugins_to_load):
    plugins = {'publics' : {}, 'privates': {}}
    if exists(plugins_dir):
      plugin_list = glob.glob("%s/**/**/*.mod" %
                               plugins_dir)
      plugins = get_needed_class(plugin_list,
                                 plugins_to_load)
    else:
      logging.error("plugin_dir doesn't exist !")

    return plugins

  @staticmethod
  def get_builtins():
    builtins = {'publics' : {}, 'privates': {}}
    __import__(Loader.BUILTIN_PLUGINS)
    module = sys.modules[Loader.BUILTIN_PLUGINS]
    for builtin_name in Loader.BUILTINS:
      builtin = getattr(module, cmd_to_class(builtin_name))
      try:
        builtin_instance = builtin()
        if builtin_instance.is_public():
          builtins['publics'].update({builtin_name : builtin_instance})
        else:
          builtins['privates'].update({builtin_name : builtin_instance})
      except TypeError:
        logging.error("You need to define help method for %s plugin class" %
                       builtin_name)
    return builtins

def cmd_to_class(command):
  while '_' in command:
    pos = command.index('_')
    command = command[:pos] + command[pos + 1:].capitalize()
  return command.capitalize()


def get_needed_class(filenames, plugin_list):
  plugins = { 'publics' : {}, 'privates' : {}}
  for filename in filenames:
    path_array = filename.split('/')
    name = path_array[-1:][0].split('.')[0]
    if not name in plugin_list:
      continue
    path =  "/".join(path_array[:len(path_array) - 1])
    wanted_class = cmd_to_class(name)
    if path.endswith('/'):
      src_path = path + path_array[-1:][0]
    else:
      src_path = "%s/%s" % (path, path_array[-1:][0])
    module = imp.load_source(path_array[-1:][0],
                               src_path)
    if hasattr(module, wanted_class):
      class_ = getattr(module, wanted_class)
      try:
        class_inst = class_()
        if class_inst.is_public():
          plugins['publics'].update({name : class_inst})
        else:
          plugins['privates'].update({name : class_inst})
      except TypeError:
        logging.error("You need to define help method for %s plugin class" % wanted_class)
    else:
      logging.warn("No %s class found in %s plugin file." %
                  (wanted_class, filename))
  return plugins
