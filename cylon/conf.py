import os
import logging
from yaml import load

class Settings:

    MANDATORY_ATTR = { 'username' : str,
                       'domain' : str,
                       'password' : str ,
                       'loaded_plugins_at_start' : list,
                       'plugin_dir' : str,
                       'chat_name' : str,
                       'master_names' : list,
                       'command_prefix' : str }

    OPTIONNAL_ATTR = { 'log_mode' : int,
                       'default_status' : str,
                       'muc' : str,
                       'muc_pwd': str,
                       'groupchat': list }

    ATTRS = [ MANDATORY_ATTR, OPTIONNAL_ATTR ]

    def __init__(self, conf_file):
      logging.debug("Starting configuration parsing")
      try:
        stream = file(conf_file, 'r')
      except Exception, e:
        logging.error("%s read: %s" % (conf_file, str(e)))
        exit()
      logging.info("Loading %s" % conf_file)
      self._conf_file_values = load(stream)
      logging.info("Configuration loaded")
      self.__set_log_mode()
      self.__check()
      self.jid = "%s@%s" % (self.username, self.domain)

    def __check(self):
      logging.debug("Configuration check")
      for attr_type in self.ATTRS:
        for attr in attr_type:
          if self._conf_file_values.has_key(attr):
            if not isinstance(self._conf_file_values[attr], attr_type[attr]):
              logging.error("Type error in configuration file: %s has to be a %s." %
                           (attr, attr_type[attr]))
              exit()
            else:
              value = self._conf_file_values[attr]
              setattr(self, attr, value)
              if attr == "password":
                value = "NOT WRITTEN IN LOGFILE"
              logging.debug("Using setting %s: %s" % (attr, value))
          else:
            if attr_type is self.MANDATORY_ATTR:
              logging.error("Configuration error: '%s' setting not found." % (attr))
              exit()

    def __set_log_mode(self):
      try:
        value = self._conf_file_values['log_mode']
        # If wrong or any value, set to logging.INFO
        if (value < 0) and (value > 4):
          value = 2
      except KeyError:
        value = 2
      # logging.DEBUG    -> 10
      # logging.INFO     -> 20
      # logging.WARNING  -> 30
      # logging.ERROR    -> 40
      # logging.CRITICAL -> 50
      logging.getLogger().setLevel(value * 10)
