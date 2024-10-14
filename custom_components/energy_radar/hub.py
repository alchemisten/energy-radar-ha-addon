"""Support for EnergyRadar connected sensors."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.util import Throttle

from .const import ER_METERS
from .erapi import Account

_LOGGER = logging.getLogger(__name__)


class EnergyRadarHub:
    """An EnergyRadar hub wrapper class."""

    def __init__(self, hass: HomeAssistant, energy_radar: Account) -> None:
        """Initialize the EnergyRadar hub."""
        self._hass = hass
        self.energy_radar: Account = energy_radar

    @Throttle(timedelta(minutes=1))
    def update_meters(self) -> None:
        """Update the meter states."""
        _LOGGER.debug("Running ERHUB.update_meters %s", self._hass.data.get(ER_METERS))
        self._hass.data[ER_METERS] = self.energy_radar.meters
