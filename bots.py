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
        self.categories = ['actions', 'locations', 'tasks', 'vents']
        self.data = {}
        self.scrolling_embeds = {}
        self.read_files()
        self.execute_commands()

    def read_files(self):
        ''' Read CSV data for each map
'''
        for cat in self.categories:
            path = os.path.join('data', self.directory, cat, f"{cat}.csv")
            with open(path) as file:
                data = list(csv.reader(file))
                headings = data.pop(0)
            self.data[cat] = {}
            for row in data:
                info = dict(zip(headings, row))
                self.data[cat].setdefault(
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
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed']:
            scrolling_embed = self.scrolling_embeds[payload.member.id]
            await scrolling_embed.scroll(payload)
        elif name == u'\u274c':
            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            del self.scrolling_embeds[payload.member.id]
            await message.delete()

    def map_information_embed(self, data, option, category):
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
        return image, embed

    def execute_commands(self):
        ''' MapBot-class commands which can be used by members
'''
        @self.command(name="actions", pass_context=True, aliases=["a"])
        async def actions(ctx, option=''):
            actions = self.data.get('actions')
            option = option.title()
            data = actions.get(option)
            if data is None:
                embed = ScrollingEmbed(
                    self.directory, ctx.message, self.data,
                    category='actions')
                await embed.create()
                self.scrolling_embeds.setdefault(
                    ctx.message.author.id, embed)
                await ctx.message.delete()
            else:
                image, embed = self.map_information_embed(
                    data, option,
                    category='actions')
                await ctx.send(file=image, embed=embed)

        @self.command(name="locations", pass_context=True, aliases=["l"])
        async def locations(ctx, option=''):
            actions = self.data.get('locations')
            option = option.title()
            data = actions.get(option)
            if data is None:
                embed = ScrollingEmbed(
                    self.directory, ctx.message, self.data,
                    category='locations')
                await embed.create()
                self.scrolling_embeds.setdefault(
                    ctx.message.author.id, embed)
                await ctx.message.delete()
            else:
                image, embed = self.map_information_embed(
                    data, option,
                    category='locations')
                await ctx.send(file=image, embed=embed)

        @self.command(name="tasks", pass_context=True, aliases=["t"])
        async def tasks(ctx, option=''):
            actions = self.data.get('tasks')
            option = option.title()
            data = actions.get(option)
            if data is None:
                embed = ScrollingEmbed(
                    self.directory, ctx.message, self.data,
                    category='tasks')
                await embed.create()
                self.scrolling_embeds.setdefault(
                    ctx.message.author.id, embed)
                await ctx.message.delete()
            else:
                image, embed = self.map_information_embed(
                    data, option,
                    category='tasks')
                await ctx.send(file=image, embed=embed)

        @self.command(name="vents", pass_context=True, aliases=["v"])
        async def vents(ctx, option=''):
            actions = self.data.get('vents')
            option = option.title()
            data = actions.get(option)
            if data is None:
                embed = ScrollingEmbed(
                    self.directory, ctx.message, self.data,
                    category='vents')
                await embed.create()
                self.scrolling_embeds.setdefault(
                    ctx.message.author.id, embed)
                await ctx.message.delete()
            else:
                image, embed = self.map_information_embed(
                    data, option,
                    category='vents')
                await ctx.send(file=image, embed=embed)

class ScrollingEmbed:
    def __init__(self, directory, message, data, category):
        self.message = message
        self.channel = self.message.channel
        self.memberid = self.message.author.id
        self.directory = directory
        self.category = category
        self.items = data.get(self.category)
        self.option = list(self.items)[0]
        self.data = self.items.get(self.option)

    async def create(self):
        self.embed = discord.Embed(
            title=f"{self.category.title()}: {self.option}",
            color=0x0000ff)
        for item in self.data:
            self.embed.add_field(name=item, value=self.data[item])
        image_name = f"{self.data['Name']}.png"
        image_path = os.path.join(
            'data', self.directory, self.category, image_name)
        image = discord.File(image_path, image_name)
        self.embed.set_image(url=f"attachment://{image_name}")
        self.embed.set_footer(
            text=f"Page 1/{len(self.items)}")
        self.message = await self.channel.send(file=image, embed=self.embed)
        reactions = [
            u'\u23ee', u'\u23ea', u'\u25c0', u'\u25b6', u'\u23e9', u'\u23ed',
            u'\u274c']
        for rxn in reactions:
            await self.message.add_reaction(rxn)

    async def scroll(self, payload):
        #Verify that the member requested the embed
        if payload.member.id != self.memberid:
            await self.message.remove_reaction(
                payload.emoji, payload.member)
            return
        index = list(self.items).index(self.option)
        scroll = {
            u'\u23ee': 0, u'\u23ea': index-5, u'\u25c0': index-1,
            u'\u25b6': index+1, u'\u23e9': index+5, u'\u23ed': -1}
        index = scroll.get(payload.emoji.name)%len(self.items)
        self.option = list(self.items)[index]
        self.data = self.items.get(self.option)
        self.embed = discord.Embed(
            title=f"{self.category.title()}: {self.option}",
            color=0x0000ff)
        for item in self.data:
            self.embed.add_field(name=item, value=self.data[item])
        image_name = f"{self.data['Name']}.png"
        image_path = os.path.join(
            'data', self.directory, self.category, image_name)
        image = discord.File(image_path, image_name)
        self.embed.set_image(url=f"attachment://{image_name}")
        self.embed.set_footer(
            text=f"Page {index+1}/{len(self.items)}")
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
