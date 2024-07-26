#!/usr/bin/env python3

import asyncio
from functools import partial
import os
import signal

from src.server import Server
from src.util import log


ALIVE_FILE = "./alive.txt"


def exit_handler(exit_event: asyncio.Event, *args):
    if exit_event.is_set():
        log("Received another stop signal. Crashing and burning...")
        exit(1)
    log("Received stop signal. Committing seppuku...")
    exit_event.set()


async def little_touch() -> None:
    while True:
        if not os.path.isfile(ALIVE_FILE):
            with open(ALIVE_FILE, "w"):
                pass
        await asyncio.sleep(1)


async def main(main_loop):
    mode = os.getenv("MODE")
    if not mode:
        mode = "random"
    log(f"Using mode {mode}")
    server = Server(address="0.0.0.0", mode=mode)
    await server.setup()
    health_check = asyncio.ensure_future(little_touch(), loop=main_loop)

    # Exit setup
    exit_event = asyncio.Event()
    signal_handler = partial(exit_handler, exit_event)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Wait to tear it all down.
    await exit_event.wait()
    health_check.cancel()
    log("Shutting down server")
    await server.stop()
    log("All stopped")


if __name__ == '__main__':
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        log("Using uvloop.")
    except ImportError:
        ...
    finally:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main(loop))
        loop.close()
