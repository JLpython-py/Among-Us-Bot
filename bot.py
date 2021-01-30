#! python3
# bots.py

"""

"""

import asyncio
import csv
import json
import logging
import random
import re
import os

import discord
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s')


class AUBot(commands.Bot):
    """
"""
    def __init__(self, *, prefix):
        intents = discord.Intents.default()
        intents.members = True
        intents.guilds = True
        commands.Bot.__init__(
            self, command_prefix=prefix, case_insensitive=True,
            intents=intents, self_bot=False)
        self.data = {}
        self.read_files()
        self.add_cog(MapDatabase(self, self.data))
        self.add_cog(RandomAmongUs(self))
        self.add_cog(VoiceChannelControl(self))

    def read_files(self):
        """ Read CSV data for each map
"""
        for maps in ['mirahq', 'polus', 'theskeld']:
            map_data = {}
            directory = os.path.join('data', maps)
            directories = [
                d for d in os.listdir(directory)
                if os.path.isdir(os.path.join(directory, d))
            ]
            for direct in directories:
                csvfile = os.path.join(
                    directory, direct, f"{direct}.csv")
                with open(csvfile) as file:
                    data = list(csv.reader(file))
                    headings = data.pop(0)
                map_data[direct] = {}
                for row in data:
                    info = dict(zip(headings, row))
                    map_data[direct].setdefault(info['Name'], info)
            self.data.setdefault(maps, map_data)

    async def on_ready(self):
        """ Notify that bot is ready
"""
        await self.change_presence(
            activity=discord.Game(name="+help | Among Us"))
        logging.info("Ready: %s", self.user.name)


class RandomAmongUs(commands.Cog):
    """ Generate a random option for various categories in Among Us
"""
    def __init__(self, bot):
        self.bot = bot
        with open(os.path.join('data', 'settings.txt')) as file:
            self.settings = json.load(file)
        self.maps = ["MIRA HQ", "Polus", "The Skeld"]

    @commands.command(name="randomize", pass_context=True, aliases=["r"])
    async def randomize(self, ctx):
        """ Invoke all commands in RandomAmongUs
"""
        for cmd in self.get_commands():
            if cmd.name == "randomize":
                continue
            await ctx.invoke(cmd)

    @commands.command(name="randmap", pass_context=True, aliases=["rm"])
    async def randmap(self, ctx):
        """ Select random map
"""
        num = random.randint(1, 3)
        mapname = random.choice(self.maps)
        embed = discord.Embed(title="Randomize Map", color=0xff0000)
        embed.add_field(name="Map", value=mapname)
        embed.add_field(name="Impostors", value=str(num))
        thumb_name = f"{''.join(mapname.split()).lower()}.png"
        thumb_path = os.path.join(
            'data', thumb_name)
        thumbnail = discord.File(thumb_path, thumb_name)
        embed.set_thumbnail(url=f"attachment://{thumb_name}")
        await ctx.channel.send(file=thumbnail, embed=embed)

    @commands.command(name="randsettings", pass_context=True, aliases=["rs"])
    async def randsettings(self, ctx, setting=''):
        """ Select random option for specified setting
            <setting> can be any of the settings which can be modified in-lobby
            Leaving <setting> blank will randomize all settings
"""
        setting = setting.title()
        options = self.settings.get(setting)
        fields = {}
        if options is None:
            title = "Randomize Setting: ALL"
            for opt in self.settings:
                fields.setdefault(opt, random.choice(self.settings[opt]))
        else:
            title = f"Randomize Setting: {setting}"
            fields.setdefault(setting, random.choice(self.settings[setting]))
        embed = discord.Embed(title=title, color=0xff0000)
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        await ctx.send(embed=embed)


class MapDatabase(commands.Cog):
    """ Allow member to explore available information in Among Us
"""
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.searches = {}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """ Manage response to added reaction
"""
        if payload.member.bot:
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        if payload.member.id == message.author.id:
            return
        if not any([m in embed.footer.text for m in [
            "Airship", "MIRAHQ", "Polus", "TheSkeld"
        ]]):
            return
        if payload.emoji.name in [
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed'
        ]:
            await self.scroll(payload)
        elif payload.emoji.name == u'\u2714':
            await self.retrieve_from_search(payload)
        elif payload.emoji.name == u'\u274c':
            await self.delete_search(payload)

    @commands.group(name="MIRAHQ", case_insensitive=True, pass_context=True,
                    aliases=["MIRA", "MH"])
    async def mira_hq(self, ctx):
        """ Command group to parse information from MIRA HQ data
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid MIRA HQ command passed")

    @mira_hq.group(name="retrieve", pass_context=True, aliases=["r"])
    async def mirahq_retrieve(self, ctx, category, option):
        """ Retrieve option for category in MIRA HQ data
