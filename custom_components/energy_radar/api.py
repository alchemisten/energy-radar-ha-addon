"""API for EnergyRadar bound to Home Assistant OAuth."""

from __future__ import annotations

from asyncio import run_coroutine_threadsafe

from homeassistant import config_entries, core
from homeassistant.components.application_credentials import AuthImplementation
from homeassistant.helpers import config_entry_oauth2_flow

from .erapi import EnergyRadar, OAuthSession


class ConfigEntryAuth(OAuthSession):
    """Provide EnergyRadar authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        hass: core.HomeAssistant,
        config_entry: config_entries.ConfigEntry,
        implementation: config_entry_oauth2_flow.AbstractOAuth2Implementation,
    ) -> None:
        """Initialize EnergyRadar Auth."""
        self.hass = hass
        self.session = config_entry_oauth2_flow.OAuth2Session(
            hass, config_entry, implementation
        )
        super().__init__(self.session.token, vendor=EnergyRadar())

    def refresh_tokens(self) -> dict:
        """Refresh and return new Neato Botvac tokens."""
        run_coroutine_threadsafe(
            self.session.async_ensure_token_valid(), self.hass.loop
        ).result()

        return self.session.token

    def token(self):
        """Get session token, used for debug purposes."""
        return self.session.token


class EnergyRadarImplementation(AuthImplementation):
    """EnergyRadar implementation of LocalOAuth2Implementation.

    We need this class because we have to add scope to authorization request.
    """

    async def async_generate_authorize_url(self, flow_id: str) -> str:
        """Generate a url for the user to authorize."""
        url = await super().async_generate_authorize_url(flow_id)
        return f"{url}&scope=user_meters"
