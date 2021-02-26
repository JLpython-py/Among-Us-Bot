# Among-Us-Bot

![GitHub last commit](https://img.shields.io/github/last-commit/JLpython-py/Among-Us-Bot)
![GitHub repo size](https://img.shields.io/github/repo-size/JLpython-py/Among-Us-Bot)
![GitHub issues](https://img.shields.io/github/issues/JLpython-py/Among-Us-Bot)
![GitHub issues by-label](https://img.shields.io/github/issues/JLpython-py/Among-Us-Bot/enhancement)
![GitHub pull requests](https://img.shields.io/github/issues-pr/JLpython-py/Among-Us-Bot)
![GitHub deployments](https://img.shields.io/github/deployments/JLpython-py/Among-Us-Bot/GitHub-pages)
![GitHub](https://img.shields.io/github/license/JLpython-py/Among-Us-Bot)

![Among Us](https://user-images.githubusercontent.com/72679601/105618817-8441fe00-5da0-11eb-97ee-4756d629d01a.png)

The Among Us Bot is a Discord bot built with `discord.py`.
The bot is equipped with multiple features related to the game of Among Us.
These features are intended to be supplemental to the game itself, in order to enhance the experience of the game.

***

## Cogs

- [Info](#info)
- [MapDatabase](#map-database)
- [RandomAmongUs](#random-among-us)
- [VoiceChannelControl](#voice-channel-control)

### Info

[**Info** Cog Command Guide](https://github.com/JLpython-py/Among-Us-Bot/wiki/MapDatabase).

### Map Database

![TheSkeld retrieve tasks "Divert Power"](https://user-images.githubusercontent.com/72679601/108528698-8bb5d380-7288-11eb-88c1-7518629a5a25.png)

Stored in this repository is data about nearly all aspects of the Among Us maps.
The `MapDatabase` cog allows guild members to reference this data.

[**MapDatabase** Cog Command Guide](https://github.com/JLpython-py/Among-Us-Bot/wiki/MapDatabase).

*Note*:
The data used by the bot is stored in a SQLite database, which requires additional software to view.
The same data has been written to CSV files which can be easily read.
These files can be found in the [AmongUsData](https://github.com/JLpython-py/AmongUsData/) GitHub repository.
Also, if there are any typos in the data, please report them as an Issue in this repository.
Any help is greatly appreciated.

### Random Among Us

![randmap](https://user-images.githubusercontent.com/72679601/107803852-070f0680-6d18-11eb-957f-a308cdda62e6.png)
![randsettings](https://user-images.githubusercontent.com/72679601/107803865-0d04e780-6d18-11eb-9446-0497fd222cd9.png)

Just like the name implies, this feature allows members to generate random apsects of Among Us.
Currently supported is the generation of a random map and number of impostors and the generation of a random option for a specific or all of the in-lobby settings.

[**RandomAmongUs** Cog Command Guide](https://github.com/JLpython-py/Among-Us-Bot/wiki/RandomAmongUs).

### Voice Channel Control

![claim](https://user-images.githubusercontent.com/72679601/107803946-2b6ae300-6d18-11eb-9da6-e59318d692f6.png)
![Voice Channel Claim Control](https://user-images.githubusercontent.com/72679601/108528722-91abb480-7288-11eb-9b35-3a262af7b8b4.png)
Members can claim control of one voice channel and designate it as a **Game Lobby**.
Optionally, they can also claim control of a second voice channel and designate it as a **Ghost Lobby**.
With control, members with claims can control the properties of other members in the **Game Lobby**.
Members with claims are able to mute/un-mute members, deafen/un-deafen members, and move members between the two voice channels, if applicable.
Lastly, members with claims will be able to lock the `MapDatabase` commands.
In doing so, members in the Game Lobby voice channel will not be able to use the `MapDatabase` commands.
(Note that the other command groups will still be available.)
[**VoiceChannelControl** Cog Command Guide](https://github.com/JLpython-py/Among-Us-Bot/wiki/VoiceChannelControl).

***

## Command Guide

A command guide for each of the cogs of the bot can be found in the repository's [Wiki](https://github.com/JLpython-py/AmongUs-MapBot/wiki).

***

## Installation

The bot requires the following permissions turned on to function properly, but they can be turned off in channels where the bot is not needed:

| General Permissions | Text Permissions | Voice Permissions |
| :--- | :--- | :--- |
| View Channels | Send Messages | Mute Members |
| | Manage Message | Deafen Members|
| | Embed Links | Move Members |
| | Attach Files | |
| | Read Message History | |
| | Add Reactions | |

**Permission Integer**: 9486144

Invite the [Among Us Bot](https://discord.com/api/oauth2/authorize?client_id=793568531757137970&permissions=29486144&scope=bot) to guild.

***

## Contributing

This repository is actively maintained and I am open to suggestions for more features.
If you have a feature to suggest or a bug to report, create a new issue under this repository's [Issues](https://github.com/JLpython-py/Among-Us-Bot/issues) tab.
Individual templates have been created for both reporting bugs and suggesting new features.
