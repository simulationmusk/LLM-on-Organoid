import socket

import numpy as np

from ..utils.constants import (
    TRIGGER_IP,
    TRIGGER_UV_PORT,
    TRIGGER_UV_TIMEOUT,
)
from ..utils.exceptions import TriggerUVConnectionError, TriggerUVSendError
from ..utils.schemas import TriggerUVSendRequest


class TriggerUVController:
    """Control the trigger UV. Only 1 trigger to activate the UV. Power Control is manual (potentiometer)
    Don't forget to close the session after each use"""

    def __init__(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((TRIGGER_IP, TRIGGER_UV_PORT))
            self.sock.settimeout(TRIGGER_UV_TIMEOUT)
            self.buffer = np.zeros(1, dtype=np.int32)
        except socket.timeout as e:
            raise TriggerUVConnectionError(f"Connection attempt timed out: {str(e)}")
        except socket.error as e:
            raise TriggerUVConnectionError(f"Failed to connect to trigger UV: {str(e)}")

    def _close(self):
        """Close the connection"""
        if self.sock:
            self.sock.close()
            self.sock = None

    async def _send(self, t: int):
        """Activate the UV for a period of t
        :type t: int
        """
        if t < 1:
            raise TriggerUVSendError("Value must be bigger than 0")
        self.buffer[0] = t
        self.sock.send(self.buffer.tobytes())

    @classmethod
    async def trigger_uv_send(cls, req: TriggerUVSendRequest) -> str:
        controller = cls()
        try:
            await controller._send(req.t)
            return "Trigger UV data send successfully"
        finally:
            controller._close()


async def trigger_uv_send(req: TriggerUVSendRequest) -> str:
    validator = TriggerUVSendRequest(t=req)
    return await validator.trigger_uv_send(req)
