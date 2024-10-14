"""Base entity for EnergyRadar."""

from __future__ import annotations

import logging

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .erapi import Sensor

_LOGGER = logging.getLogger(__name__)


class EnergyRadarSensorEntity(Entity):
    """Base EnergyRadar entity."""

    _attr_has_entity_name = True

    def __init__(self, sensor: Sensor) -> None:
        """Initialize EnergyRadar entity."""
        self._sensor = sensor

        self._attr_name = self._sensor.name
        self._attr_device_info: DeviceInfo = DeviceInfo(
            identifiers={(DOMAIN, self._sensor.meter_id)},
            name=self._sensor.meter_id,
            manufacturer=self._sensor.manufacturer,
            serial_number=self._sensor.meter_id,
        )
