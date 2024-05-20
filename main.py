from fastapi import FastAPI, Body, Response, Path

from fastapi.responses import JSONResponse

from model.request_response import Request
from model.data_class import Coordinates, Satellite
from services.satellites_services import SatelliteService

from typing import Annotated, List

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/topsecret", response_model=None)
async def top_secret(
        request: Annotated[Request, Body(
            ...,
            title="List of satellites with the information of the distance and the message that they sent.",
            description="List of satellites with the information of the distance and the message that they sent.",
            openapi_examples={
                "normal": {
                    "summary": "Example of a normal request",
                    "value": {
                        "satellites": [
                            {
                                "name": "kenobi",
                                "distance": 0,
                                "coordinates": {
                                    "x": 15,
                                    "y": 50
                                },
                                "message": ["Hola", "", "esto", "", "", "mensaje", ""]
                            },
                            {
                                "name": "skywalker",
                                "distance": 0,
                                "coordinates": {
                                    "x": 65,
                                    "y": 90
                                },
                                "message": ["", "soldado", "esto", "", "", "mensaje", ""]
                            },
                            {
                                "name": "sato",
                                "distance": 0,
                                "coordinates": {
                                    "x": 23,
                                    "y": 180
                                },
                                "message": ["", "soldado", "", "es", "un", "", ""]
                            }
                        ]
                    }

                }
            }
        )]
) -> dict | Response:
    """
    This endpoint receives a list of satellites with the information of the distance and the message that they sent.
    It returns the coordinates of the point where the message was sent and the complete message.

        :param request: Request model with the list of satellites.
        :return: Dictionary with the coordinates of the point where the message was sent and the complete message.
    """
    try:
        satellites: List[Satellite] = request.satellites
        for satellite in satellites:
            SatelliteService.add_satellite(satellite)

        coordinates: Coordinates = SatelliteService.get_coordinates(satellites)
        message: str = SatelliteService.get_message(satellites)
        return {"coordinates": coordinates, "message": message}
    except Exception as e:
        return JSONResponse(status_code=404, content={"message ": str(e)})


@app.put("/topsecret_split/{satellite_name}", response_model=None)
async def top_secret_split(
        satellite_name: Annotated[str, Path()],
        satellite: Annotated[Satellite, Body(
            ...,
            title="Satellite with the information of the distance, coordinates and the message that it sent.",
            description="Satellite with the information of the distance, coordinates and the message that it sent."
        )]
) -> Satellite | Response:
    """
    This endpoint receives a satellite with the information of the distance, coordinates and the message that it sent.
    It updates the information of the satellite in the database.

        :param satellite: Satellite model with the information of the distance, coordinates and the message that it sent.
        :param satellite_name: Name of the satellite.
        :return: Satellite model with the information of the distance, coordinates and the message that it sent.
    """
    try:
        if satellite_name != satellite.name:
            return JSONResponse(status_code=400, content={"message ": "The name of the satellite is not the same in "
                                                                      "the path and in the body."})
        SatelliteService.update_satellite(satellite)
        return satellite
    except Exception as e:
        return JSONResponse(status_code=404, content={"message ": str(e)})


@app.get("/topsecret_split/{satellite_name}", response_model=None)
async def get_satellite(
        satellite_name: Annotated[str, Path()],
) -> Satellite | Response:
    """
    This endpoint receives a satellite name and returns the information of the satellite.

        :param satellite_name: Name of the satellite.
        :return: Satellite model with the information of the distance, coordinates and the message that it sent
    """
    try:
        satellite: Satellite = SatelliteService.get_satellite(satellite_name)
        return satellite
    except Exception as e:
        return JSONResponse(status_code=404, content={"message ": str(e)})




