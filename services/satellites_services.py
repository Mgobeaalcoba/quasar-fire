from sqlalchemy.orm import Session
from model.data_class import Satellite, Coordinates
from repository.database import SatelliteDB, satellite_to_db, db_to_satellite, Session
from scipy.optimize import minimize
import numpy as np


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
        # Definir la función objetivo para minimizar
        def objective(x, locations, distances):
            return sum([(np.linalg.norm(x - locations[i]) - distances[i]) ** 2 for i in range(len(locations))])

        # Obtener las ubicaciones y distancias de los satélites
        locations = np.array([np.array([satellite.coordinates.x, satellite.coordinates.y]) for satellite in satellites])
        distances = np.array([satellite.distance for satellite in satellites])

        # Estimar la ubicación inicial como el centroide de las ubicaciones de los satélites
        x0 = np.mean(locations, axis=0)

        # Minimizar la función objetivo
        result = minimize(objective, x0, args=(locations, distances), method='L-BFGS-B')

        # Devolver las coordenadas resultantes
        return Coordinates(x=result.x[0], y=result.x[1])

    @classmethod
    def get_message(cls, satellites: list[Satellite]) -> str:
        # Crear una lista de listas para almacenar los fragmentos de mensajes de cada satélite
        message_fragments = [satellite.message for satellite in satellites]

        # Crear una lista vacía para almacenar el mensaje reconstruido
        message = []

        # Iterar sobre las listas de fragmentos de mensajes en paralelo
        for fragments in zip(*message_fragments):
            # Agregar al mensaje el primer fragmento que no sea una cadena vacía
            for fragment in fragments:
                if fragment:
                    message.append(fragment)
                    break

        # Unir los fragmentos de mensajes en un solo mensaje
        message = " ".join(message)

        # Devolver el mensaje
        return message

