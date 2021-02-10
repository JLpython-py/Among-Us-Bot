#! python3
# voicechannelcontrol.py

"""
==============================================================================
MIT License

Copyright (c) 2020 Jacob Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==============================================================================
"""

import asyncio
import logging

import discord
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(levelname) - %(message)"
)


class VoiceChannelControl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emojis = [
            u'0\ufe0f\u20e3', u'1\ufe0f\u20e3', u'2\ufe0f\u20e3',
            u'3\ufe0f\u20e3', u'4\ufe0f\u20e3', u'5\ufe0f\u20e3',
            u'6\ufe0f\u20e3', u'7\ufe0f\u20e3', u'8\ufe0f\u20e3',
            u'9\ufe0f\u20e3']
        self.claims = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id not in self.claims:
            return
        direct_message = await member.create_dm()
        if before.channel and after.channel is None:
            del self.claims[member.id]
            await direct_message.send(
                f"{member.mention}: All claims forcefully yielded after voice channel disconnect"
            )
        if after.afk:
            del self.claims[member.id]
            await direct_message.send(
                f"{member.mention}: All claims forcefully yielded due to inactivity"
            )

    @commands.command(name="claim", pass_context=True)
    async def claim(self, ctx):
        """ Invoke a claim request panel
            Member cannot have an active claim request
            Member cannot have a claim on another voice channel
"""
        if ctx.author.id in self.claims:
            await ctx.send("You already have a voice channel claim")
            return
        embed = discord.Embed(
            title="Select Lobby Claim Mode",
            color=0x0000ff
        )
        embed.add_field(
            name="Options",
            value=":zero: - Game Lobby\n:one: - Game Lobby and Ghost Lobby"
        )
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction(u'0\ufe0f\u20e3')
        await message.add_reaction(u'1\ufe0f\u20e3')
        try:
            payload = await self.bot.wait_for(
                "raw_reaction_add",
                timeout=30.0,
                check=lambda p: p.member.id == ctx.author.id
            )
            await message.delete()
        except asyncio.TimeoutError:
            await message.delete()
            return
        if payload.emoji.name not in [u'0\ufe0f\u20e3', u'1\ufe0f\u20e3']:
            return
        game = await self.claim_voice_channel(ctx, style="Game Lobby")
        if game is None:
            return
        self.claims[ctx.author.id] = [game]
        if payload.emoji.name == u'0\ufe0f\u20e3':
            await self.voice_control(ctx, game=game, ghost=None)
        elif payload.emoji.name == u'1\ufe0f\u20e3':
            ghost = await self.claim_voice_channel(ctx, style="Ghost Lobby")
            if ghost is None:
                await self.voice_control(ctx, game=game, ghost=None)
                return
            self.claims[ctx.author.id].append(ghost)
            await self.voice_control(ctx, game=game, ghost=ghost)

    async def claim_voice_channel(self, ctx, *, style):
        """ Send an embed with reactions for member to designate a lobby VC
"""
        claimed = []
        for claim in self.claims.values():
            claimed.extend(claim)
        voice_channels = [
            c for c in ctx.guild.voice_channels
            if c.id not in claimed
        ][:10]
        if not voice_channels:
            await ctx.channel.send(
                "There are no available voice channels to claim."
            )
            return
        embed = discord.Embed(
            title=f"Claim a Voice Channel for a {style}",
            color=0x0000ff
        )
        fields = {
            "Channel Options": '\n'.join([
                f"{self.emojis[voice_channels.index(c)]} - {c}"
                for c in voice_channels
            ]),
            "Claim": "Use the reactions below to claim a voice channel",
            "Cancel": "This message will automatically close after 30s"
        }
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        embed.set_footer(
            text=f"VoiceChannelControl | {ctx.author.id}"
        )
        message = await ctx.channel.send(embed=embed)
        for chan in voice_channels:
            await message.add_reaction(
                self.emojis[voice_channels.index(chan)]
            )
        try:
            payload = await self.bot.wait_for(
                "raw_reaction_add", timeout=30.0,
                check=lambda p: p.member.id == ctx.author.id
            )
            await message.delete()
        except asyncio.TimeoutError:
            return
        return voice_channels[
            self.emojis.index(payload.emoji.name)
        ].id

    async def voice_control(self, ctx, game, ghost):
        # Get applicable voice channels and appropriate reactions
        game = self.bot.get_channel(id=game)
        if ghost is None:
            reactions = [
                u"\U0001F507", u"\U0001F508", u"\U0001F3F3"
            ]
            fields = {
                "Claimed": f"Game: `{game.name}`",
                "Voice Channel Control": "\n".join([
                    "Mute All- :mute:",
                    "Unmute All - :speaker:",
                    "Yield - :flag_white:"
                ])
            }
        else:
            ghost = self.bot.get_channel(id=ghost)
            reactions = [
                u"\U0001F507", u"\U0001F508", u"\U0001F47B",
                u"\U0001F3E5", u"\U0001F504", u"\U0001F3F3"
            ]
            fields = {
                "Claimed": f"Game: `{game.name}`\nGhost: `{ghost.name}`",
                "Voice Channel Control": "\n".join([
                    "Mute All - :mute:",
                    "Unmute All - :speaker:",
                    "Select and Move Member to Ghost - :ghost:",
                    "Select and Move Member to Game - :hospital:",
                    "Revert All Actions/Reset Game - :arrows_counterclockwise:"
                    "Yield - :flag_white:"
                ])
            }
        embed = discord.Embed(
            title="Voice Channel Control", color=0x0000ff)
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        embed.set_footer(text="VoiceChannelControl")
        message = await ctx.channel.send(embed=embed)
        for rxn in reactions:
            await message.add_reaction(rxn)
        await self.process_input(message, ctx)

    async def process_input(self, message, ctx):
        while True:
            try:
                payload = await self.bot.wait_for(
                    "raw_reaction_add",
                    timeout=600,
                    check=lambda p: p.member.id == ctx.author.id
                )
            except asyncio.TimeoutError:
                check = await ctx.channel.send(
                    f"{ctx.author.mention}: React to confirm you're still active"
                )
                await check.add_reaction(u"\U0001F44D")
                try:
                    await self.bot.wait_for(
                        "raw_reaction_add",
                        timeout=60.0,
                        check=lambda p: p.member.id == ctx.author.id
                    )
                    await check.delete()
                    continue
                except asyncio.TimeoutError:
                    await check.clear_reactions()
                    await check.edit(
                        f"{ctx.author.mention}: All claims forcefully yielded due to inactivity"
                    )
                    break
            if payload.emoji.name in [u"\U0001F507", u"\U0001F508"]:
                await self.manage_voices(payload)
            elif payload.emoji.name == u"\U0001F47B":
                await self.member_dead(payload)
            elif payload.emoji.name == u"\U0001F3E5":
                await self.member_alive(payload)
            elif payload.emoji.name == u"\U0001F504":
                await self.reset_game(payload)
            elif payload.emoji.name == u"\U0001F3F3":
                await ctx.channel.send(
                    f"{ctx.author.mention}: All claims yielded successfully"
                )
                break
            await message.remove_reaction(payload.emoji, payload.member)
        await message.delete()
        del self.claims[ctx.author.id]

    async def manage_voices(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        # Manage the voices of the members based on the emoji used
        emojis = {"\U0001F507": True, "\U0001F508": False}
        voice_channel = self.bot.get_channel(
            self.claims.get(payload.member.id)
        )
        if not voice_channel.members:
            msg = await channel.send(
                f"there are no members in {voice_channel.name}"
            )
            await asyncio.sleep(5)
            await msg.delete()
        else:
            for member in voice_channel.members:
                await member.edit(
                    mute=emojis.get(payload.emoji.name)
                )
        await message.remove_reaction(payload.emoji, payload.member)

    async def member_dead(self, payload):
        # Get channel of payload and claimed game, ghost channels
        channel = self.bot.get_channel(payload.channel_id)
        guild = self.bot.get_guild(payload.guild_id)
        game, ghost = [
            self.bot.get_channel(id=c)
            for c in self.claims[payload.member.id]
        ]
        # Get all members who can be moved (no claims)
        available_members = [m for m in game.members][:10]  # if m.id not in self.claims
        if not available_members:
            msg = await channel.send("There are no members which can be moved")
            await asyncio.sleep(5)
            await msg.delete()
            return
        # Send embed with options and reactions to move
        embed = discord.Embed(
            title="Move member to Ghost Lobby", color=0x0000ff
        )
        fields = {
            "Select Members": '\n'.join([
                f"{self.emojis[available_members.index(c)]} - {c}"
                for c in available_members
            ]),
            "Moving Members": "Members will be moved once this message closes."
        }
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        embed.set_footer(
            text="This message will automatically close when stale for 5s."
        )
        message = await channel.send(embed=embed)
        for mem in available_members[:10]:
            await message.add_reaction(
                self.emojis[available_members.index(mem)]
            )
        # Wait for member to add all reactions
        while True:
            try:
                await self.bot.wait_for(
                    "raw_reaction_add",
                    timeout=5.0,
                    check=lambda p: (
                        p.member.id == payload.member.id
                        and p.emoji.name in self.emojis
                    )
                )
            except asyncio.TimeoutError:
                break
        # Parse through message reactions
        message = await channel.fetch_message(message.id)
        for rxn in message.reactions:
            async for user in rxn.users():
                mem = guild.get_member(user.id)
                if mem.id == payload.member.id:
                    break
            member = available_members[
                self.emojis.index(rxn.emoji)
            ]
            await member.move_to(ghost)
        await message.delete()

    async def member_alive(self, payload):
        game, ghost = [
            self.bot.get_channel(id=c)
            for c in self.claims[payload.member.id]
        ]

    async def reset_game(self, payload):
        game, ghost = [
            self.bot.get_channel(id=c)
            for c in self.claims[payload.member.id]
        ]
        for mem in ghost.members:
            await mem.move_to(game)


def setup(bot):
    """ Allow lib.bot.__init__.py to add VoiceChannelControl cog
"""
    bot.add_cog(VoiceChannelControl(bot))
