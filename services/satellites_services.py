from sqlalchemy.orm import Session
from model.data_class import Satellite, Coordinates
from repository.database import SatelliteDB, db_to_satellite, Session
from scipy.optimize import minimize
import numpy as np


class SatelliteService(object):
    """
    This class provides methods to interact with the satellites in the database.

    Methods include adding a new satellite, upgrading an existing satellite,
    the recovery of a satellite by name and the recovery of all satellites.

    Also provides methods to calculate coordinates based on satellite information
    and to obtain a message from the satellite message fragments.
    """
    session: Session = Session()

    @classmethod
    def add_satellite(cls, satellite: Satellite) -> None:
        """
        Add a new satellite to the database or update an existing satellite.

            :param satellite: The satellite to add or update.
            :return: None
        """
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
        """
        Update an existing satellite in the database.

            :param satellite: The satellite to update.
            :return: None
        """
        satellite_db = cls.session.query(SatelliteDB).filter(SatelliteDB.name == satellite.name).first()
        if satellite_db:
            satellite_db.distance = satellite.distance
            satellite_db.x = satellite.coordinates.x
            satellite_db.y = satellite.coordinates.y
            satellite_db.message = ",".join(satellite.message)
            cls.session.commit()

    @classmethod
    def get_satellite(cls, satellite_name: str) -> Satellite:
        """
        Get a satellite from the database by name.

            :param satellite_name: The name of the satellite to get.
            :return: The satellite with the given name.
        """
        satellite_db = cls.session.query(SatelliteDB).filter(SatelliteDB.name == satellite_name).first()
        if satellite_db:
            return db_to_satellite(satellite_db)
        raise Exception("Satellite not found")

    @classmethod
    def get_satellites(cls) -> list[Satellite]:
        """
        Get all satellites from the database.

            :return: A list of all satellites in the database.
        """
        satellites_db = cls.session.query(SatelliteDB).all()
        return [db_to_satellite(satellite_db) for satellite_db in satellites_db]

    @classmethod
    def get_coordinates(cls, satellites: list[Satellite]) -> Coordinates:
        """
        Get the coordinates of the point where the message was sent based on satellite information.

            :param satellites: A list of satellites with the information of the distance and the coordinates.
            :return: The coordinates of the point where the message was sent.
        """

        def objective(x, locations, distances):
            return sum([(np.linalg.norm(x - locations[i]) - distances[i]) ** 2 for i in range(len(locations))])

        locations = np.array([np.array([satellite.coordinates.x, satellite.coordinates.y]) for satellite in satellites])
        distances = np.array([satellite.distance for satellite in satellites])

        x0 = np.mean(locations, axis=0)

        result = minimize(objective, x0, args=(locations, distances), method='L-BFGS-B')

        return Coordinates(x=result.x[0], y=result.x[1])

    @classmethod
    def get_message(cls, satellites: list[Satellite]) -> str:
        """
        Get the complete message from the satellite message fragments.

            :param satellites: A list of satellites with the information of the message.
            :return: The complete message.
        """
        message_fragments = [satellite.message for satellite in satellites]
        message = []

        for fragments in zip(*message_fragments):
            for fragment in fragments:
                if fragment:
                    message.append(fragment)
                    break

        message = " ".join(message)

        return message
