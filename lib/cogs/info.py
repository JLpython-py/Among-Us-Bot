#! python3
# info.py

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

import logging

import discord
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(levelname)s - %(message)"
)


class Info(commands.Cog):
    """ General bot info
"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="info"
    )
    async def stats(self, ctx):
        app_info = await self.bot.application_info()
        embed = discord.Embed(
            title="Bot Application Info",
            color=0x0000ff
        )
        logging.info(app_info)
        fields = {
            "ID": app_info.id, "Name": app_info.name, "Owner": app_info.owner,
            "Team": app_info.team, "Description": app_info.description,
            "Bot Public": app_info.bot_public,
            "Bot Require Code Grant": app_info.bot_require_code_grant,
        }
        for field in fields:
            embed.add_field(name=field, value=fields[field])
        embed.set_image(url=app_info.cover_image_url_as(format="png"))
        await ctx.channel.send(embed=embed)


def setup(bot):
    """ Add Info cog
"""
    bot.add_cog(Info(bot))
