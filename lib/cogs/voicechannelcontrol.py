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
import csv
import os

import discord
from discord.ext import commands


class VoiceChannelControl(commands.Cog):
    """ Allow member to claim voice channels and control member properties
"""
    def __init__(self, bot):
        self.bot = bot
        self.emojis = [
            u'0\ufe0f\u20e3', u'1\ufe0f\u20e3', u'2\ufe0f\u20e3',
            u'3\ufe0f\u20e3', u'4\ufe0f\u20e3', u'5\ufe0f\u20e3',
            u'6\ufe0f\u20e3', u'7\ufe0f\u20e3', u'8\ufe0f\u20e3',
            u'9\ufe0f\u20e3']
        self.claims = {}
        self.locked = []

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """ Forcefully yield voice channel claim
"""
        # Verify member has a voice channel claim
        if member.id not in self.claims:
            return
        direct_message = await member.create_dm()
        # Check if member disconnected from voice channels
        if before.channel and after.channel is None:
            del self.claims[member.id]
            await direct_message.send(
                f"{member.mention}: All claims forcefully yielded after voice channel disconnect"
            )
        # Check if member is AFK
        if after.afk:
            del self.claims[member.id]
            await direct_message.send(
                f"{member.mention}: All claims forcefully yielded due to inactivity"
            )

    @commands.command(
        name="claim", case_insensitive=True, pass_context=True
    )
    async def claim(self, ctx):
        """ Invoke a request to claim voice channels
"""
        # Verify member does not have a voice channel claim
        if ctx.author.id in self.claims:
            await ctx.send("You already have a voice channel claim")
            return
        # Send prompt for member to decide how many voice channels to claim
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
        # Wait for valid member response
        try:
            payload = await self.bot.wait_for(
                "raw_reaction_add",
                timeout=30.0,
                check=lambda p: (
                        p.member.id == ctx.author.id
                        and p.message_id == message.id
                )
            )
            await message.delete()
        except asyncio.TimeoutError:
            await message.delete()
            return
        if payload.emoji.name not in [u'0\ufe0f\u20e3', u'1\ufe0f\u20e3']:
            await message.delete()
            return
        # Allow member to claim a voice channel for a Game Lobby
        game = await self.claim_voice_channel(ctx, style="Game Lobby")
        if game is None:
            return
        self.claims[ctx.author.id] = [game]
        # Check if member requested to claim a voice channel for a Ghost Lobby
        if payload.emoji.name == u'0\ufe0f\u20e3':
            await self.voice_control(ctx, game=game, ghost=None)
        elif payload.emoji.name == u'1\ufe0f\u20e3':
            # Allow member to claim a voice channel for a Ghost Lobby
            ghost = await self.claim_voice_channel(ctx, style="Ghost Lobby")
            if ghost is None:
                await self.voice_control(ctx, game=game, ghost=None)
                return
            self.claims[ctx.author.id].append(ghost)
            await self.voice_control(ctx, game=game, ghost=ghost)

    @commands.command(
        name="claimed", case_insensitive=True, pass_context=True
    )
    async def claimed(self, ctx):
        """ Return all members with claims and repsective claimed voice channels
"""
        embed = discord.Embed(
            title="Claimed Voice Channels", color=0x0000ff
        )
        for claim in self.claims:
            game = self.bot.get_channel(
                id=self.claims[claim][0]
            )
            value = f"`Game`: {game.name}"
            if len(self.claims[claim]) == 2:
                ghost = self.bot.get_channel(
                    id=self.claims[claim][1]
                )
                value += f"\n`Ghost`: {ghost.name}"
            embed.add_field(
                name=discord.utils.get(
                    ctx.guild.members, id=ctx.author.id
                ).name,
                value=value
            )
        await ctx.channel.send(embed=embed)

    async def claim_voice_channel(self, ctx, *, style):
        """ Send an embed with reactions for member to designate a lobby VC
"""
        # Get all available voice channels
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
        # Send prompt for member to claim a voice channel
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
        # Wait for member to select a voice channel
        try:
            payload = await self.bot.wait_for(
                "raw_reaction_add", timeout=30.0,
                check=lambda p: (
                        p.member.id == ctx.author.id
                        and p.message_id == message.id
                )
            )
            await message.delete()
            return voice_channels[
                self.emojis.index(payload.emoji.name)
            ].id
        except asyncio.TimeoutError:
            await message.delete()
            return

    async def voice_control(self, ctx, game, ghost):
        """ Allow member to control member properties in claimed voice channels
"""
        # Get Game Lobby voice channel
        game = self.bot.get_channel(id=game)
        # Check if Ghost Lobby is applicable
        if ghost is None:
            reactions = [
                u"\U0001F507", u"\U0001F508", u"\U0001F515",
                u"\U0001F514", u"\U0001F3F3", u"\U0001F512"
            ]
            fields = {
                "Claimed": f"Game: `{game.name}`",
                "Voice Channel Control": "\n".join([
                    "Mute/Un-Mute All - :mute:/:speaker:",
                    "Deafen/Un-Deafen All - :no_bell:/:bell:",
                    "Yield - :flag_white:",
                    "Disable/Enable `MapDatabase` Commands - :lock:"
                ])
            }
        else:
            # Get Ghost Lobby voice channel
            ghost = self.bot.get_channel(id=ghost)
            reactions = [
                u"\U0001F507", u"\U0001F508", u"\U0001F515",
                u"\U0001F514", u"\U0001F47B", u"\U0001F3E5",
                u"\U0001F504", u"\U0001F3F3", u"\U0001F512"
            ]
            fields = {
                "Claimed": f"Game: `{game.name}`\nGhost: `{ghost.name}`",
                "Voice Channel Control": "\n".join([
                    "Mute/Un-Mute All - :mute:/:speaker:",
                    "Deafen/Un-Deafen All - :no_bell:/:bell:",
                    "Select and Move Member(s) to Ghost - :ghost:",
                    "Select and Move Member(s) to Game - :hospital:",
                    "Revert All Actions/Reset Game - :arrows_counterclockwise:",
                    "Yield - :flag_white:",
                    "Disable/Enable `MapDatabase` Commands - :lock:"
                ])
            }
        # Send prompt for user to control member properties
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
        """ Handle member emoji usage and perform corresponding action(s)
"""
        while True:
            # Wait for member to control voice channels with reacions
            try:
                payload = await self.bot.wait_for(
                    "raw_reaction_add",
                    timeout=600,
                    check=lambda p: (
                            p.member.id == ctx.author.id
                            and p.message_id == message.id
                    )
                )
            # Check if member is still actively using voice channel claim
            except asyncio.TimeoutError:
                check = await ctx.channel.send(
                    f"{ctx.author.mention}: React to confirm you're still active"
                )
                await check.add_reaction(u"\U0001F44D")
                # Wait for member response to inactivity warning
                try:
                    await self.bot.wait_for(
                        "raw_reaction_add",
                        timeout=60.0,
                        check=lambda p: (
                                p.member.id == ctx.author.id
                                and p.message_id == check.id
                        )
                    )
                    await check.delete()
                    continue
                # Forcefully yield voice channel claim
                except asyncio.TimeoutError:
                    await check.clear_reactions()
                    await check.edit(
                        f"{ctx.author.mention}: All claims forcefully yielded due to inactivity"
                    )
                    break
            # Call functions according to emoji used
            if payload.emoji.name in [u"\U0001F507", u"\U0001F508"]:
                await self.manage_mute(payload)
            elif payload.emoji.name in [u"\U0001F515", u"\U0001F514"]:
                await self.manage_deafen(payload)
            elif payload.emoji.name == u"\U0001F47B":
                await self.member_dead(payload)
            elif payload.emoji.name == u"\U0001F3E5":
                await self.member_alive(payload)
            elif payload.emoji.name == u"\U0001F504":
                await self.reset_game(payload)
            elif payload.emoji.name == u"\U0001F3F3":
                await self.yield_control(payload)
                await ctx.channel.send(
                    f"{ctx.author.mention}: All claims yielded successfully"
                )
                break
            elif payload.emoji.name == u"\U0001F512":
                await self.lock_commands(payload)
            await message.remove_reaction(payload.emoji, payload.member)
        await message.delete()

    async def manage_mute(self, payload):
        """ Mute/Un-Mute members in Game Lobby
"""
        # Get information from payload
        channel = self.bot.get_channel(payload.channel_id)
        voice_channel = self.bot.get_channel(
            id=self.claims.get(payload.member.id)[0]
        )
        # Verify members are present in the voice channel
        if not voice_channel.members:
            msg = await channel.send(
                f"There are no members in {voice_channel.name}"
            )
            await asyncio.sleep(2)
            await msg.delete()
        # Edit all members' voices according to the emoji used
        else:
            emojis = {"\U0001F507": True, "\U0001F508": False}
            for member in voice_channel.members:
                await member.edit(
                    mute=emojis.get(payload.emoji.name)
                )

    async def manage_deafen(self, payload):
        """ Deafen/Un-Deafen members in Game Lobby
"""
        # Get information from payload
        channel = self.bot.get_channel(payload.channel_id)
        voice_channel = self.bot.get_channel(
            id=self.claims.get(payload.member.id)[0]
        )
        # Verify members are present in the voice channel
        if not voice_channel.members:
            msg = await channel.send(
                f"There are no members in {voice_channel.name}"
            )
            await asyncio.sleep(2)
            await msg.delete()
        # Edit all members' voices according to the emoji used
        else:
            emojis = {u"\U0001F515": True, u"\U0001F514": False}
            for member in voice_channel.members:
                await member.edit(
                    deafen=emojis.get(payload.emoji.name)
                )

    async def member_dead(self, payload):
        """ Move member from Game Lobby to Ghost Lobby
"""
        # Get channel of payload and claimed game, ghost channels
        channel = self.bot.get_channel(payload.channel_id)
        game, ghost = [
            self.bot.get_channel(id=c)
            for c in self.claims[payload.member.id]
        ]
        # Get all members who can be moved (no claims)
        available_members = [m for m in game.members if m.id not in self.claims][:10]
        if not available_members:
            msg = await channel.send("There are no members which can be moved")
            await asyncio.sleep(2)
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
                        and p.message_id == message.id
                        and p.emoji.name in self.emojis
                    )
                )
            except asyncio.TimeoutError:
                break
        # Parse through message reactions and move corresponding members
        message = await channel.fetch_message(message.id)
        for rxn in message.reactions:
            async for user in rxn.users():
                # Ignore reaction if added by bot
                if user.id == payload.member.id:
                    await available_members[
                        self.emojis.index(rxn.emoji)
                    ].move_to(ghost)
        await message.delete()

    async def member_alive(self, payload):
        """ Move members from Ghost Lobby to Game Lobby
"""
        # Get channel of payload and claimed game, ghost channels
        channel = self.bot.get_channel(payload.channel_id)
        game, ghost = [
            self.bot.get_channel(id=c)
            for c in self.claims[payload.member.id]
        ]
        # Get all members who can be moved
        if not ghost.members:
            msg = await channel.send("There are no members which can be moved")
            await asyncio.sleep(2)
            await msg.delete()
            return
        # Send embed with options and reactions to move
        embed = discord.Embed(
            title="Move member to Game Lobby", color=0x0000ff
        )
        fields = {
            "Select Members": '\n'.join([
                f"{self.emojis[ghost.members.index(c)]} - {c}"
                for c in ghost.members[:10]
            ]),
            "Moving Members": "Members will be moved once this message closes."
        }
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        embed.set_footer(
            text="This message will automatically close when stale for 5s."
        )
        message = await channel.send(embed=embed)
        for mem in ghost.members[:10]:
            await message.add_reaction(
                self.emojis[ghost.members.index(mem)]
            )
        # Wait for member to add all reactions
        while True:
            try:
                await self.bot.wait_for(
                    "raw_reaction_add",
                    timeout=5.0,
                    check=lambda p: (
                            p.member.id == payload.member.id
                            and p.message_id == message.id
                            and p.emoji.name in self.emojis
                    )
                )
            except asyncio.TimeoutError:
                break
        # Parse through message reactions and move corresponding members
        message = await channel.fetch_message(message.id)
        for rxn in message.reactions:
            async for user in rxn.users():
                # Ignore reaction if added by bot
                if user.id == payload.member.id:
                    await ghost.members[
                        self.emojis.index(rxn.emoji)
                    ].move_to(game)
        await message.delete()

    async def reset_game(self, payload):
        """ Revert member properties to defaults
"""
        game, ghost = [
            self.bot.get_channel(id=c)
            for c in self.claims[payload.member.id]
        ]
        # Move all members from Ghost Lobby to Game Lobby
        for mem in ghost.members:
            await mem.move_to(game)
        # Unmute and Undeafen all members
        for mem in game.members:
            await mem.edit(mute=False, deafen=False)

    async def yield_control(self, payload):
        """ Yield control of voice channel claims
"""
        # Delete channel from list of locked voice channels
        game = self.claims[payload.member.id][0]
        if game in self.locked:
            self.locked.remove(game)
        with open(os.path.join("data", "locked.txt"), "w") as file:
            writer = csv.writer(file)
            writer.writerow(self.locked)
        # Delete channel from claimed channels
        del self.claims[payload.member.id]

    async def lock_commands(self, payload):
        """ Lock MapDatabase commands for member in voice channels
"""
        game = self.claims[payload.member.id][0]
        if game in self.locked:
            self.locked.remove(game)
        else:
            self.locked.append(game)
        with open(os.path.join("data", "locked.txt"), "w") as file:
            writer = csv.writer(file)
            writer.writerow(self.locked)


def setup(bot):
    """ Allow lib.bot.__init__.py to add VoiceChannelControl cog
"""
    bot.add_cog(VoiceChannelControl(bot))
