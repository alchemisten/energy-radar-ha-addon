"""The EnergyRadar integration."""

from __future__ import annotations

import logging

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_TOKEN, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import config_entry_oauth2_flow

from . import api
from .const import DOMAIN, ER_LOGIN
from .erapi import Account, EnergyRadar, EnergyRadarException
from .hub import EnergyRadarHub

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

type EnergyRadarConfigEntry = ConfigEntry[api.ConfigEntryAuth]


async def async_setup_entry(hass: HomeAssistant, entry: EnergyRadarConfigEntry) -> bool:
    """Set up EnergyRadar from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    if CONF_TOKEN not in entry.data:
        raise ConfigEntryAuthFailed

    if DOMAIN not in hass.data.get("oauth2_flow_implementations", {}):
        er_vendor = EnergyRadar()

        config_entry_oauth2_flow.async_register_implementation(
            hass,
            DOMAIN,
            config_entry_oauth2_flow.LocalOAuth2Implementation(
                hass,
                DOMAIN,
                client_id="customers-app",
                client_secret="",
                authorize_url=er_vendor.auth_endpoint,
                token_url=er_vendor.token_endpoint,
            ),
        )

    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)

    try:
        await session.async_ensure_token_valid()
    except aiohttp.ClientResponseError as ex:
        _LOGGER.info("API error: %s (%s)", ex.code, ex.message)
        if ex.code in (401, 400, 403):
            raise ConfigEntryAuthFailed("Token not valid, trigger renewal") from ex
        raise ConfigEntryNotReady from ex

    er_session = api.ConfigEntryAuth(hass, entry, implementation)

    hass.data[DOMAIN][entry.entry_id] = er_session
    hub = EnergyRadarHub(hass, Account(er_session))

    # This is only here for debug purposes.
    # _LOGGER.info(er_session.token())

    try:
        await hass.async_add_executor_job(hub.update_meters)
    except EnergyRadarException as ex:
        _LOGGER.debug("Failed to connect to EnergyRadar API")
        raise ConfigEntryNotReady from ex

    hass.data[ER_LOGIN] = hub

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: EnergyRadarConfigEntry
) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