"""
        await self.retrieve(ctx, category, option)

    @mira_hq.group(name="search", pass_context=True, aliases=["s"])
    async def mirahq_search(self, ctx, category):
        """ Search options for category in MIRA HQ data
"""
        await self.search(ctx, category)

    @mira_hq.group(name="listopts", pass_context=True, aliases=["ls"])
    async def mirahq_listopts(self, ctx, category):
        """ List options for category in MIRA HQ data
"""
        await self.listopts(ctx, category)

    @commands.group(name="Polus", case_insensitive=True, pass_context=True,
                    aliases=["P"])
    async def polus(self, ctx):
        """ Command group to parse information from Polus data
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid Polus command passed")

    @polus.group(name="retrieve", pass_context=True, aliases=["r"])
    async def polus_retrieve(self, ctx, category, option):
        """ Retrieve option for category in Polus data
"""
        await self.retrieve(ctx, category, option)

    @polus.group(name="search", pass_context=True, aliases=["s"])
    async def polus_search(self, ctx, category):
        """ Search options for category in Polus data
"""
        await self.search(ctx, category)

    @polus.group(name="listopts", pass_context=True, aliases=["ls"])
    async def polus_listopts(self, ctx, category):
        """ List options for category in Polus data
"""
        await self.listopts(ctx, category)

    @commands.group(name="TheSkeld", case_insensitive=True, pass_context=True,
                    aliases=["Skeld", "TS"])
    async def the_skeld(self, ctx):
        """ Command group to parse information from The Skeld data
"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid The Skeld command passed")

    @the_skeld.group(name="retrieve", pass_context=True, aliases=["r"])
    async def theskeld_retrieve(self, ctx, category, option):
        """ Retrieve option for category in The Skeld data
"""
        await self.retrieve(ctx, category, option)

    @the_skeld.group(name="search", pass_context=True, aliases=["s"])
    async def theskeld_search(self, ctx, category):
        """ Search options for category in The Skeld data
"""
        await self.search(ctx, category)

    @the_skeld.group(name="listopts", pass_context=True, aliases=["ls"])
    async def theskeld_listopts(self, ctx, category):
        """ List options for category in The Skeld data
"""
        await self.listopts(ctx, category)

    async def retrieve(self, ctx, category, option):
        """ Retrieve data for option for category of map
"""
        # Validate category and option
        category, option = category.lower(), option.title()
        mapname = ctx.command.full_parent_name.lower()
        if category not in self.data[mapname]:
            await ctx.send(f"`category={category}` is not valid")
            return
        if option not in self.data[mapname][category]:
            await ctx.send(f"`option={option}` is not valid")
            return
        # Get data from category and option and send in embed
        data = self.data[mapname][category][option]
        embed = discord.Embed(
            title=f"{category.title()}: {option}",
            color=0x0000ff)
        for item in data:
            embed.add_field(name=item, value=data[item])
        embed.set_footer(text=ctx.command.full_parent_name)
        image_name = f"{data['Name']}.png"
        image_path = os.path.join(
            'data', mapname, category, image_name)
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        await ctx.channel.send(file=image, embed=embed)

    async def search(self, ctx, category):
        """ Allow member to scroll through options for category of map
"""
        # Validate category
        category = category.lower()
        mapname = ctx.command.full_parent_name.lower()
        if category not in self.data[mapname]:
            await ctx.send(f"`category={category}` is not valid")
            return
        # Delete any existing search
        if ctx.author.id in self.searches:
            embed = self.searches[ctx.author.id]
            await embed.message.delete()
            del self.searches[ctx.author.id]
        # Create embed for member to scroll data with
        embed = ScrollingEmbed(
            ctx.command.full_parent_name, category, self.data)
        embed.manage_embed()
        await embed.send_with_reactions(ctx.message)
        self.searches.setdefault(ctx.author.id, embed)

    async def listopts(self, ctx, category):
        """ List all options for a category of map
