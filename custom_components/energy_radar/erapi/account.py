"""Account class."""

import logging

from .meter import EnergyMeter, GasMeter, Meter, WaterMeter
from .schemas import METERS_SCHEMA
from .session import Session

_LOGGER = logging.getLogger(__name__)


class Account:
    """Class with data and methods for interacting with an EnergyRadar cloud session."""

    def __init__(self, session: Session) -> None:
        """Initialize the account data."""
        self._meters: set[Meter] = set()
        self._session = session

    @property
    def meters(self):
        """Return set of meters for logged in account.

        :return:
        """
        if not self._meters:
            self.refresh_meters()

        return self._meters

    def refresh_meters(self):
        """Get information about meters connected to account.

        :return:
        """

        resp = self._session.get("/v1/meters")

        meters = METERS_SCHEMA(resp.json())

        data = meters["data"]

        for meter in data:
            if meter["obisMedium"] == "1":
                meter_obj = EnergyMeter(meter["meterId"], self._session)
                self._meters.add(meter_obj)
                _LOGGER.info("Added power meter %s", meter["meterId"])
            if meter["obisMedium"] == "8":
                meter_obj = WaterMeter(meter["meterId"], self._session)
                self._meters.add(meter_obj)
                _LOGGER.info("Added water meter %s", meter["meterId"])
            if meter["obisMedium"] == "7":
                meter_obj = GasMeter(meter["meterId"], self._session)
                self._meters.add(meter_obj)
                _LOGGER.info("Added gas meter %s", meter["meterId"])
