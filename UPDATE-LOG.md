gBot's Update Log and Planned Features
--------------------------------------
This markdown file includes different information about the updates of gBot.
This markdown file will also include planned features in the future.
If anyone want certain features to be added, please create a new issue.
Or if you have fixes or updates, create a pull request.
   
**Contents**
- [Update Logs](#update-logs)
- [Planned Features](#planned-features)

---

# Update Logs
-------------

## Version 1.4.0
----------------

> ### Version 1.4.1 [Version Rework]
> --------------------------------
> This update has changed how versions function. The first number indicates an enormous update, for example a whole new system. The second number indicates normal updates, bug fixes, etc,. Finally, the last number indicates miscellaneous fixes and updates.
>
> This version also has a couple bug fixes. Removed some hard coding, and refactoring some code.

> ### Version 1.4.2
> ----------------
> gBot's pagination system is now fixed. From now on, if a user changes a page, other users' page will not be changed.This fix is implemented by using dictionaries on different variables of the paginator class.
>
> This version also fixed a couple of grammar and spelling mistakes.

## Version 1.5.0 [Custom Server Prefix]
---------------------------------------
This update introduces custom server prefix by using a sqlite database. 2 new commands are added. They are, `setprefix` and `prefix`. `setprefix` will change the server's prefix. Only server administrators can use this command. `prefix` sends the current prefix of gBot. A new cog is also added to organize these commands, it is called `ConfigCog` and is also added to the help command.

This version also has more spelling fixes.

## Version 1.6.0 [Pagination Configuration]
-------------------------------------------
This version fixes more pagination problems. If the bot didn't had the manage messages permission, commands that use pagination will break. Now it works fine. 3 new commands are also added in this version. `setpaginationmode`, `paginationmode`, and `httpcode`. `httpcode` is a new fun command that sends http response cats! `setpaginationmode` will change the server's pagination mode. Only server administrators can use this command. There are only 2 modes, which are `auto` and `manual`. `auto` mode will automatically remove pagination reactions and delete the message after inactivity, but this mode requires the bot to have the manage messages permission. `manual` mode does the opposite to `auto` mode and does not require special permissions.

Side note: We might have a new developer to work on gBot pretty soon. He is currently trying to purpose an economy system design.

## Version 1.7.0 [I'm not a robot]
----------------------------------
This version introduces the new captcha system! New commands are `setverificationchannel`, `verificationchannel`, and verify. `setverificationchannel` will setup the captcha system for the server. It will restrict the @everyone role so that unverified people cant access other channels other than the verification channel. The bot will also create a role called "Verified" for verified people. *Do not change the name of the verified role, if you change it the captcha system will create another "Verified" role.* `verificationchannel` will tell the user which channel is used for verification. `verify` can only be used in a verification channel. The bot will send a captcha with random uppercase characters and numbers. If you succeed, you will get the "Verified" role.

Bugs not fixed: `panel updater` doesn't really execute the update_wait.py script in linux. I'm having problems with bash.

> ### Version 1.7.1
> -----------------
> This version just bring small bug fixes to the verification system. You cannot use other commands in a verification channel.

> ### Version 1.7.2
> -----------------
> I just cleaned up the `clear` command and made it better.

> ### Version 1.7.3
> -----------------
> Remade the `ping` command. It now shows the websocket, typing, and database latency.

## Version 1.8.0 [Anime]
------------------------
New cog this update, `AnimeCog`. It brings 4 commands in total. They are `waifu`, `waifu categories`, `waifu sfw`, and `waifu nsfw`. Thanks to [waifu.pics](https://waifu.pics), fetching anime pictures are made very easy using it's API and `aiohttp`. I recommend finding out about these commands by yourself ( ͡° ͜ʖ ͡°). 

---

# Planned Features
------------------

## Plans for Version 2.0.0 [Economy Update]
-------------------------------------------
The update for version 2.0.0 will be a very big update. This includes a very big economy system.
List of features for the economy system are down below. They are subject to change at any time.

List of features:
  - Economy system
    - Bank were users can deposit their money for safe keeping
    - Jobs for users to choose from
    - Minigames will appear when you users execute a command that makes money for them
    - Robbing other users' wallets
    - Item and power-up shop
    - Stocks or cryptocurrency market
    - Bankruptcy, loans and interests
