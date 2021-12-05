"""Xiaomi temperature and humidity sensor V2 adapter for WebThings Gateway."""

from os import path
import signal
import sys
import time
import asyncio
import threading


sys.path.append(path.join(path.dirname(path.abspath(__file__)), 'lib'))

from pkg.mitemp_adapter import MiTempAdapter  # noqa
from pkg.util import print


_DEBUG = True
_ADAPTER = None


def cleanup(signum, frame):
    """Clean up any resources before exiting."""
    if _ADAPTER is not None:
        _ADAPTER.close_proxy()

    sys.exit(0)


async def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    _ADAPTER = MiTempAdapter(loop=asyncio.get_running_loop(), verbose=_DEBUG)
    # Wait until the proxy stops running, indicating that the gateway shut us
    # down.
    print('... Running forever')
    while _ADAPTER.proxy_running():
        print('running')
        await asyncio.sleep(300)
        # await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
