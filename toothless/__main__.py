import argparse
from os.path import expanduser
from toothless.bot import Bot


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default=expanduser('~/.toothless/config.json'))
    parser.add_argument('--state',
                        default=expanduser('~/.toothless/state.json'))
    args = parser.parse_args()
    config_file = open(args.config, 'r')
    state_file = open(args.state, 'a+')
    bot = Bot(config_file, state_file)
    bot.start()
