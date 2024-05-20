from model.data_class import Satellite, Coordinates


class SatelliteService(object):
    satellites: list[Satellite] = []

    @classmethod
    def add_satellite(cls, satellite: Satellite) -> None:
        cls.satellites.append(satellite)

    @classmethod
    def update_satellite(cls, satellite: Satellite) -> None:
        for i, s in enumerate(cls.satellites):
            if s.name == satellite.name:
                cls.satellites[i] = satellite
                break

    @classmethod
    def get_satellite(cls, satellite_name: str) -> Satellite:
        for satellite in cls.satellites:
            if satellite.name == satellite_name:
                return satellite
        raise Exception("Satellite not found")

    @classmethod
    def get_satellites(cls) -> list[Satellite]:
        return cls.satellites

    @classmethod
    def get_coordinates(cls, satellites: list[Satellite]) -> Coordinates:
        return Coordinates(x=0.0, y=0.0)

    @classmethod
    def get_message(cls, satellites: list[Satellite]) -> str:
        return "This is a message"

    @classmethod
    def get_distance(cls, satellites: list[Satellite]) -> float:
        return 100.0
