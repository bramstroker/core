"""Support for VELUX scenes."""
from typing import Any, Callable

from homeassistant.components.scene import Scene
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from . import _LOGGER, DATA_VELUX


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[list[Entity], bool], None],
) -> None:
    """Set up the scenes for Velux platform."""
    entities = [VeluxScene(scene) for scene in hass.data[DATA_VELUX].pyvlx.scenes]
    async_add_entities(entities)


class VeluxScene(Scene):
    """Representation of a Velux scene."""

    def __init__(self, scene):
        """Init velux scene."""
        _LOGGER.info("Adding Velux scene: %s", scene)
        self.scene = scene

    @property
    def name(self):
        """Return the name of the scene."""
        return self.scene.name

    async def async_activate(self, **kwargs: Any) -> None:
        """Activate the scene."""
        await self.scene.run(wait_for_completion=False)
