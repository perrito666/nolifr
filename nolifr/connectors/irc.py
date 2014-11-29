#! env python3
# GPL Goes here
from twisted.words.protocols import irc

from nolifr.event import Event

# http://twistedmatrix.com/documents/current/api/twisted.words.protocols.irc.IRCClient.html
EV_CONNECTED="connectionMade"
EV_DISCONNECTED="connectionLost"

class IRCEvent(Event):
    def __init__(self, event_name, message, user, channel, conn_id):
        super(IRCEvent, self).__init__()
        self.event_name = event_name
        self.message = message
        self.user = user
        self.channel = channel
        self.conn_id = conn_id

    def to_json(self):
        return {
            "event_name": self.event_name,
            "message": self.message,
            "user": self.user,
            "channel": self.channel,
            "conn_id": self.conn_id,
        }


class IRCClient(irc.IRCClient):
    def __init__(self, nickname, username, password,
                        realname, hostname, nickserv_password,
                        event_handler):
        super(IRCClient, self).__init__()
        self.nickname = nickname
        self.hostname = hostname
        self.username = username
        self.password = password
        self.nickserv_password = nickserv_password
        self._handler = event_handler
        self.sourceURL = "http://github.com/perrito666/nolifr"

    def __conn_id(self):
        return "%s@%s" % (self.nickname, self.hostname)

    def __newEvent(self, event, message=None, channel=None):
        return IRCEvent(event, message, self.username, channel, self.__conn_id())

    def connectionMade(self):
        super(IRCClient, self).connectionMade(self)
        # should emmit a connection made event
        event = self.__newEvent(EV_CONNECTED)
        self._handler.emit(event)

    def connectionLost(self, reason):
        event = self.__newEvent(EV_DISCONNECTED)
        self._handler.emit(event)
        #FIXME: Return and decorate?
        #FIXME: Return and decorate?
        super(IRCClient, self).connectionLost(self, reason)
        # should emmit a connection lost event


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""

    def joined(self, channel):
        """This will get called when the bot joins the channel."""

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            pass

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname): #FIXME: Fails with partially colliding names
            pass

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '_'


