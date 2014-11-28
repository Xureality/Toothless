from toothless.bot import ToothlessBot


if __name__ == '__main__':
    bot = ToothlessBot('Toothless')
    bot.user = 'Toothless'
    bot.real_name = 'ToothlessBot, by Tomako, with help from Xureality'
    bot.connect('irc.editingarchive.com', port=6697, use_ssl=True)
    bot.start()
