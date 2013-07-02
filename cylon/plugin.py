import logging
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
