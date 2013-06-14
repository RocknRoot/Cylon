import logging
import xmpp
import re
from cylon.conf    import Settings
from cylon.command import Loader, Plugin

from optparse        import OptionParser

class Cylon:

    MSG_OK = 'Accept my fraking request. Now.'
    MSG_KO = 'DENIED.'


    def __init__(self):
      self._conn = None
      self._parser = OptionParser()
      self._parser.add_option("-c", "--conf_file", dest="conf_file",
                  default="/etc/cylon.yml",
                  help="use configuration file", )
      self._parser.add_option("-l", "--log_file", dest="log_file",
                  default="/var/log/cylon.log",
                  help="use specified file to write logs")
      self._parser.add_option("-D", "--debug", dest="debug",
                  action="store_false", default=True,
                  help="Debug mode into console")

      (self._options, self._args) = self._parser.parse_args()
      logging.basicConfig(filename=self._options.log_file,
                          level=logging.INFO)
      logging.info("Starting Cylon !")
      self._settings = Settings(self._options.conf_file)
      self._modules = Loader.get_modules(self._settings.plugin_dir,
                                         self._settings.loaded_plugins_at_start)
      built = Loader.get_builtins()
      self._modules['publics'].update(built['publics'])
      self._modules['privates'].update(built['privates'])
      Plugin.modules = self._modules
      Plugin.settings = self._settings
      self.__status = None
      if hasattr(self._settings, 'default_status'):
        self.__status = self._settings.default_status
      self.__connect()
      Plugin.connection = self._conn
      self.__run()

    def message_handler(self, conn, mess):
      if xmpp.NS_DELAY in mess.getProperties(): return
      sender = mess.getFrom().getResource()
      if sender == self._settings.chat_name: return
      body = mess.getBody()
      if not body: return

      prefixed = mess.getBody().startswith("%s "
           % self._settings.command_prefix)

      modules = {}
      modules.update(self._modules['publics'])
      if mess.getType() == "groupchat":
        Plugin.request_is_private = False
        muc_from = str(mess.getFrom())
        reply_to =  muc_from.split('/')[0]
        msg_type = "groupchat"
      else:
        Plugin.request_is_private = True
        reply_to = mess.getFrom()
        msg_type = "chat"
        if str(mess.getFrom()).split('/')[0] in self._settings.master_names:
          modules.update(self._modules['privates'])

      if prefixed or (mess.getType() == "chat"):
        cmd = mess.getBody()
        if prefixed:
          length = self._settings.command_prefix.__len__()
          cmd = cmd[length + 1:]
        cmd_parameters = cmd.split()
        if modules.has_key(cmd_parameters[0]):
          try:
            class_ = cmd_parameters.pop(0)
            if not cmd_parameters:
              func = "default"
            else:
              func =  cmd_parameters.pop(0)
            # Way to test if class exists.If exception, error msg.
            method = getattr(modules[class_], func)
          except AttributeError, e:
            msg = "Function %s not implemented." % func
            logging.error("%s plugin exec: %s" % (class_, str(e)))
          try:
            msg = modules[class_].wrapper(func, cmd_parameters)
          except Exception, e:
            msg = "Error during %s function execution." % func
            logging.error("%s plugin exec: %s" % (class_, str(e)))
        else:
          msg = "Command '%s': not found." % cmd_parameters[0]
        if not msg:
          # When a module doesn't return str.
          msg = "Hmm. Problem(s) during command execution. (Null return)."
        self.send(reply_to, msg, msg_type)

    def send(self, user, text, mess_type='chat'):
        mess = self.build_message(text)
        mess.setTo(user)
        mess.setType(mess_type)
        self._conn.send(mess)

    def build_message(self, text):
        text_plain = re.sub(r'<[^>]+>', '', text)
        message = xmpp.protocol.Message(body=text_plain)
        if text_plain != text:
            html = xmpp.Node('html', {'xmlns': 'http://jabber.org/protocol/xhtml-im'})
            try:
                html.addChild(node=xmpp.simplexml.XML2Node("<body xmlns='http://www.w3.org/1999/xhtml'>" +
                                                           text.encode('utf-8') + "</body>"))
                message.addChild(node=html)
            except Exception:
                message = xmpp.protocol.Message(body=text_plain)
        return message

    def presence_handler(self, conn, presence):
        jid, ptype, status = presence.getFrom(), \
                             presence.getType(), \
                             presence.getStatus()
        if self._jid.bareMatch(jid): return
        try:
            if jid in self._settings.master_names:
              subscription = self.roster.getSubscription(str(jid))
            else:
              subscription = None
        except KeyError:
            # User not on our roster
            subscription = None
        if ptype == 'error': logging.error(presence.getError())
        logging.debug("Presence for %s (type: %s, status: %s, subscription: %s)" %
                     (jid, ptype, status, subscription))
        if (ptype == 'subscribe') and (jid in self._settings.master_names):
            # Incoming presence subscription request
            if subscription in ('to', 'both', 'from'):
              self.roster.Authorize(jid)
              self._conn.send(xmpp.dispatcher.Presence(show=None,
                                                       status=self.__status))
            if subscription not in ('to', 'both'):
              self.roster.Subscribe(jid)
            if subscription in (None, 'none'):
              self.send(jid, self.MSG_OK)
        elif ptype == 'subscribed':
          # Authorize any pending requests for that JID
          self.roster.Authorize(jid)
        elif ptype == 'unsubscribed':
          # Authorization was not granted
          self.send(jid, self.MSG_KO)
          self.roster.Unauthorize(jid)


    def __connect(self):
      self._jid = xmpp.JID(self._settings.jid)
      if not self._conn:
        if not self._options.debug:
          conn = xmpp.Client(self._jid.getDomain())
        else:
          conn = xmpp.Client(self._jid.getDomain(), debug=[])
        res = conn.connect()
        if not res:
          logging.error("Unable to connect to server %s." %
                         self._jid.getDomain())
          exit()
        if res<>'tls':
          logging.warning("Unable to establish TLS connection.")

        res = conn.auth(self._jid.getNode(),
                        self._settings.password,
                        self._settings.chat_name)
        if not res:
          logging.error("Unable to authenticate this connection.")
          exit()
        if res<>'sasl':
          logging.warning("Unable to get SASL creditential for: %s." %
                          self.jid.getDomain())
        conn.RegisterHandler('message', self.message_handler)
        conn.RegisterHandler('presence', self.presence_handler)
        conn.sendInitPresence()
        self.roster = conn.Roster.getRoster()
        self._conn = conn
        if hasattr(self._settings, 'default_status'):
          self._conn.send(xmpp.Presence(status=self._settings.default_status))
        if hasattr(self._settings, 'groupchat'): self.__join_muc()

    def __join_muc(self):
        for room_config in self._settings.groupchat:
          if isinstance(room_config, dict):
            for k, v in room_config.iteritems():
              presence = xmpp.Presence(to="%s/%s" % (k, self._settings.chat_name))
              presence.setTag('x', namespace='http://jabber.org/protocol/muc').setTagData('password',v)
          else:
              presence = xmpp.Presence(to="%s/%s" % (room_config, self._settings.chat_name))
          self._conn.send(presence)

    def __run(self):
      while True:
        try:
          self._conn.Process(1)
        except KeyboardInterrupt:
          logging.info('Signal catched, shutting down.')
          break
      logging.info('Exiting. Bye.')
      exit()

