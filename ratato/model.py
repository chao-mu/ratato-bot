# Core
from collections import namedtuple

Connection = namedtuple('Connection', ['discord_channel_id', 'twitch_username'])

class Message:
    def __init__(self, connection, author, message):
        self.connection = connection
        self.author = author
        self.message = message
