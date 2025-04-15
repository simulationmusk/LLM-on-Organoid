import requests

from ..utils.constants import (
    INTAN_SERVICE_IP,
    PRIZMATIX_PORT,
)


class PrizmatixController:
    """Control the Prizmatix UV led"""

    @classmethod
    async def start(cls) -> bool:
        """Start the device"""
        r = requests.get(f"http://{INTAN_SERVICE_IP}:{PRIZMATIX_PORT}/start")
        if r.status_code == 200:
            return True
        else:
            return False

    @classmethod
    async def stop(cls) -> bool:
        """Stop the device"""
        r = requests.get(f"http://{INTAN_SERVICE_IP}:{PRIZMATIX_PORT}/stop")
        if r.status_code == 200:
            return True
        else:
            return False


async def start_prizmatix() -> bool:
    return await PrizmatixController.start()


async def stop_prizmatix() -> bool:
    return await PrizmatixController.stop()
