#! python3
# bots.py

import asyncio
import csv
import logging
import os

import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

class MapBot(commands.Bot):
    def __init__(self, *, command_prefix, name, directory):
        '''
'''
        self.client = discord.Client()
        commands.Bot.__init__(
            self, command_prefix=command_prefix, self_bot=False)
        self.name = name
        self.directory = directory
        self.files = {
            'Actions': os.path.join('data', self.directory, 'actions.csv'),
            'Locations': os.path.join('data', self.directory, 'locations.csv'),
            'Tasks': os.path.join('data', self.directory, 'tasks.csv'),
            'Vents': os.path.join('data', self.directory, 'vents.csv')}
        self.data = {}
        self.read_files()
        self.execute_commands()

    def read_files(self):
        ''' Read CSV data for each map
'''
        for category in self.files:
            with open(self.files[category]) as file:
                data = list(csv.reader(file, delimiter='\t'))
                headings = data.pop(0)
            self.data[category] = {}
            for row in data:
                info = dict(zip(headings, row))
                self.data[category].setdefault(info['Name'], info)

    async def on_ready(self):
        ''' Notify developer that a MapBot-class bot is active
'''
        print(f"Bot is ready: {self.name}")

    def execute_commands(self):
        ''' MapBot-class commands which can be used by members
'''
        @self.command(name="map", pass_context=True)
        async def map(ctx):
            ''' Returns a high-detailed image of the corresponding map
'''
            embed = discord.Embed(title="Map", color=0x0000ff)
            file = discord.File(
                os.path.join('data', self.directory, "Map.png"),
                "Map.png")
            embed.set_image(url="attachment://Map.png")
            await ctx.send(file=file, embed=embed)

        @self.command(name="sabotage_map", pass_context=True)
        async def sabotage_map(ctx):
            ''' Returns an image of the sabotage map of the corresponding map
'''
            embed = discord.Embed(title="Sabotage Map", color=0x0000ff)
            file = discord.File(
                os.path.join('data', self.directory, "SabotageMap.png"),
                "SabotageMap.png")
            embed.set_image(url="attachment://SabotageMap.png")
            await ctx.send(file=file, embed=embed)

        @self.command(name="list", pass_context=True)
        async def list(ctx, category):
            category = category.title()
            if category not in self.data:
                await ctx.send(f"{category} cannot be found")
                return
            embed = discord.Embed(title=category, color=0x0000ff)
            for i, cat in enumerate(self.data[category], 1):
                embed.add_field(name=i, value=cat)
            await ctx.send(embed=embed)

        @self.command(name="get", pass_context=True)
        async def get(ctx, category, name):
            category, name = category.title(), name.title()
            dirname = category.lower()
            if category not in self.data:
                await ctx.send(f"{category} cannot be found")
                return
            data = self.data[category].get(name)
            if data is None:
                await ctx.send(f"{name} cannot be found in {category}")
            embed = discord.Embed(title=f"{category}: {name}", color=0x0000ff)
            for aspect in data:
                embed.add_field(name=aspect, value=data[aspect])
            filename = f"{data['Name']}.png"
            file = discord.File(
                os.path.join(
                    'data', self.directory, dirname, filename),
                filename)
            embed.set_image(url=f"attachment://{filename}")
            await ctx.send(file=file, embed=embed)

class Main:
    def __init__(self):
        ''' Create and run MapBot-class bots for each Among Us map
'''
        self.bots = {
            'Mira HQ': os.environ.get('MIRAHQ', None),
            'Polus': os.environ.get('POLUS', None),
            'The Skeld': os.environ.get('THESKELD', None)}
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
