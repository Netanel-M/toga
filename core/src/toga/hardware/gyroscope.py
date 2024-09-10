from __future__ import annotations

from typing import TYPE_CHECKING, Any

from toga.constants import FlashMode
from toga.handlers import AsyncResult, PermissionResult
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.app import App
    from toga.widgets.base import Widget


class GyroscopeDevice:
    def __init__(self, impl: Any):
        self._impl = impl

    @property
    def id(self) -> str:
        """A unique identifier for the device"""
        return self._impl.id()

    @property
    def name(self) -> str:
        """A human-readable name for the device"""
        return self._impl.name()

    def __eq__(self, other: Widget) -> bool:
        return self.id == other.id

    def __repr__(self) -> str:
        return f"<GyroscopeDevice id={self.id} {self.name!r}>"

    def __str__(self) -> str:
        return self.name


class Gyroscope:
    def __init__(self, app: App):
        self.factory = get_platform_factory()
        self._app = app
        self._impl = self.factory.Gyroscope(self)

    @property
    def app(self) -> App:
        return self._app

    def start(self, callback):
        self._impl.start(callback)
    
    def stop(self):
        self._impl.stop(callback)
