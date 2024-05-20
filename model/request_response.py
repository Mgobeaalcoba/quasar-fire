from pydantic import BaseModel

from .data_class import Satellite


class Request(BaseModel):
    """Request model."""
    satellites: list[Satellite]

    def set_satellites(self, satellites: list[Satellite]) -> None:
        self.satellites = satellites
