import re
import logging
from abc import ABCMeta, abstractmethod

class Hook:


  __metaclass__ = ABCMeta
  hooks = {}
  settings = {}
  connection = None
  ACTIONS = {}


  def __init__(self):
    mod_name = self.__class__.__name__
    logging.info("Hook %s loaded." % mod_name)
    self.regex = []


  def build_regex(self):
    for r in self.ACTIONS.keys():
      self.regex.append((re.compile(r), self.ACTIONS[r]))
