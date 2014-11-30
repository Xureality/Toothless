# Toothless

Toothless is an IRC bot. Toothless welcomes users, responds to trigger phrases, and eats stuff.

Toothless requires **Python 2.7** and uses **[ircutils](https://github.com/kracekumar/ircutils)**.

## Commands

### Private

`/msg Toothless list_commands` lists all trigger&ndash;response pairs.

`/msg Toothless ignore_me` prevents Toothless from greeting your future channel joins.

`/msg Toothless append_whitelist nick1 nick2 nick3` adds one or more nicks to the whitelist. Only admins can use this command.

`/msg Toothless purge_commands` removes all trigger&ndash;response pairs. Only admins can use this command.

`/msg Toothless terminate` shuts down the bot. Only admins can use this command.

### Channel

`Toothless! attack target` makes Toothless attack "target".

`Toothless! eat victim` makes Toothless eat "victim".

`Toothless! stomach` lists what Toothless has eaten.

`Toothless! spit victim` makes Toothless regurgitate "victim".

`Toothless! vomit` makes Toothless regurgitate everything.

`Toothless! learn trigger -> response` adds a trigger&ndash;response pair. Triggers are parsed as regular expressions. Responses are parsed as Python template strings; supplied substitution placeholders include the triggerer's nick (as `${nick}`) and any of the trigger's named groups. Only admins and whitelisted nicks can use this command.

`Toothless! forget trigger` removes the corresponding trigger&ndash;response pair. Only admins and whitelisted nicks can use this command.
