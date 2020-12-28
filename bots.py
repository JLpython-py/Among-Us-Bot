#! python3
# bots.py

import asyncio
import csv
import logging
import re
import os

import discord
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

class MapBot(commands.Bot):
    def __init__(self, *, command_prefix, name, directory):
        '''
'''
        self.client = discord.Client()
        commands.Bot.__init__(
            self, command_prefix=command_prefix, self_bot=False)
        self.name = name
        self.directory = directory
        self.data = {}
        self.scrolling_embeds = {}
        self.read_files()
        self.execute_commands()

    def read_files(self):
        ''' Read CSV data for each map
'''
        dirpath = os.path.join('data', self.directory)
        directories = [d for d in os.listdir(dirpath)\
                       if os.path.isdir(os.path.join(dirpath, d))]
        for direct in directories:
            csvfile = os.path.join(dirpath, direct, f"{direct}.csv")
            with open(csvfile) as file:
                data = list(csv.reader(file))
                headings = data.pop(0)
            self.data[direct] = {}
            for row in data:
                info = dict(zip(headings, row))
                self.data[direct].setdefault(
                    info['Name'], info)

    async def on_ready(self):
        ''' Notify developer that a MapBot-class bot is active
'''
        logging.info("Ready: %s", self.name)

    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        name = payload.emoji.name
        if name in [
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9',
            u'\u23ed']:
            embed = self.scrolling_embeds[payload.member.id]
            await embed.scroll(payload)
        elif name == u'\u274c':
            embed = self.scrolling_embeds[payload.member.id]
            await embed.message.delete()
            del self.scrolling_embeds[payload.member.id]

    async def map_information(self, ctx, *, category, option):
        items = self.data.get(category)
        option = option.title()
        data = items.get(option)
        if data is None:
            embed = ScrollingEmbed(
                self.directory, ctx.message, self.data,
                category=category)
            embed.manage_embed()
            await embed.send_with_reactions()
            if ctx.message.author.id in self.scrolling_embeds:
                embed = self.scrolling_embeds[ctx.message.author.id]
                await embed.message.delete()
                del self.scrolling_embeds[ctx.message.author.id]
            self.scrolling_embeds[ctx.message.author.id] = embed
            await ctx.message.delete()
        else:
            embed = discord.Embed(
                title=f"{category.title()}: {option}",
                color=0x0000ff)
            for item in data:
                embed.add_field(name=item, value=data[item])
            image_name = f"{data['Name']}.png"
            image_path = os.path.join(
                'data', self.directory, category, image_name)
            image = discord.File(image_path, image_name)
            embed.set_image(url=f"attachment://{image_name}")
            await ctx.send(file=image, embed=embed)
            await ctx.message.delete()

    def execute_commands(self):
        ''' MapBot-class commands which can be used by members
'''
        @self.command(name="actions", pass_context=True, aliases=["a"])
        async def actions(ctx, option=''):
            await self.map_information(
                ctx, category='actions', option=option)

        @self.command(name="locations", pass_context=True, aliases=["l"])
        async def locations(ctx, option=''):
            await self.map_information(
                ctx, category='locations', option=option)

        @self.command(name="tasks", pass_context=True, aliases=["t"])
        async def tasks(ctx, option=''):
            await self.map_information(
                ctx, category='tasks', option=option)

        @self.command(name="vents", pass_context=True, aliases=["v"])
        async def vents(ctx, option=''):
            await self.map_information(
                ctx, category='vents', option=option)

        @self.command(name="maps", pass_context=True, aliases=["m"])
        async def maps(ctx, option=''):
            await self.map_information(
                ctx, category='maps', option=option)

class ScrollingEmbed:
    def __init__(self, directory, message, data, category):
        self.channel = message.channel
        self.memberid = message.author.id
        self.directory = directory
        self.category = category
        self.items = data.get(self.category)

    def manage_embed(self, index=0):
        self.option = list(self.items)[index]
        self.data = self.items.get(self.option)
        self.embed = discord.Embed(
            title=f"{self.category.title()}: {self.option}",
            color=0x0000ff)
        self.embed.set_footer(
            text=f"Page {index+1}/{len(self.items)}")
        for item in self.data:
            self.embed.add_field(name=item, value=self.data[item])
        image_name = f"{self.data['Name']}.png"
        image_path = os.path.join(
            'data', self.directory, self.category, image_name)
        self.image = discord.File(image_path, image_name)
        self.embed.set_image(url=f"attachment://{image_name}")

    async def send_with_reactions(self):
        self.message = await self.channel.send(
            file=self.image, embed=self.embed)
        reactions = [
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed',
            u'\u274c']
        for rxn in reactions:
            await self.message.add_reaction(rxn)

    async def scroll(self, payload):
        if payload.member.id != self.memberid:
            await self.message.remove_reaction(
                payload.emoji, payload.member)
            return
        index = list(self.items).index(self.option)
        scroll = {
            u'\u23ee': 0, u'\u23ea': index-5, u'\u25c0': index-1,
            u'\u25b6': index+1, u'\u23e9': index+5, u'\u23ed': -1}
        index = scroll.get(payload.emoji.name)%len(self.items)
        self.manage_embed(index=index)
        await self.message.edit(embed=self.embed)
        await self.message.remove_reaction(payload.emoji, payload.member)
        
class Main:
    def __init__(self):
        ''' Create and run MapBot-class bots for each Among Us map
'''
        self.bots = {
            'MIRA HQ': os.environ.get('MIRAHQ', None),
            'Polus': os.environ.get('POLUS', None),
            'The Skeld': os.environ.get('THESKELD', None),
            'Airship': os.environ.get('AIRSHIP', None)}
        if None in self.bots.values():
            with open(os.path.join('data', 'tokens.csv')) as file:
                self.bots = dict(list(csv.reader(file, delimiter='\t')))
        self.loop = asyncio.get_event_loop()
        for bot in self.bots:
            directory = ''.join(bot.split())
            prefix, token = f"{directory}.", self.bots[bot]
            discord_bot = MapBot(
                command_prefix=prefix, name=bot, directory=directory)
            self.loop.create_task(discord_bot.start(token))
        self.loop.run_forever()

if __name__ == '__main__':
    Main()
