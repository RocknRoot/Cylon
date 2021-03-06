import imp
import glob
import sys
import logging
from os.path import exists
from cylon.hook import Hook
from cylon.plugin import Plugin, Public, Private

class Loader:


  BUILTINS = ['plug', 'help']
  BUILTIN_PLUGINS = 'cylon.builtins'


  @staticmethod
  def get_modules(plugins_dir, plugins_to_load, alias_list):
    plugins = [{'publics' : {}, 'privates': {}},
               {'publics' : {}, 'privates': {}}]
    if exists(plugins_dir):
      plugin_list = glob.glob("%s/**/**/*.mod" %
                               plugins_dir)
      plugins = get_needed_class(plugin_list,
                                 plugins_to_load,
                                 alias_list)
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


  @staticmethod
  def get_hooks(hooks_dir, hooks_to_load):
    hooks = {}
    if exists(hooks_dir):
      hook_list = glob.glob("%s/**/**/*.hook" % hooks_dir)
      hooks = get_needed_hooks(hook_list, hooks_to_load)
    else:
      logging.error("hook_dir doesn't exist ! ")
    return hooks


def cmd_to_class(command):
  while '_' in command:
    pos = command.index('_')
    command = command[:pos] + command[pos + 1:].capitalize()
  return command.capitalize()


def compute_aliases(alias_info, class_inst, plugin_name):
  logging.debug("Loading aliases...")
  alias_hash = {}
  for method_name, alias_name in alias_info.iteritems():
    alias_hash.update({alias_name : { method_name : class_inst }})
  logging.debug("Final alias list:")
  logging.debug(alias_hash)
  return alias_hash


def get_needed_class(filenames, plugin_list, alias_list):
  plugins = { 'publics' : {}, 'privates' : {}}
  aliases = { 'publics' : {}, 'privates' : {}}
  for filename in filenames:
    path_array = filename.split('/')
    name = path_array[-1:][0].split('.')[0]
    if not name in plugin_list:
      continue
    path = "/".join(path_array[:len(path_array) - 1])
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
          if name in alias_list.keys():
            aliases['publics'].update(compute_aliases(alias_list[name], class_inst, name))
        else:
          plugins['privates'].update({name : class_inst})
          if alias_list.has_key(name):
            aliases['privates'].update(compute_aliases(alias_list[name], class_inst, name))
      except TypeError:
        logging.error("You need to define help method for %s plugin class" % wanted_class)
    else:
      logging.warn("No %s class found in %s plugin file." %
                  (wanted_class, filename))
  return [plugins, aliases]


def get_needed_hooks(filenames, hook_list):
  hooks = {}
  for filename in filenames:
    path_array = filename.split('/')
    name = path_array[-1:][0].split('.')[0]
    if not name in hook_list:
      continue
    path = "/".join(path_array[:len(path_array) - 1])
    wanted_class = cmd_to_class(name)
    if path.endswith('/'):
      src_path = path + path_array[-1:][0]
    else:
      src_path = "%s/%s" % (path, path_array[-1:][0])
    hook = imp.load_source(path_array[-1:][0], src_path)
    if hasattr(hook, wanted_class):
      class_ = getattr(hook, wanted_class)
      if issubclass(class_, Hook):
        class_inst = class_()
        class_inst.build_regex()
        hooks.update({name: class_inst})
      else:
        logging.error("You need to define ACTIONS dictionary for %s hook class" % wanted_class)
    else:
      logging.warn("No %s class found in %s hook file." % (wanted_class, filename))
  return hooks
