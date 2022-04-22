#!/usr/bin/env python3

from ratato.discord import DiscordBot
from ratato.twitch import TwitchBot

# Core
import asyncio

# Community
import yaml

async def main():
    with open('secrets.yml') as secrets_file:
        secrets = yaml.load(secrets_file, Loader=yaml.SafeLoader)


    twitch_outbox = asyncio.Queue()
    discord_outbox = asyncio.Queue()

    twitch_bot = TwitchBot(
            secrets["twitch_bot_username"],
            secrets["twitch_oath_token"],
            discord_outbox,
            twitch_outbox)

    discord_bot = DiscordBot(
            secrets["discord_token"],
            874116394902503445,
            twitch_outbox,
            discord_outbox)

    tasks = [asyncio.create_task(twitch_bot.start()),
            asyncio.create_task(discord_bot.start())]

    await asyncio.wait(tasks)

if __name__ == "__main__":
    asyncio.run(main())
