from datetime import datetime
from typing import Optional

import pandas as pd
from influxdb_client import InfluxDBClient

from ..utils.constants import DB_IP, DB_PORT, DB_TIMEOUT, DB_TOKEN
from ..utils.exceptions import DatabaseConnectionError, DatabaseQueryError
from ..utils.schemas import (
    RawSpikeQuery,
    SpikeCountQuery,
    SpikeEventQuery,
    TriggersQuery,
)


class DatabaseController:
    """Database class to access recorded data"""

    def __init__(self):
        self._token = DB_TOKEN
        self._url = f"http://{DB_IP}:{DB_PORT}"

    def _connect_to_db(self):
        try:
            client_read = InfluxDBClient(
                url=self._url, token=self._token, timeout=DB_TIMEOUT
            )
            return client_read.query_api()
        except DatabaseConnectionError as e:
            raise DatabaseConnectionError(f"Failed to connecting to db: {str(e)}")

    async def _get_spike_event(
        self, start: datetime, stop: datetime, fsname: str
    ) -> pd.DataFrame:
        query_api = self._connect_to_db()
        query = f'from(bucket:"spikeevent")\
            |> range(start: {start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}, stop: {stop.strftime("%Y-%m-%dT%H:%M:%S.%fZ")})\
            |> filter(fn:(r) => r["_measurement"] == "{fsname}")\
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")\
            |> drop(columns: ["_start", "_stop", "_field", "_measurement"])\
            |> rename(columns: {{index: "channel", _time: "Time", voltage:"Max Amplitude"}})'
        df = query_api.query_data_frame(query=query, org="FinalSpark")
        if len(df.index) > 0:
            df = df.drop(columns=["result", "table"]).astype({"channel": int})
        return df

    @classmethod
    async def get_spike_event(cls, query: SpikeEventQuery) -> Optional[pd.DataFrame]:
        controller = cls()
        try:
            return await controller._get_spike_event(
                query.start, query.stop, query.fsname
            )
        except DatabaseQueryError as e:
            raise DatabaseQueryError(f"Failed to get spike event from db: {str(e)}")

    async def _get_raw_spike(
        self, start: datetime, stop: datetime, index: int
    ) -> pd.DataFrame:
        query_api = self._connect_to_db()
        query = f'from(bucket:"rawspike")\
            |> range(start: {start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}, stop: {stop.strftime("%Y-%m-%dT%H:%M:%S.%fZ")})\
            |> filter(fn:(r) => r["index"] == "{index}")\
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")\
            |> drop(columns: ["_start", "_stop", "_field", "_measurement"])\
            |> rename(columns: {{index: "channel", _time: "Time", voltage:"Amplitude"}})'
        df = query_api.query_data_frame(query=query, org="FinalSpark")
        if len(df.index) > 0:
            df = df.drop(columns=["result", "table"]).astype({"channel": int})
        return df

    @classmethod
    async def get_raw_spike(cls, query: RawSpikeQuery) -> pd.DataFrame:
        controller = cls()
        try:
            return await controller._get_raw_spike(query.start, query.stop, query.index)
        except DatabaseQueryError as e:
            raise DatabaseQueryError(f"Failed to get raw spike from db: {str(e)}")

    async def _get_spike_count(
        self, start: datetime, stop: datetime, fsname: str
    ) -> pd.DataFrame:
        query_api = self._connect_to_db()
        query = f'from(bucket:"spikecount")\
            |> range(start: {start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}, stop: {stop.strftime("%Y-%m-%dT%H:%M:%S.%fZ")})\
            |> filter(fn:(r) => r["_measurement"] == "{fsname}")\
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")\
            |> drop(columns: ["_start", "_stop", "_field", "_measurement"])\
            |> rename(columns: {{index: "channel", _time: "Time", voltage:"Spike per minutes"}})'
        df = query_api.query_data_frame(query=query, org="FinalSpark")
        if len(df.index) > 0:
            df = df.drop(columns=["result", "table"]).astype({"channel": int})
        return df

    @classmethod
    async def get_spike_count(cls, query: SpikeCountQuery) -> pd.DataFrame:
        controller = cls()
        try:
            return await controller._get_spike_count(
                query.start, query.stop, query.fsname
            )
        except DatabaseQueryError as e:
            raise DatabaseQueryError(f"Failed to get spike count from db: {str(e)}")

    async def _get_all_triggers(self, start: datetime, stop: datetime) -> pd.DataFrame:
        query_api = self._connect_to_db()
        query = f'from(bucket:"stimevent")\
            |> range(start: {start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}, stop: {stop.strftime("%Y-%m-%dT%H:%M:%S.%fZ")})\
            |> filter(fn:(r) => r["_measurement"] == "trigger")\
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")\
            |> drop(columns: ["_start", "_stop", "_field", "_measurement"])\
            |> rename(columns: {{index: "trigger"}})'
        df = query_api.query_data_frame(query=query, org="FinalSpark")
        if len(df.index) > 0:
            df = (
                df.drop(columns=["result", "table"])
                .sort_values(by=["_time", "trigger"], ignore_index=True)
                .astype({"trigger": int})
                .astype({"up": int})
            )
        return df

    @classmethod
    async def get_all_triggers(cls, query: TriggersQuery) -> pd.DataFrame:
        controller = cls()
        try:
            return await controller._get_all_triggers(query.start, query.stop)
        except DatabaseQueryError as e:
            raise DatabaseQueryError(f"Failed to get all triggers from db: {str(e)}")


async def get_spike_event(query: SpikeEventQuery) -> Optional[pd.DataFrame]:
    validator = SpikeEventQuery(start=query.start, stop=query.stop, fsname=query.fsname)
    return await DatabaseController.get_spike_event(validator)


async def get_raw_spike(query: RawSpikeQuery) -> pd.DataFrame:
    validator = RawSpikeQuery(start=query.start, stop=query.stop, index=query.index)
    return await DatabaseController.get_raw_spike(validator)


async def get_spike_count(cls, query: SpikeCountQuery) -> pd.DataFrame:
    validator = SpikeCountQuery(start=query.start, stop=query.stop, fsname=query.fsname)
    return await DatabaseController.get_spike_count(validator)


async def get_all_triggers(query: TriggersQuery) -> pd.DataFrame:
    validator = TriggersQuery(start=query.start, stop=query.stop)
    return await DatabaseController.get_all_triggers(validator)