"""
        # Validate category
        category = category.lower()
        mapname = ctx.command.full_parent_name.lower()
        if category not in self.data[mapname]:
            await ctx.send(f"`category={category}` is not valid")
            return
        # Get data for category and send all options in embed
        data = self.data[mapname][category]
        embed = discord.Embed(
            title=category.title(), color=0xff0000)
        for item in data:
            text = '\n'.join([
                f"`{k}`: {v[:20]}..." for k, v in data[item].items()])
            embed.add_field(name=item, value=text)
        embed.set_footer(text=ctx.command.full_parent_name)
        image_name = f"{mapname}.png"
        image_path = os.path.join('data', image_name)
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        await ctx.channel.send(file=image, embed=embed)

    async def retrieve_from_search(self, payload):
        """ Retrieve data for current option of embed
"""
        # Process payload information
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        # Get map and category from embed
        footer_regex = re.compile(
            fr"^({'|'.join([c.name for c in self.get_commands()])}):")
        mapname = footer_regex.search(
            message.embeds[0].footer.text).group(1)
        title_regex = re.compile(
            r"^(.*):")
        category = title_regex.search(
            message.embeds[0].title).group(1).lower()
        # Get data from embed from searches by payload
        option = self.searches.get(payload.member.id).option
        data = self.data[mapname.lower()][category][option]
        # Edit embed to mimic retrieve command
        embed = discord.Embed(
            title=f"{category.title()}: {option.title()}",
            color=0x0000ff)
        for item in data:
            embed.add_field(name=item, value=data[item])
        embed.set_footer(text=mapname)
        image_name = f"{data['Name']}.png"
        image_path = os.path.join(
            'data', mapname.lower(), category, image_name)
        image = discord.File(image_path, image_name)
        embed.set_image(url=f"attachment://{image_name}")
        await channel.send(file=image, embed=embed)
        await message.delete()
        del self.searches[payload.member.id]

    async def scroll(self, payload):
        """ Scroll embed from search command based on the emoji used
"""
        embed = self.searches.get(payload.member.id)
        await embed.scroll(payload)

    async def delete_search(self, payload):
        """ Delete embed from search command
"""
        embed = self.searches.get(payload.member.id)
        await embed.message.delete()
        del self.searches[payload.member.id]


class ScrollingEmbed:
    """ Generate embed which a member can scroll by using reactions
"""
    def __init__(self, name, category, data):
        self.name = name
        self.category = category
        self.items = data[self.name.lower()][self.category]
        self.option = list(self.items)[0]
        self.data = self.items.get(self.option)

        self.embed = None
        self.image = None
        self.message = None
        self.memberid = 0

    def manage_embed(self, index=0):
        """ Edit the existing embed with new data
"""
        # Create embed with data in body and page number in footer
        self.embed = discord.Embed(
            title=f"{self.category.title()}: {self.option}",
            color=0x0000ff)
        self.embed.set_footer(
            text=f"{self.name}: Page {index+1}/{len(self.items)}")
        for item in self.data:
            self.embed.add_field(name=item, value=self.data[item])
        # Attach image to embed
        image_name = f"{self.name.lower()}.png"
        image_path = os.path.join('data', image_name)
        self.image = discord.File(image_path, image_name)
        self.embed.set_image(url=f"attachment://{image_name}")

    async def send_with_reactions(self, message):
        """ Send generated embed and react with designated emojis
"""
        self.memberid = message.author.id
        self.message = await message.channel.send(
            file=self.image, embed=self.embed)
        reactions = [
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed',
            u'\u2714', u'\u274c']
        for rxn in reactions:
            await self.message.add_reaction(rxn)

    async def scroll(self, payload):
        """ Get new data based on emoji used
"""
        # Validate member who reacted requested embed
        if payload.member.id != self.memberid:
            await self.message.remove_reaction(
                payload.emoji, payload.member)
            return
        # Get current index and scroll according to emoji
        index = list(self.items).index(self.option)
        scroll = {
            u'\u23ee': 0, u'\u23ea': index-5, u'\u25c0': index-1,
            u'\u25b6': index+1, u'\u23e9': index+5, u'\u23ed': -1}
        index = scroll.get(payload.emoji.name) % len(self.items)
        # Get new option and new data from new index
        self.option = list(self.items)[index]
        self.data = self.items.get(self.option)
        self.manage_embed(index=index)
        await self.message.edit(embed=self.embed)
        await self.message.remove_reaction(payload.emoji, payload.member)


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


def main():
    """ Run MapBot called AmongUs MapBot on static token
"""
    token = os.environ.get("token", None)
    if token is None:
        with open('token.txt') as file:
            token = file.read()
    assert token is not None
    loop = asyncio.get_event_loop()
    discord_bot = AUBot(prefix="+")
    loop.create_task(discord_bot.start(token))
    loop.run_forever()


if __name__ == '__main__':
    main()
