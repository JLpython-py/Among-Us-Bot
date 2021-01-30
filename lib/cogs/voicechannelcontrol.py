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
import re

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
    async def on_raw_reaction_add(self, payload):
        """ Listen for member using emojis to control others members' voices
"""
        logging.info("Raw Reaction Add: %s", payload)
        if payload.member.bot:
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        if message.author.id != self.bot.user.id or\
           "VoiceChannelControl" not in embed.footer.text:
            return
        if payload.emoji.name in [u"\U0001F507", u"\U0001F508"]:
            await self.manage_voices(payload)
        elif payload.emoji.name == u"\U0001F47B":
            await self.member_dead(payload)
        elif payload.emoji.name == u"\U0001F3E5":
            await self.member_alive(payload)
        elif payload.emoji.name == u"\U0001F504":
            await self.reset_game(payload)
        elif payload.emoji.name == u"\U0001F3F3":
            await self.yield_control(payload)

    @commands.command(name="claim", pass_context=True)
    async def claim(self, ctx):
        """ Invoke a claim request panel
            Member cannot have an active claim request
            Member cannot have a claim on another voice channel
"""
        if ctx.author.id in self.claims:
            await ctx.send("You already have a voice channel claim")
            return
        game_pay = await self.claim_voice_channel(
            ctx, style="Game Lobby"
        )
        if game_pay is None:
            return
        ghost_pay = await self.claim_voice_channel(
            ctx, style="Ghost Lobby"
        )
        if ghost_pay is None:
            return
        await self.voice_control(ctx)

    async def claim_voice_channel(self, ctx, *, style):
        """ Send an embed with reactions for member to designate a lobby VC
"""
        def check(pay):
            return pay.member.id == ctx.author.id

        voice_channels = ctx.guild.voice_channels[:10]\
            if len(ctx.guild.voice_channels) > 10\
            else ctx.guild.voice_channels
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
            "Cancel": "This message will automatically close after 60s"
        }
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        embed.set_footer(
            text=f"VoiceChannelControl | {ctx.author.id}"
        )
        message = await ctx.channel.send(embed=embed)
        for channel in voice_channels:
            await message.add_reactions(
                self.emojis[voice_channels.index(channel)]
            )
        try:
            payload = await self.bot.wait_for(
                "raw_reaction_add", timeout=60.0,
                check=check
            )
            return payload
        except asyncio.TimeoutError:
            await message.delete()

    async def voice_control(self, payload):
        voice_channel = payload.member.guild.voice_channels[
            self.emojis.index(payload.emoji.name)]
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        self.claims.setdefault(payload.member.id, voice_channel.id)
        embed = discord.Embed(
            title="Voice Channel Control", color=0x0000ff)
        fields = {
            "Claimed": f"You have successfully claimed {voice_channel.name}",
            "Voice Channel Control": '\n'.join([
                "Mute all - :mute:", "Unmute all - :speaker:",
                "Yield - :flag_white:"])}
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        embed.set_footer(text="VoiceChannelControl")
        await message.edit(embed=embed)
        await message.clear_reactions()
        reactions = [
            u"\U0001F507", u"\U0001F508", u"\U0001F47B",
            u"\U0001F3E5", u"\U0001F504", u"\U0001F3F3"]
        for reaction in reactions:
            await message.add_reaction(reaction)

    async def cancel_claim(self, payload):
        """ Cancel member request to claim a voice channel
"""
        # Get channel and message information from payload
        channel = discord.utils.get(
            payload.member.guild.channels, id=payload.channel_id
        )
        message = await channel.fetch_message(payload.message_id)
        # Verify payload member is the member who requested
        embed = message.embeds[0]
        footer_regex = re.compile(
            r"^VoiceChannelControl \| (.*)"
        )
        if int(
                footer_regex.search(embed.footer.text).group(1)
        ) != payload.member.id:
            await channel.send(
                "You did not request this voice channel claim"
            )
            return
        # Delete voice channel claim panel
        await message.clear_reactions()
        embed = discord.Embed(
            title="Voice Channel Claim Canceled",
            color=0x0000ff
        )
        await message.edit(embed=embed)
        await asyncio.sleep(10)
        await message.delete()

    async def manage_voices(self, payload):
        channel = self.bot.get_chanel(payload.channel_id)
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
        pass

    async def member_alive(self, payload):
        pass

    async def reset_game(self, payload):
        pass

    async def yield_control(self, payload):
        """ Yield control of a claimed voice channel
"""
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.member.id)
        # Delete voice control message
        voice_channel = self.bot.get_channel(
            self.claims.get(payload.member.id)
        )
        embed = discord.Embed(
            title="Voice Channel Control Panel Close",
            color=0x0000ff
        )
        embed.add_field(
            name="Yielded",
            value=f"You have successfully yielded {voice_channel.name}"
        )
        await message.edit(embed=embed)
        await message.clear_reactions()
        del self.claims[payload.member.id]
        await asyncio.sleep(10)
        await message.delete()


def setup(bot):
    """ Allow lib.bot.__init__.py to add VoiceChannelControl cog
"""
    bot.add_cog(VoiceChannelControl(bot))
