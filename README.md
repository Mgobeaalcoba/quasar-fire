# Quasar Fire Project

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FMgobeaalcoba%2Fquasar-fire&label=Visitors&countColor=%23263759)

## Description

This project is a solution for the "Quasar Fire" challenge. It is a REST API that allows to obtain the position of a distress signal and the message sent by a ship in a given sector of the galaxy.

## Technologies

- Python 3.12
- FastAPI 0.111.0
- Pydantic 1.11.0
- SQLAlchemy 1.4.30

## Installation

To install the project, you must have Python 3.12 installed on your computer. Then, you must clone the repository and install the dependencies with the following commands:

```bash
$ git clone 
$ cd quasar-fire
$ pip install -r requirements.txt
```

## Usage

To run the project, you must execute the following command:

```bash
$ uvicorn app.main:app --reload
```

This will start the server on `http://localhost:8000`.
You can test the endpoints using the Swagger UI or the OpenAPI documentation available at `http://localhost:8000/docs` or `http://localhost:8000/redoc` respectively.

## Endpoints

The API has the following endpoints:

- `POST /topsecret`: Allows to obtain the position and message of a distress signal from the three satellites.
- `PUT /topsecret_split/{satellite_name}`: Allows to update the information of a satellite.
- `GET /topsecret_split/{satellite_name}`: Allows to obtain the position and message of a distress signal from the satellites.

## Database

The project uses a SQLite database to store the information of the satellites. The database is created automatically when the application starts, and the tables are created if they do not exist.

## Service

The project has a service layer that is responsible for processing the information received from the satellites and obtaining the position and message of the distress signal. The service layer uses the trilateration algorithm to calculate the position of the signal.

## Tests

In progress...

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more information.

## Contact

Mariano Gobea Alcoba - [email](gobeamariano@gmail.com)
