<h1>Among-Us-Bot</h1>

![GitHub last commit](https://img.shields.io/github/last-commit/JLpython-py/Among-Us-Bot)
![GitHub repo size](https://img.shields.io/github/repo-size/JLpython-py/Among-Us-Bot)
![GitHub issues](https://img.shields.io/github/issues/JLpython-py/Among-Us-Bot)
![GitHub issues by-label](https://img.shields.io/github/issues/JLpython-py/Among-Us-Bot/enhancement)
![GitHub pull requests](https://img.shields.io/github/issues-pr/JLpython-py/Among-Us-Bot)
![GitHub deployments](https://img.shields.io/github/deployments/JLpython-py/Among-Us-Bot/GitHub-pages)
![GitHub](https://img.shields.io/github/license/JLpython-py/Among-Us-Bot)

![Among Us](https://user-images.githubusercontent.com/72679601/105618817-8441fe00-5da0-11eb-97ee-4756d629d01a.png)

Among Us Bot is a Discord bot with various features concerining the game of Among Us.
These features are intended to be supplemental to the game itself, in order to enhance the experience of the game.

<h2>Features</h2>

<h3>Map Database</h2>

![TheSkeld retrieve tasks "Divert Power"](https://user-images.githubusercontent.com/72679601/108528698-8bb5d380-7288-11eb-88c1-7518629a5a25.png)

This repository has data about nearly all aspect of the Among Us maps. 
Member of guilds can use a sent of comprehensive commands to reference the available data. 
[See more details](https://github.com/JLpython-py/Among-Us-Bot/wiki/MapDatabase).

<h3>Random Among Us</h2>

![randmap](https://user-images.githubusercontent.com/72679601/107803852-070f0680-6d18-11eb-957f-a308cdda62e6.png)
![randsettings](https://user-images.githubusercontent.com/72679601/107803865-0d04e780-6d18-11eb-9446-0497fd222cd9.png)
Just like its name implies, this feature allows members to generate random apsects of Among Us.
Currently supported is generation of a random map, a random number of impostors, and a random option for a specific setting or for all the in-game settings.
[See more details](https://github.com/JLpython-py/Among-Us-Bot/wiki/RandomAmongUs).

<h3>Voice Channel Control</h3>

![claim](https://user-images.githubusercontent.com/72679601/107803946-2b6ae300-6d18-11eb-9da6-e59318d692f6.png)
![Voice Channel Claim Control](https://user-images.githubusercontent.com/72679601/108528722-91abb480-7288-11eb-9b35-3a262af7b8b4.png)
Members can claim control of a voice channel and designate it as a Game Lobby.
Optionally, they can also claim control of a second voice channel and designate it as a Ghost Lobby.
With control, members with claims can control the properties of other members in the Game Lobby.
Members with claims are able to mute/un-mute members, deafen/un-deafen members, and move members to and from the Ghost Lobby, if applicable.
Lastly, members with claims will be able to lock the `MapDatabase` commands.
In doing so, members in the Game Lobby voice channel will not be able to use the `MapDatabase` commands.
(Note that the other commands will still be available.)
[See more details](https://github.com/JLpython-py/Among-Us-Bot/wiki/VoiceChannelControl).

<h2>Command Guide</h2>

A command guide for each of the cogs of the bot can be found in the repository's [Wiki](https://github.com/JLpython-py/AmongUs-MapBot/wiki).

<h2>Installation</h2>

The bot requires the following permissions turned on to function properly, but they can be turned off in channels where the bot is not needed:

| General Permissions | Text Permissions | Voice Permissions |
| :--- | :--- | :--- |
| View Channels | Send Messages | Mute Members |
| | Manage Message | Deafen Members|
| | Embed Links | Move Members |
| | Attach Files | |
| | Read Message History | |
| | Add Reactoins | |

Add the [Among Us Bot](https://discord.com/api/oauth2/authorize?client_id=793568531757137970&permissions=29486144&scope=bot) to your guild.

<h2>Contributing</h2>

This repository is constantly maintained and the developers are open to suggestions for more features.
If you have a feature to suggest or a bug to report, create a new issue under this repository's [Issues](https://github.com/JLpython-py/Among-Us-Bot/issues) tab.
