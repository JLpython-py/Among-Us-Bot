#! python3
# lib.bot.__init__.py

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

import glob
import logging
import os

import discord
from discord.ext import commands

from lib.db import db

logging.basicConfig(
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s')


class BotRoot(commands.Bot):
    """ Create commands.Bot Discord bot and set up cogs
"""
    def __init__(self, prefix="+"):
        intents = discord.Intents.default()
        intents.members = True
        intents.guilds = True
        super().__init__(
            command_prefix=prefix, case_insensitive=True,
            intents=intents
        )
        self.airship = db.AirshipDB()
        self.mirahq = db.MIRAHQDB()
        self.polus = db.PolusDB()
        self.theskeld = db.TheSkeldDB()
        self.load_all_cogs()

    def load_all_cogs(self):
        """ Load all cogs in lib/cogs as extensions
"""
        cog_paths = [
            [d, os.path.splitext(f)]
            for d, f in [
                os.path.split(p)
                for p in glob.glob("lib/cogs/*.py")
            ]
        ]
        for path in cog_paths:
            cog = path[1][0]
            self.load_extension(f"lib.cogs.{cog}")
            setattr(self, cog, False)
            logging.info("Cog Loaded: %s", cog)
        logging.info("Loaded all cogs in lib/cogs")

    async def on_ready(self):
        """ Notify logging of event reference
            Change bot status message
"""
        logging.info("Ready: %s", self.user.name)
        await self.change_presence(
            activity=discord.Game("Among Us | +"))
