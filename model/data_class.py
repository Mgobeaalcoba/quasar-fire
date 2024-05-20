from pydantic import BaseModel

from .enum_class import SatelliteName


class Coordinates(BaseModel):
    """Coordinates model."""
    x: float
    y: float


class Satellite(BaseModel):
    name: SatelliteName
    distance: float = 0.0
    coordinates: Coordinates
    message: list[str] = []

    def set_distance(self, distance: float) -> None:
        self.distance = distance

    def set_coordinates(self, coordinates: Coordinates) -> None:
        self.coordinates = coordinates

    def set_message(self, message: list[str]) -> None:
        self.message = message
