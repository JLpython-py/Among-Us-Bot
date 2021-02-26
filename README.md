<h1>AmongUs-MapBot</h1>

This Discord Bot, called the AmongUs MapBot, acts as an easily accessbile database for information regarding each of the Among Us maps. The information in this repository is free for anyone to use, even if it is not used in the Discord Bot.

<h2>Installation</h2>

The bot requires the following permissions turned on to function properly, but they can be turned off in channels where the bot is not needed:

<h3>General Permissions</h3>

 - View Channels

<h3>Text Permissions</h3>

 - Send Messages
 - Manage Messages
 - Embed Links
 - Attach Files
 - Read Message History
 - Add Reactions
 
<h3>Voice Permissions</h3>

 - N/A

The following link can be used to add this bot to a server with all the necessary permissions:
- [Add AmongUs MapBot](https://discord.com/api/oauth2/authorize?client_id=793568531757137970&permissions=126016&scope=bot)

<h2>Commands</h2>

<h3>Command Prefix</h3>
The command prefix for this bot is the '+' character. Currently, there is no customization for the command prefix.

<h3>Command List</h3>

All the commands are case-insensitive. Currently there are two commands available for the bot, `retrieve` and `search`. Each command returns an embed with features unique to the command.

![help command](https://user-images.githubusercontent.com/72679601/103316442-74234280-49dd-11eb-85a8-d5ca5308e707.png)
![help command response](https://user-images.githubusercontent.com/72679601/103316443-75546f80-49dd-11eb-9c42-9ee993f60a73.png)

<h4>Command: retrieve</h4>

*Note: This command can be aliased to `r`*

![help retrieve command](https://user-images.githubusercontent.com/72679601/103316567-c5cbcd00-49dd-11eb-98ca-22c88c10fc28.png)
![help retrieve command reponse](https://user-images.githubusercontent.com/72679601/103316571-c7959080-49dd-11eb-9b71-428c724becf6.png)

<h5>Arguments</h5>

 - `<mapname>`: The name of the map, condensed into one word, case-insensitive. Since there are only three maps, the possible values for this parameter are `MiraHQ`, `Polus`, or `TheSkeld`.
 - `<category>`: The category which the argument `<option>` belongs to, case-insensitive. Currently, the available values for this parameter are `actions`, `locations`, `maps`, `tasks`, or `vents`.
 - `<option>`: The name of the item which is being retrieved, case-insensitive. The available values for this parameter varies based on the `<category>` argument. Since many of the possible values for this argument contain multiple words, it is recommended that the option is surrounded by double quotes ("), for example `"Option Parameter"` as opposed to `Option Parameters`.
 
<h5>Return Values</h5> 

![retrieve command w/ mapname=Polus category=locations option="Admin"](https://user-images.githubusercontent.com/72679601/103320919-19ddae00-49ec-11eb-9920-095b7da9526f.png)
![retrieve command response w/ mapname=Polus category=locations option="Admin"](https://user-images.githubusercontent.com/72679601/103320920-1a764480-49ec-11eb-9142-c40bbcdeced6.png)

This command returns an embed with an image and information which correspond to the `<option>` argument. Once this command is called, the message the member sent which called the command is deleted, in order to limit the number of message sent in a channel.

<h4>Command: `search`</h4>

*Note: This command can be aliased to `s`*

![help search command](https://user-images.githubusercontent.com/72679601/103316568-c6646380-49dd-11eb-860a-6af0c18ed45f.png)
![help search command response](https://user-images.githubusercontent.com/72679601/103316570-c6fcfa00-49dd-11eb-85ff-e7ea660103c0.png)

<h5>Arguments</h5>

 - `<mapname>`: The name of the map, condensed into one word, case-insensitive. Since there are only three maps, the possible values for this parameter are `MiraHQ`, `Polus`, or `TheSkeld`.
 - `<category>`: The category which the argument `<option>` belongs to, case-insensitive. Currently, the available values for this parameter are `actions`, `locations`, `maps`, `tasks`, or `vents`.
 
<h5>Return Values</h5>

![search command w/ mapname=TheSkeld category=actions](https://user-images.githubusercontent.com/72679601/103317104-5e168180-49df-11eb-8899-7a4cafb9698c.png)
![search command response w/ mapname=TheSkeld category=actions](https://user-images.githubusercontent.com/72679601/103317103-5e168180-49df-11eb-8951-80d784aae0c5.png)

This command returns an embed with an image of the logo of the map and the basic description items of the option. The message is also reacted with eight emojis which the member can use to scroll along the list. Note that the scrolling wraps, i.e. scrolling backwards from the first page will scroll to the last page and scrolling forwards from the last page will scroll to the first page. Once this command is called, the message the member sent which called the command is deleted, in order to limit the number of messages in a channel. This command only allows the member who originally send the `search` command to scroll with the emojis. Other members who attempt to scroll with the emojis will be ignored, and their reaction removed. A member can only have one of these embeds open at a time, i.e. calling this command, then calling it again will delete the first message. The only exception to this is if the member reacts with the ✔ emoji.

<h6>Emoji Usage</h6>

 - ⏮ Jumps to the first page
 - ⏪ Scrolls five pages preceding the current page.
 - ◀ Scrolls to the preceding page.
 - ▶ Scrolls to the succeeding page.
 - ⏩ Scrolls five pages succeeding the current page.
 - ⏭ Jumps to the last page
 - ✔ Imitates the `retrieve` command with the `<option>` parameter set to the current page.
 - ❌ Closes the embed and deletes the message
