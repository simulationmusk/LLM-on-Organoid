import socket
import psycopg2
import pandas as pd
from datetime import datetime, timezone

import numpy as np

from ..utils.constants import TRIGGER_IP, TRIGGER_IP_PORT
from ..utils.exceptions import (
    TriggerConnectionError,
)
from ..utils.schemas import TriggerPattern


class TriggerController:
    def __init__(self, email: str, timeout=5):
        try:
            self.sock = socket.socket()
            self.sock.settimeout(timeout)  # Set timeout for the socket
            self.sock.connect((TRIGGER_IP, TRIGGER_IP_PORT))

            if email == "admin":
                self.start_time = datetime.min.replace(tzinfo=timezone.utc)
                self.end_time = datetime.max.replace(tzinfo=timezone.utc)
            else:
                bookings = self.__get_booking__()
                emails = bookings["email"].unique()
                # Check if the email id is register in the booking.
                if email in emails:
                    last_row = bookings.loc[bookings["email"] == email].iloc[-1]
                    self.start_time = last_row["startTime"]
                    self.end_time = last_row["endTime"]
                    if not self.__check_time__():
                        raise TriggerConnectionError(
                            f"Booking time: ({self.start_time}-{self.end_time})"
                        )
                else:
                    raise TriggerConnectionError("Email not found in the booking")

        except socket.timeout as e:
            raise TriggerConnectionError(f"Connection attempt timed out: {str(e)}")
        except socket.error as e:
            raise TriggerConnectionError(
                f"Failed to connect to trigger device: {str(e)}"
            )

    def __check_time__(self) -> bool:
        """Check if you are still in booking period"""
        now = datetime.now(timezone.utc)
        return now <= self.end_time and now >= self.start_time

    def __get_booking__(self) -> pd.DataFrame:
        """Get the booking for the database"""
        conn = psycopg2.connect(
            database="calendso",
            host="172.30.1.43",
            user="readonly_user",
            password="73d7aZ2PtJodadB",
            port="5432",
        )
        cursor = conn.cursor()

        # Get the current time in UTC
        now = datetime.now(timezone.utc)

        # Modify the SQL query to filter bookings based on the current time
        cursor.execute(
            """
            SELECT "startTime", "endTime", "responses"
            FROM "Booking"
            WHERE %s >= "startTime" AND %s <= "endTime";
            """,
            (now, now),
        )
        list_booking = cursor.fetchall()

        if not list_booking:
            raise TriggerConnectionError(
                "No bookings found for the current time period"
            )

        # Extract the required data
        data = []
        for booking in list_booking:
            start_time, end_time, responses = booking
            name = responses.get("name")
            email = responses.get("email")
            # Convert start_time and end_time to UTC
            start_time = start_time.replace(tzinfo=timezone.utc)
            end_time = end_time.replace(tzinfo=timezone.utc)
            data.append([start_time, end_time, name, email])

        # Create DataFrame
        df = pd.DataFrame(data, columns=["startTime", "endTime", "name", "email"])

        return df

    def __del__(self):
        self.close()

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    async def send(self, pattern: np.ndarray):
        try:
            if self.__check_time__():
                self.sock.send(pattern.tobytes())
            else:
                raise TriggerConnectionError(
                    f"Booking time: ({self.start_time}-{self.end_time})"
                )
        except socket.timeout as e:
            raise TriggerConnectionError(f"Sending pattern timed out: {str(e)}")
        except socket.error as e:
            raise TriggerConnectionError(
                f"Failed to send pattern to trigger device: {str(e)}"
            )

    @classmethod
    async def trigger_sender(cls, pattern: TriggerPattern) -> str:
        controller = cls()
        try:
            validator = pattern
            np_pattern = np.array(validator.pattern, dtype=np.uint8)
            await controller.send(np_pattern)
            return "Trigger pattern sent successfully"
        finally:
            controller.close()


# Wrapper function at the module level
async def trigger_sender(pattern: TriggerPattern) -> str:
    validated_pattern = TriggerPattern(pattern=pattern)
    return await TriggerController.trigger_sender(validated_pattern)
