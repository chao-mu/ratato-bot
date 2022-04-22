# IRC
from asif.bot import Client, Channel

# Ours
from ratato.bot import Bot
from ratato.model import Connection, Message

TwitchServer = 'irc.chat.twitch.tv'
TwitchPort = 6667

class TwitchBot(Bot):

    def __init__(self, username, oath_token, inbox, outbox):
        self.inbox = inbox
        self.outbox = outbox
        self.is_connected = False
        self.connections = set()

        self.client = Client(
            host=TwitchServer,
            port=TwitchPort,
            user=username,
            password=oath_token,
        )

        self.add_commands(self.client)

    async def _run(self):
        await self.client.run()

    async def write_message(self, msg):
        conn = msg.connection
        channel = "#" + conn.twitch_username
        if conn not in self.connections:
            await self.client.join(channel)
            self.connections.add(conn)

        await self.client.message(channel, f'[{msg.author}] says: {msg.message}')

    def add_commands(self, client):
        @client.on_connected()
        async def connected():
            self.is_connected = True
            print("Twitch Server Joined!")

        @client.on_message()
        async def on_message(message):
            channel = message.recipient
            for conn in self.connections:
                if ("#" + conn.twitch_username) == channel.name:
                    await self.outbox.put(Message(conn, message.sender.name, message.text))
