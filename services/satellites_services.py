from sqlalchemy.orm import Session
from model.data_class import Satellite, Coordinates
from repository.database import SatelliteDB, satellite_to_db, db_to_satellite, Session

class SatelliteService(object):
    session: Session = Session()

    @classmethod
    def add_satellite(cls, satellite: Satellite) -> None:

        satellite_db = cls.session.query(SatelliteDB).filter(SatelliteDB.name == satellite.name).first()
        if satellite_db:
            satellite_db.distance = satellite.distance
            satellite_db.x = satellite.coordinates.x
            satellite_db.y = satellite.coordinates.y
            satellite_db.message = ",".join(satellite.message)
            cls.session.commit()
        else:
            cls.session.add(satellite_db)
            cls.session.commit()

    @classmethod
    def update_satellite(cls, satellite: Satellite) -> None:
        satellite_db = cls.session.query(SatelliteDB).filter(SatelliteDB.name == satellite.name).first()
        if satellite_db:
            satellite_db.distance = satellite.distance
            satellite_db.x = satellite.coordinates.x
            satellite_db.y = satellite.coordinates.y
            satellite_db.message = ",".join(satellite.message)
            cls.session.commit()

    @classmethod
    def get_satellite(cls, satellite_name: str) -> Satellite:
        satellite_db = cls.session.query(SatelliteDB).filter(SatelliteDB.name == satellite_name).first()
        if satellite_db:
            return db_to_satellite(satellite_db)
        raise Exception("Satellite not found")

    @classmethod
    def get_satellites(cls) -> list[Satellite]:
        satellites_db = cls.session.query(SatelliteDB).all()
        return [db_to_satellite(satellite_db) for satellite_db in satellites_db]

    @classmethod
    def get_coordinates(cls, satellites: list[Satellite]) -> Coordinates:
        return Coordinates(x=0.0, y=0.0)

    @classmethod
    def get_message(cls, satellites: list[Satellite]) -> str:
        return "This is a message"

    @classmethod
    def get_distance(cls, satellites: list[Satellite]) -> float:
        return 100.0