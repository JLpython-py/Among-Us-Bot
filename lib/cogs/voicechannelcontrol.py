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
import json
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
        self.disabled = []

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
            await self.yield_control(member)
            await direct_message.send(
                f"{member.mention}: All claims forcefully yielded after voice channel disconnect"
            )
        # Check if member is AFK
        if after.afk:
            await self.yield_control(member)
            await direct_message.send(
                f"{member.mention}: All claims forcefully yielded after AFK"
            )

    @commands.command(
        name="claim", case_insensitive=True, pass_context=True
    )
    async def claim(self, ctx):
        """ Invoke a request to claim voice channels
"""
        await ctx.message.delete()
        # Verify member does not have a voice channel claim
        if ctx.author.id in self.claims:
            await ctx.send("You already have a voice channel claim")
            return
        # Prompt member to select a voice channel for a Game Lobby
        game = await self.claim_voice_channel(ctx, style="Game Lobby")
        if game is None:
            return
        self.claims[ctx.author.id] = [game]
        # Prompt member to optionally select a voice channel for a Ghost Lobby
        ghost = await self.claim_voice_channel(ctx, style="Ghost Lobby")
        if ghost is None:
            await self.voice_control(ctx, game=game, ghost=None)
        else:
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
        await ctx.message.delete()
        message = await ctx.channel.send(embed=embed)
        await asyncio.sleep(10)
        await message.delete()

    @commands.command(
        name="locked", case_insensitive=True, pass_context=True
    )
    async def locked(self, ctx):
        """ Check if MapDatabase commands are locked for member
"""
        locked = self.check_commands(ctx)
        embed = discord.Embed(
            title="Commands Enabled/Disabled Check",
            color=0x0000ff
        )
        embed.add_field(
            name="Member", value=ctx.author.mention
        )
        embed.add_field(
            name="`MapDatabase` Commands Locked?", value=f"`{locked}`"
        )
        await ctx.message.delete()
        message = await ctx.channel.send(embed=embed)
        await asyncio.sleep(10)
        await message.delete()

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
            "Close": "React with :x:"
        }
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        embed.set_footer(
            text="This message will automatically close after 10s"
        )
        message = await ctx.channel.send(embed=embed)
        for chan in voice_channels:
            await message.add_reaction(
                self.emojis[voice_channels.index(chan)]
            )
        await message.add_reaction(u"\u274c")
        # Wait for member to select a voice channel
        try:
            payload = await self.bot.wait_for(
                "raw_reaction_add", timeout=10.0,
                check=lambda p: (
                        p.member.id == ctx.author.id
                        and p.message_id == message.id
                )
            )
            await message.delete()
            if payload.emoji.name == u"\u274c":
                return
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
        # Get Game Lobby and Ghost Lobby reactions and fields
        with open(
                os.path.join("data", "VoiceChannelControl", "vcc_content.txt")
        ) as file:
            data = json.load(file)
        if ghost is None:
            reactions = data["game"]["reactions"]
            fields = data["game"]["fields"]
            fields["Claimed"] = fields["Claimed"].format(game.name)
        else:
            ghost = self.bot.get_channel(id=ghost)
            reactions = data["ghost"]["reactions"]
            fields = data["ghost"]["fields"]
            fields["Claimed"] = fields["Claimed"].format(game.name, ghost.name)
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
                if await self.verify_activity(ctx):
                    continue
                break
            # Call functions according to emoji used
            if payload.emoji.name in [u"\U0001F507", u"\U0001F508"]:
                await self.manage_mute(payload)
            elif payload.emoji.name in [u"\U0001F515", u"\U0001F514"]:
                await self.manage_deafen(payload)
            elif payload.emoji.name == u"\U0001F47B":
                await self.move_member(payload, dest="Ghost Lobby")
            elif payload.emoji.name == u"\U0001F3E5":
                await self.move_member(payload, dest="Game Lobby")
            elif payload.emoji.name == u"\U0001F504":
                await self.reset_game(payload.member)
            elif payload.emoji.name == u"\U0001F3F3":
                await self.yield_control(payload.member)
                await ctx.channel.send(
                    f"{ctx.author.mention}: All claims yielded successfully"
                )
                break
            elif payload.emoji.name == u"\U0001F512":
                await self.lock_commands(payload.member)
            await message.remove_reaction(payload.emoji, payload.member)
        await message.delete()

    async def verify_activity(self, ctx):
        """ Verify member with claim is still active
"""
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
            return True
        # Forcefully yield voice channel claim
        except asyncio.TimeoutError:
            await check.clear_reactions()
            await self.yield_control(ctx.author)
            await check.edit(
                content=f"{ctx.author.mention}: All claims yielded due to inactivity"
            )
            return False

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

    async def move_member(self, payload, dest):
        """ Move members to and from Game Lobby/Ghost Lobby
"""
        # Get channel of payload and claimed voice channels
        channel = self.bot.get_channel(payload.channel_id)
        game, ghost = [
            self.bot.get_channel(id=c)
            for c in self.claims[payload.member.id]
        ]
        # Get destination voice channel and members who can be moved
        if dest == "Ghost Lobby":
            new_vc = ghost
            member_list = [m for m in game.members if m.id not in self.claims][:10]
        elif dest == "Game Lobby":
            new_vc = game
            member_list = ghost.members[:10]
        else:
            return
        if not member_list:
            await channel.send("There are no members who can be moved")
            return
        # Send embed with options and reactions to move members
        embed = discord.Embed(
            title=f"Move members to `{dest}`", color=0x0000ff
        )
        fields = {
            "Select Members": '\n'.join([
                f"{self.emojis[member_list.index(m)]} - {m}"
                for m in member_list
            ]),
            "Move Members": "Selected members will be moved once this message closes."
        }
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        embed.set_footer(
            text="This message with automatically close when stale for 5s."
        )
        message = await channel.send(embed=embed)
        for mem in member_list:
            await message.add_reaction(
                self.emojis[member_list.index(mem)]
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
        # Move members according to message reactions
        message = await channel.fetch_message(message.id)
        for rxn in message.reactions:
            async for user in rxn.users():
                # Ignore reaction if only added by bot
                if user.id == payload.member.id:
                    await member_list[
                        self.emojis.index(rxn.emoji)
                    ].move_to(new_vc)
        await message.delete()

    async def reset_game(self, member):
        """ Revert member properties to defaults
"""
        game = self.bot.get_channel(
            id=self.claims[member.id][0]
        )
        # If Ghost Lobby exists, move all members to Game Lobby
        if len(self.claims[member.id]) == 2:
            ghost = self.bot.get_channel(
                id=self.claims[member.id][1]
            )
            for mem in ghost.members:
                await mem.move_to(game)
        # Unmute and Undeafen all members
        for mem in game.members:
            await mem.edit(mute=False, deafen=False)

    async def yield_control(self, member):
        """ Yield control of voice channel claims
"""
        # Reset voice channel(s)
        await self.reset_game(member)
        # Delete channel from list of locked voice channels
        game = self.claims[member.id][0]
        if game in self.disabled:
            self.disabled.remove(game)
        # Delete channel from claimed channels
        del self.claims[member.id]

    async def lock_commands(self, member):
        """ Lock MapDatabase commands for member in voice channels
"""
        game = self.claims[member.id][0]
        if game in self.disabled:
            self.disabled.remove(game)
        else:
            self.disabled.append(game)

    def check_commands(self, ctx):
        """ Check if MapDatabase commands are disabled for member
"""
        for vcid in self.disabled:
            voice_channel = discord.utils.get(
                ctx.guild.voice_channels, id=vcid
            )
            if voice_channel is None:
                continue
            if ctx.author in voice_channel.members:
                return True
        return False


def setup(bot):
    """ Allow lib.bot.__init__.py to add VoiceChannelControl cog
"""
    bot.add_cog(VoiceChannelControl(bot))
