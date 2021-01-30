#! python3
# launcher.py

"""
==============================================================================
MIT License

Copyright (c) 2020 Jacob Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==============================================================================
"""

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
