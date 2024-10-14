"""Config flow for EnergyRadar."""

from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import SOURCE_REAUTH, ConfigFlowResult
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.config_entry_oauth2_flow import (
    AbstractOAuth2FlowHandler,
    LocalOAuth2Implementation,
)

from .const import DOMAIN
from .erapi import EnergyRadar

_LOGGER = logging.getLogger(__name__)


class OAuth2FlowHandler2(AbstractOAuth2FlowHandler, domain=DOMAIN):
    """Config flow to handle EnergyRadar OAuth2 authentication."""

    DOMAIN = DOMAIN

    def __init__(self) -> None:
        """Instantiate config flow."""
        super().__init__()
        self.external_data: Any = None
        self.flow_impl: LocalOAuth2Implementation = None  # type: ignore[assignment]

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    async def async_step_user(self, user_input=None) -> config_entries.ConfigFlowResult:
        """Handle a flow start."""
        # Ensure OAuth2 implementation is registered
        if DOMAIN not in self.hass.data.get("oauth2_flow_implementations", {}):
            er_vendor = EnergyRadar()

            config_entry_oauth2_flow.async_register_implementation(
                self.hass,
                DOMAIN,
                config_entry_oauth2_flow.LocalOAuth2Implementation(
                    self.hass,
                    DOMAIN,
                    client_id="customers-app",
                    client_secret="",
                    authorize_url=er_vendor.auth_endpoint,
                    token_url=er_vendor.token_endpoint,
                ),
            )

        return await self.async_step_pick_implementation(user_input)

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon migration of old entries."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm reauth upon migration of old entries."""
        if user_input is None:
            return self.async_show_form(step_id="reauth_confirm")
        return await self.async_step_user()

    async def async_oauth_create_entry(self, data: dict[str, Any]) -> ConfigFlowResult:
        """Create an entry for the flow. Update an entry if one already exist."""
        current_entries = self._async_current_entries()
        if self.source == SOURCE_REAUTH and current_entries:
            # Update entry
            self.hass.config_entries.async_update_entry(
                current_entries[0], title="EnergyRadar", data=data
            )
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(current_entries[0].entry_id)
            )
            return self.async_abort(reason="reauth_successful")
        return self.async_create_entry(title="EnergyRadar", data=data)
