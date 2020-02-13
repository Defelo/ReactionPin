import json
import os
from typing import Set

from discord import Client, Message, TextChannel, RawReactionActionEvent

config: dict = json.load(open("config.json"))
CHANNELS: Set[int] = set(config["channels"])
EMOJIS: Set[str] = set(chr(int(e, 16)) for e in config["emojis"])


class Bot(Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        channel: TextChannel = self.get_channel(payload.channel_id)
        message: Message = await channel.fetch_message(payload.message_id)
        if str(payload.emoji) in EMOJIS and channel.id in CHANNELS and payload.user_id == message.author.id:
            await message.pin()

    async def on_raw_reaction_remove(self, payload):
        channel: TextChannel = self.get_channel(payload.channel_id)
        message: Message = await channel.fetch_message(payload.message_id)
        if str(payload.emoji) in EMOJIS and channel.id in CHANNELS and payload.user_id == message.author.id:
            await message.unpin()


Bot().run(os.environ["TOKEN"])
