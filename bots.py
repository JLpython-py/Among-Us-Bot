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

        @self.command(name="tasks", pass_context=True)
        async def tasks(ctx):
            ''' Returns a list of all the tasks on the map
'''
            embed = discord.Embed(title="Tasks", color=0x0000ff)
            for i, task in enumerate(self.data['Tasks'], 1):
                embed.add_field(name=i, value=task)
            await ctx.send(embed=embed)

        @self.command(name="task_type", pass_context=True)
        async def task_type(ctx, type_name):
            ''' Returns a list of all the tasks by the type on the map
'''
            tasks = []
            for task in self.data['Tasks']:
                if type_name.title() in self.data['Tasks'][task]['Type']:
                    tasks.append(task)
            if not tasks:
                await ctx.send(f"{type_name} cannot be found")
                await ctx.message.delete()
                return
            embed = discord.Embed(title=f"Task: {type_name}", color=0x0000ff)
            for i, task in enumerate(tasks, 1):
                embed.add_field(name=i, value=task)
            await ctx.send(embed=embed)

        @self.command(name="task", pass_context=True)
        async def task(ctx, name):
            ''' Returns information about a given task
                Returns:
                - Name of task
                - Type of task
                - Locations where the task can be completed
                - Number of steps required to complete the task
'''
            data = None
            for task in self.data['Tasks']:
                if ''.join(name).lower() == ''.join(task.split()).lower():
                    data = self.data['Tasks'][task]
                    break
            if data is None:
                await ctx.send(f"{name} cannot be found")
                await ctx.message.delete()
                return
            data = self.data['Tasks'][task]
            embed = discord.Embed(title=f"Task: {task}", color=0x0000ff)
            for aspect in data:
                embed.add_field(name=aspect, value=data[aspect])
            filename = f"{data['Name']}.png"
            file = discord.File(
                os.path.join('data', self.directory, 'tasks', filename),
                filename)
            embed.set_image(url=f"attachment://{filename}")
            await ctx.send(file=file, embed=embed)

        @self.command(name="locations", pass_context=True)
        async def locations(ctx):
            ''' Returns a list of all the locations on the map
'''
            embed = discord.Embed(title="Locations", color = 0x0000ff)
            for i, room in enumerate(self.data["Locations"], 1):
                embed.add_field(name=i, value=room)
            await ctx.send(embed=embed)

        @self.command(name="location", pass_context=True)
        async def location(ctx, *name):
            ''' Returns information about a given location
                Returns:
                - Name of location
                - Directly connected locations
                - Locations connected by vents
                - Tasks which can be complete in the location
                - Actions which can be cone in the locations
                - Image of location
'''
            data = None
            for location in self.data['Locations']:
                if ''.join(name).lower() == ''.join(location.split()).lower():
                    data = self.data['Locations'][location]
                    break
            if data is None:
                await ctx.send(f"{name} cannot be found")
                await ctx.message.delete()
                return
            embed = discord.Embed(title=f"Location: {location}", color = 0x0000ff)
            for aspect in data:
                embed.add_field(name=aspect, value=data[aspect])
            filename = f"{data['Name']}.png"
            file = discord.File(
                os.path.join('data', self.directory, 'locations', filename),
                filename)
            embed.set_image(url=f"attachment://{filename}")
            await ctx.send(file=file, embed=embed)

        @self.command(name="vents", pass_context=True)
        async def vents(ctx):
            ''' Returns a list of all the vents on the map
'''
            embed = discord.Embed(title="Vents", color=0x0000ff)
            for i, vent in enumerate(self.data["Vents"], 1):
                embed.add_field(name=i, value=vent)
            await ctx.send(embed=embed)

        @self.command(name="vent", pass_context=True)
        async def vent(ctx, *name):
            ''' Returns information about a given vent
                Returns:
                - Name of location
                - Locations connected by vents
'''
            data = None
            for vent in self.data['Vents']:
                if ''.join(name).lower() == ''.join(vent.split()).lower():
                    data = self.data['Vents'][vent]
                    break
            if data is None:
                await ctx.send(f"{name} cannot be found")
                await ctx.message.delete()
                return
            embed = discord.Embed(title=f"Vent: {vent}", color=0x0000ff)
            for aspect in data:
                embed.add_field(name=aspect, value=data[aspect])
            await ctx.send(embed=embed)

        @self.command(name="actions", pass_context=True)
        async def actions(ctx):
            ''' Returns a list of al the actions on the map
'''
            embed = discord.Embed(title="Actions", color=0x0000ff)
            for i, action in enumerate(self.data["Actions"], 1):
                embed.add_field(name=i, value=action)
            await ctx.send(embed=embed)

        @self.command(name="action", pass_contextroo=True)
        async def action(ctx, *name):
            ''' Returns information about a given action
                Returns
                - Name of action
                - Type of action
                - Locations where action can be done
                - Severity of action
'''
            data = None
            for action in self.data['Actions']:
                if ''.join(name).lower() == ''.join(action.split()).lower():
                    data = self.data['Actions'][action]
                    break
            if data is None:
                await ctx.send(f"{name} cannot be found")
                await ctx.message.delete()
                return
            embed = discord.Embed(title=f"Action: {action}", color=0x0000ff)
            for aspect in data:
                embed.add_field(name=aspect, value=data[aspect])
            filename = f"{data['Name']}.png"
            file = discord.File(
                os.path.join('data', self.directory, 'actions', filename),
                filename)
            embed.set_image(url=f"attachment://{filename}")
            await ctx.send(file=file, embed=embed)

class Main:
    def __init__(self):
        ''' Create and run MapBot-class bots for each Among Us map
'''
        self.bots = {
            'Mira HQ': os.environ.get('MIRAHQ'),
            'Polus': os.environ.get('POLUS'),
            'The Skeld': os.environ.get('THESKELD')}
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
