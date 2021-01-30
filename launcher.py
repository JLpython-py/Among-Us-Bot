#! python3
# launcher.py

import asyncio
import os

from lib.bot import BotRoot


def main():
    """ Create bot object and add to Async I/O event loop to run forever
"""
    token = os.environ.get("token", None)
    if token is None:
        with open(os.path.join("lib", "bot", "token.txt")) as file:
            token = file.read()
    assert token is not None
    loop = asyncio.get_event_loop()
    bot = BotRoot()
    loop.create_task(bot.start(token))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        bot.connection.close_connection()


if __name__ == '__main__':
    main()
