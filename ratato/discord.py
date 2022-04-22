# Core
import re

# Discord
from discord.ext import commands, tasks
import discord
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import SlashCommandOptionType

# Ours
from ratato.bot import Bot
from ratato.model import Connection, Message

class DiscordBot(Bot):
    def __init__(self, token, channel_id, inbox, outbox):
        self.token = token
        self.channel_id = channel_id
        self.is_connected = False
        self.inbox = inbox
        self.outbox = outbox
        self.connections = set()

        self.client = discord.Client(intents=discord.Intents.default())
        self.slash = SlashCommand(self.client, sync_commands=True)

        self.add_commands(self.client, self.slash)

    async def write_message(self, msg):
        channel = self.client.get_channel(self.channel_id)
        await channel.send(f'[{msg.author}] says: {msg.message}')

    def add_commands(self, client, slash):
        @client.event
        async def on_ready():
            print(f'{client.user} has connected to Discord!')
            self.is_connected = True
            await self.client.get_channel(self.channel_id).send("Chirp!")

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            for conn in self.connections:
                if conn.discord_channel_id == message.channel.id:
                    await self.outbox.put(Message(conn, message.author.name, message.content))

        @slash.slash(
                name="connect",
                # TODO Parameterize this
                guild_ids=[874089235106369606],
                description="Connect a Discord channel to a Twitch channel",
                options=[
                    {"name": "channel", "type": SlashCommandOptionType.CHANNEL, "required": True, "description": "Discord Channel"},
                    {"name": "twitch", "type": SlashCommandOptionType.STRING, "required": True, "description": "Twitch account"}
                ]
            )
        async def connect(ctx: SlashContext, channel, twitch):
            if not re.search(r"^\w+$", twitch):
                await ctx.send("Invalid Twitch username. Typo? Bug?")
                return

            conn = Connection(channel.id, twitch)
            if conn not in self.connections:
                self.connections.add(conn)

            msg = f"{ctx.guild} connected to {twitch}!"

            await ctx.send(msg)
            await self.outbox.put(Message(conn, client.user.name, msg))

    async def _run(self):
        await self.client.start(self.token)
