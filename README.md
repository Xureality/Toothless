# Toothless

Latest release is **v2.2a "Gronckle"**

Toothless is ~~a messy, horrendously and arse-written~~ ~~decently~~ somewhat decently written IRC-bot that can interacts with whitelisted nicks. Toothless welcomes users, responds to trigger phrases and eats stuff.

Toothless is written in **Python 2.7.X** and based upon **[ircutils](https://github.com/kracekumar/ircutils)**.

## Commands
### PRIVMSG
`/msg Toothless identify passwd`, identifies Toothless with NickServ

`/msg Toothless join #channel`, tells Toothless to join #channel

`/msg Toothless list_commands`,  lists the currently saved trigger and response phrases found in `commands.txt`

`/msg Toothless terminate`, shuts down the bot if nick is found in `admins.txt`

`/msg Toothless ignore_me`, excludes you from Toothless's welcome messages

`/msg Toothless append_whitelist nick`, appends nick to `whitelist.txt` 

### Channel
Following commands can only be used if nick is found `whitelist.txt` for anti-spam purposes

`Toothless$ foobar -> flowerpot`, saves the response "flowerpot" to be said when a message contains "foobar"

`Toothless$ bad dragon! -> tackles {0}`, tackles nick when "bad dragon!" is found in message

`Toothless# foobar`, removes the response for the trigger "foobar"

`Toothless! eat eel`, makes Toothless eat "eel"

`Toothless! spit eel`, makes Toothless spit out "eel"

`Toothless! stomach`, lists what Toothless has eaten
