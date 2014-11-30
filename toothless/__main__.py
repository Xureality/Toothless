import argparse
import logging

from os.path import expanduser

from toothless.bot import Bot


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default=expanduser('~/.toothless/config.json'))
    parser.add_argument('--state',
                        default=expanduser('~/.toothless/state.json'))
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    config_file = open(args.config, 'r')
    state_file = open(args.state, 'a+')
    bot = Bot(config_file, state_file)
    bot.start()
