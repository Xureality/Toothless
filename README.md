# Toothless

Toothless is an IRC bot. Toothless welcomes users, responds to trigger phrases, rolls dices, eats stuff and much more.<br>
Toothless is written in **Python 2.7.X** and requires everything in required.txt

## Commands

### Private

Private command | what it does
---------------- | ------------
`/msg Toothless list_commands` | lists all made trigger&ndash;response pairs.
`/msg Toothless ignore_me` | prevents Toothless from greeting your future channel joins.
`/msg Toothless append_whitelist nick1 nick2 nick3` | adds one or more nicks to the whitelist. Whitelisted nicks can create new trigger phrases. Only administrators can use this command.
`/msg Toothless purge_commands` | removes **all** created trigger&ndash;response pairs. Only admins can use this command.<br>
`/msg Toothless terminate` | shuts Toothless down. Only admins can use this command.
`/msg Toothless reload_config` | reloads config.json and state.json while running. Note that connection configuration changes will not take effect without a restart. Only admins can use this command.

### Channel

Channel command | what it does
--------------- | -------------
`Toothless! attack target` | makes Toothless attack `target`.
`Toothless! eat victim` | makes Toothless eat `victom`.
`Toothless! stomach` | lists what Toothless has eaten.
`Toothless! spit victim` | makes Toothless regurgitate `victim`.
`Toothless! vomit` | makes Toothless regurgitate everything.

`Toothless! learn trigger -> response` is the main thingy.<br>
Adds a trigger&ndash;response pair. Triggers are parsed as regular expressions. Responses are parsed as Python template strings; supplied substitution placeholders include the triggerer's nick (as `${nick}`) and any of the trigger's named groups. Only admins and whitelisted nicks can use this command.

Channel command | what it does
--------------- | ------------
`Toothless! learn trigger -> response` | adds a trigger&ndash;response pair. Triggers are parsed as regular expressions. Responses are parsed as Python template strings; supplied substitution placeholders include the triggerer's nick (as `${nick}`) and any of the trigger's named groups. Only admins and whitelisted nicks can use this command.
`Toothless! forget trigger` | removes the corresponding trigger&ndash;response pair. Only admins and whitelisted nicks can use this command.

## Installation
```
$ apt-get install virtualenv python python-dev
$ virtualenv Toothless
$ git clone https://github.com/Tmplt/Toothless.git
$ cd Toothless/
```

Configure ./config.json and ./state.json to taste<br>
Remember to add an administrator nick in `config.json`<br>

```
$ source bin/activate
$ pip install -r requirements.txt
$ python -m --config ./config.json --state ./state.json 
```
