from aiohttp import web

import asyncio
import os
import random
import string
import time
from typing import TYPE_CHECKING, Union

from src.util import *


class Server:
    SHUTDOWN_TIMEOUT = 5
    # Flood chunk size (in kB)
    FLOOD_CHUNK_SIZE = 1024
    MODES = ["mist", "drip", "flood", "trickle"]
    RANDOM_OPTIONS = [str(x) for x in string.ascii_uppercase + string.digits]

    def __init__(self, address: str = "0.0.0.0", port: int = 8080, mode: str = "flood", loop = None):
        """
        :param address: Address to bind the server to.
        :param port: Port to bind the server to.
        :param mode: Mode of the tarpit.
        """
        # Do a sanity check of the mode
        assert mode in self.MODES or mode == "random", \
            f"Tarpit mode must be either {''.join(m + ', ' for m in self.MODES)} or \"random\". Instead got {mode}"
        # Binding variables
        self.__address = address
        self.__port = port

        # Tarpit mode to use
        self.__mode = mode

        # Async setup
        if loop is None:
            self.__loop = asyncio.get_event_loop()
        else:
            self.__loop = loop
        self.__int_fut = self.__loop.create_future()
        self.__shutdown = asyncio.ensure_future(self.__int_fut, loop=self.__loop)
        self.__flood_size = self.FLOOD_CHUNK_SIZE * 1024

        if TYPE_CHECKING:
            self.__server: Union[web.Server, None] = None
            self.__runner: Union[web.ServerRunner, None] = None
            self.__site: Union[web.TCPSite, None] = None

        """ 
        Some consistent data to make the tarpit look like an enormous HTML page with obfuscated code.
        Based on https://www.akamai.com/blog/security/catch-me-if-you-can-javascript-obfuscation
        """
        html_start = ("<!DOCTYPE html><html lang=\"en\"><head><script "
                      "type=\"text/javascript\">window.location=\"data:text/html;base64,")
        self.__html_start = html_start.encode("utf-8")

    async def handler(self, request) -> web.StreamResponse:
        start = time.time()
        peer_addr = request.transport.get_extra_info('peername')
        if not peer_addr:
            peer_addr = "invalid client"
        log(f"Connected to {peer_addr}")
        if self.__mode == "random":
            mode = random.choice(self.MODES)
        else:
            mode = self.__mode
        try:
            if mode == "mist":
                return await self.__do_handle_mist(request)
            elif mode == "drip":
                return await self.__do_handle_drip(request)
            elif mode == "flood":
                return await self.__do_handle_flood(request)
            elif mode == "trickle":
                return await self.__do_handle_trickle(request)
        except ConnectionError or ConnectionAbortedError:
            ...
        except Exception as e:
            log(f"Encountered exception {e}")
        finally:
            end = time.time()
            log(f"Kept client {peer_addr} busy with {mode} for {time_format(start, end)}")

    async def __do_handle_mist(self, request) -> web.StreamResponse:
        response = web.StreamResponse(
            headers={'Content-Type': 'text/html', 'Server': self.get_server()})
        response.enable_chunked_encoding()
        await response.prepare(request)
        await response.write(self.__html_start)
        while not self.__shutdown.done():
            # Send a drip chunk
            data = random.choice(
                    string.ascii_uppercase + string.digits
            )
            data = data.encode("utf-8")
            await response.write(data)
            await asyncio.sleep(5 + random.random() * 5)
        return response

    async def __do_handle_drip(self, request) -> web.StreamResponse:
        response = web.StreamResponse(
            headers={'Content-Type': 'text/html', 'Server': self.get_server()})
        response.enable_chunked_encoding()
        await response.prepare(request)
        await response.write(self.__html_start)
        while not self.__shutdown.done():
            # Send a drip chunk
            data = ''.join(
                random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(128)
            )
            data = data.encode("utf-8")
            await response.write(data)
            await asyncio.sleep(1)
        return response

    async def __do_handle_flood(self, request) -> web.StreamResponse:
        response = web.StreamResponse(
            headers={'Content-Type': 'text/html', 'Server': self.get_server()})
        response.enable_chunked_encoding()
        await response.prepare(request)
        await response.write(self.__html_start)
        while not self.__shutdown.done():
            # Send a flood chunk
            data = os.urandom(self.__flood_size)
            await response.write(data)
            """
            Add a small sleep to allow event loop to handle other connections in Docker. This is likely not needed if 
            the code is just running on a host. 
            """
            await asyncio.sleep(0.0001)
        return response

    async def __do_handle_trickle(self, request) -> web.StreamResponse:
        response = web.StreamResponse(
            headers={'Content-Type': 'text/html', 'Server': self.get_server()})
        response.enable_chunked_encoding()
        await response.prepare(request)
        await response.write(self.__html_start)
        while not self.__shutdown.done():
            # Send a trickle chunk
            data = ''.join(
                random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(1024)
            )
            data = data.encode("utf-8")
            await response.write(data)
            await asyncio.sleep(0.5)
        return response

    async def run(self):
        await self.__shutdown

    async def stop(self):
        try:
            self.__int_fut.set_result(None)
        except asyncio.InvalidStateError:
            pass
        else:
            await self.__server.shutdown()
            await self.__site.stop()
            await self.__runner.cleanup()

    @staticmethod
    def get_server() -> str:
        """
        Make up some random server to send to the bot.
        :return: Server header string
        """
        return random.choice(SERVER_OPTIONS)

    async def setup(self):
        # Server setup
        self.__server = web.Server(self.handler)
        self.__runner = web.ServerRunner(self.__server)
        await self.__runner.setup()
        self.__site = web.TCPSite(self.__runner, self.__address, self.__port,
                                  ssl_context=None,
                                  shutdown_timeout=self.SHUTDOWN_TIMEOUT)
        await self.__site.start()
        log(f"Server listening at http://{self.__address}:{self.__port}")
