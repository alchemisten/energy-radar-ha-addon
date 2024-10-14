"""Support for EnergyRadar sensors."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

from .const import ER_LOGIN, ER_METERS, SCAN_INTERVAL_MINUTES
from .entity import EnergyRadarSensorEntity
from .erapi import EnergyRadarException, Meter, Sensor
from .hub import EnergyRadarHub

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=SCAN_INTERVAL_MINUTES)


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the EnergyRadar sensors using config entry."""
    energy_radar: EnergyRadarHub = hass.data[ER_LOGIN]

    dev = [
        EnergyRadarSensor(energy_radar, meter, sensor)
        for meter in hass.data[ER_METERS]
        for sensor in meter.get_sensors()
    ]

    if not dev:
        return

    _LOGGER.debug("Adding meters for sensors %s", dev)
    async_add_entities(dev, True)


class EnergyRadarSensor(EnergyRadarSensorEntity, SensorEntity):
    """EnergyRadar sensor."""

    def __init__(
        self, energy_radar: EnergyRadarHub, meter: Meter, sensor: Sensor
    ) -> None:
        """Initialize EnergyRadar sensor entity."""
        super().__init__(sensor)
        self.sensor = sensor
        identifier = (
            self.sensor.meter_id + "_" + self.sensor.name.lower().replace(" ", "_")
        )

        self._meter_id: str = self.sensor.meter_id
        self._attr_unique_id = identifier
        self._state: float | int | None = None
        self.name = self.sensor.name
        self._attr_device_class = self.sensor.device_class
        self._attr_native_unit_of_measurement = self.sensor.unit
        self._attr_state_class = self.sensor.state_class

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            self._state = self.sensor.get_value
        except EnergyRadarException as ex:
            if self._attr_available:
                _LOGGER.error(
                    "EnergyRadar sensor connection error for '%s': '%s",
                    self.entity_id,
                    ex,
                )
            self._state = None
            self._attr_available = False
            return

        self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return the state."""
        if self._state is not None:
            return str(self._state)
        return None
