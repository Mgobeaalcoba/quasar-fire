from sqlalchemy import Column, String, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from model.data_class import Satellite, Coordinates

Base = declarative_base()


class SatelliteDB(Base):
    __tablename__ = "satellites"

    name = Column(String, primary_key=True)
    distance = Column(Float)
    x = Column(Float)
    y = Column(Float)
    message = Column(String)


def satellite_to_db(satellite):
    return SatelliteDB(
        name=satellite.name,
        distance=satellite.distance,
        x=satellite.coordinates.x,
        y=satellite.coordinates.y,
        message=",".join(satellite.message),
    )


def db_to_satellite(satellite_db):
    return Satellite(
        name=satellite_db.name,
        distance=satellite_db.distance,
        coordinates=Coordinates(x=satellite_db.x, y=satellite_db.y),
        message=satellite_db.message.split(","),
    )


# Crear una base de datos SQLite en memoria y una sesión de SQLAlchemy
# engine = create_engine('sqlite:///databases/satellites.db')
engine = create_engine('sqlite:////Users/mgobea/Documents/Personal_Develop/fuegoQuasarProject/databases/satellites.db')
Session = sessionmaker(bind=engine)

# Crear la tabla satellites en la base de datos
Base.metadata.create_all(engine)
