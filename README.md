# AmongUs-MapBot

<img alt="Discord" src="https://img.shields.io/discord/772273631677251625?label=Among%20Us%20Discord%20Server&style=plastic">

Preface: If you have no idea what Among Us is, check out the game's [Wiki](https://among-us.fandom.com/wiki/Among_Us_Wiki), the [Among Us Twitter profile](https://twitter.com/AmongUsGame?s=20), or the [Innersloth devlopers Twitter profile](https://twitter.com/InnerslothDevs?s=20).

The goal of these Discord Bots was to create an easily accessible database for each of the Among Us maps. Note: the Discord bots which are run using *bots.py* are referred to as MapBot-class bots or simply MapBots. Each of these MapBots has its own directory in _data/_ loaded with all the relevant information I could find. For my Discord Server, the one above, three (soon to be four) MapBots are used, one for each map (Mira HQ, Polus, and The Skeld). While more could obviously be used, I cannot think of any reason why more would be needed.

## Installation

Use the below links to add the bots to your server:
 - [Airship](https://discord.com/api/oauth2/authorize?client_id=778735317154791475&permissions=124928&scope=bot)
 - [MiraHQ](https://discord.com/api/oauth2/authorize?client_id=773039813396791296&permissions=124928&scope=bot)
 - [Polus](https://discord.com/api/oauth2/authorize?client_id=773040583324467220&permissions=124928&scope=bot)
 - [TheSkeld](https://discord.com/api/oauth2/authorize?client_id=772928466260590663&permissions=124928&scope=bot)

Each will need the following permissions turned on, but only in the channel(s) they will be used in:
 - Send Messages
 - Manage Messages
 - Embed Links
 - Attach Files
 - Read Message History

I recommend creating a role for all the MapBots and using that role to restrict the bots to certain channels.

## Basic Usage

There is currently one MapBot per active Among Us map. While the prefixes for each bot is somewhat long, it is much easier to memorize than random symbols. The bot prefixes are as follows:
 - (Coming Soon) Airship: _Airship._
 - Mira HQ: _MiraHQ._
 - Polus: _Polus._
 - The Skeld: _TheSkeld._
 
 Each bot has the same number and type of commands, but they each reference unique sets of data.

## Commands

While there are only four commands available to each bot, they total amount of data which they cover is a bit suprising. The intention was to distribute the data amongst the commands in the most logical, yet user-friendly way possible.

_map_

The 'map' command simply returns the corresponding map, with annotations. The maps can be found [here](https://gameplay.tips/guides/8482-among-us.html). Credit to **u/mooseknuckle_king**, **u/SuperInkyGD**, and **u/Vici_Finis** for these maps.

_sabotage\_map_

The 'sabotage_map' command is even simpler, only returning a screenshot of the corresponding sabotage map, for reference.

_list_ **category**

The 'list' command returns all options for the given **category** argument. The available **category** options are: 
 - Actions
 - Locations
 - Tasks
 - Vents

_get_ **category** **name**

The most extensive of the three commands, the 'get' command returns data found in the corresponding CSV files, along with the appropriate image. The options for **name** depend on the **category** argument, but are the same items which are returned by the 'list' command with the same **category** argument.
