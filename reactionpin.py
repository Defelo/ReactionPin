import json
import os
from typing import Set

from discord import Client, Message, TextChannel, RawReactionActionEvent, RawReactionClearEvent, Member, Guild

config: dict = json.load(open("config.json"))
CHANNELS: Set[int] = set(config["channels"])
EMOJIS: Set[str] = set(chr(int(e, 16)) for e in config["emojis"])
BLOCKED_ROLE: int = int(config["blocked_role"])


class Bot(Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        channel: TextChannel = self.get_channel(payload.channel_id)
        message: Message = await channel.fetch_message(payload.message_id)
        guild: Guild = channel.guild
        member: Member = guild.get_member(payload.user_id)
        if str(payload.emoji) in EMOJIS and channel.id in CHANNELS:
            if payload.user_id == message.author.id and all(r.id != BLOCKED_ROLE for r in member.roles):
                await message.pin()
            else:
                await message.remove_reaction(payload.emoji, self.get_user(payload.user_id))

    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        channel: TextChannel = self.get_channel(payload.channel_id)
        message: Message = await channel.fetch_message(payload.message_id)
        if str(payload.emoji) in EMOJIS and channel.id in CHANNELS and payload.user_id == message.author.id:
            await message.unpin()

    async def on_raw_reaction_clear(self, payload: RawReactionClearEvent):
        channel: TextChannel = self.get_channel(payload.channel_id)
        message: Message = await channel.fetch_message(payload.message_id)
        await message.unpin()


Bot().run(os.environ["TOKEN"])
