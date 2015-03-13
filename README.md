# Toothless

Toothless is an IRC bot. Toothless welcomes users, responds to trigger phrases, and eats stuff.

Toothless is written in **Python 2.7** and requires:

**[ircutils](https://github.com/kracekumar/ircutils)**

**[mechanize](http://wwwsearch.sourceforge.net/mechanize/download.html)**

**[dice](https://pypi.python.org/pypi/dice)**

## Commands

### Private

`/msg Toothless list_commands` lists all trigger&ndash;response pairs.

`/msg Toothless ignore_me` prevents Toothless from greeting your future channel joins.

`/msg Toothless append_whitelist nick1 nick2 nick3` adds one or more nicks to the whitelist. Only admins can use this command.

`/msg Toothless purge_commands` removes all trigger&ndash;response pairs. Only admins can use this command.

`/msg Toothless terminate` shuts down the bot. Only admins can use this command.

`/msg Toothless reload_config` reloads config.json and state.json while running. Note that connection configuration changes will not take effect without a restart. Only admins can use this command.

### Channel

`Toothless! attack target` makes Toothless attack "target".

`Toothless! eat victim` makes Toothless eat "victim".

`Toothless! stomach` lists what Toothless has eaten.

`Toothless! spit victim` makes Toothless regurgitate "victim".

`Toothless! vomit` makes Toothless regurgitate everything.

`Toothless! learn trigger -> response` adds a trigger&ndash;response pair. Triggers are parsed as regular expressions. Responses are parsed as Python template strings; supplied substitution placeholders include the triggerer's nick (as `${nick}`) and any of the trigger's named groups. Only admins and whitelisted nicks can use this command.

`Toothless! forget trigger` removes the corresponding trigger&ndash;response pair. Only admins and whitelisted nicks can use this command.

## Installation (assuming sudo)

### Debian
`apt-get install virtualenv python python-dev`

`virtualenv Toothless`

`git clone https://github.com/Tmplt/Toothless.git`

`cd Toothless/`

Configurate config.json and state.json

`source bin/activate`

`pip install -r requirements.txt`

`python -m --config ./config.json --state ./state.json`

### Arch Linux (assumin python and python2)

`pacman -S python2-virtualenv python2`

same as Debian
