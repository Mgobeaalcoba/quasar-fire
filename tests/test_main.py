from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_top_secret():
    response = client.post(
        "/topsecret",
        json={
            "satellites": [
                {
                    "name": "kenobi",
                    "distance": 0,
                    "coordinates": {
                        "x": 15,
                        "y": 50
                    },
                    "message": [
                        "Hola",
                        "",
                        "esto",
                        "",
                        "",
                        "mensaje",
                        ""
                    ]
                },
                {
                    "name": "skywalker",
                    "distance": 0,
                    "coordinates": {
                        "x": 65,
                        "y": 90
                    },
                    "message": [
                        "",
                        "soldado",
                        "esto",
                        "",
                        "",
                        "mensaje",
                        ""
                    ]
                },
                {
                    "name": "sato",
                    "distance": 0,
                    "coordinates": {
                        "x": 23,
                        "y": 180
                    },
                    "message": [
                        "",
                        "soldado",
                        "",
                        "es",
                        "un",
                        "",
                        ""
                    ]
                }
            ]
        }
    )
    assert response.status_code == 200
    assert "coordinates" in response.json()
    assert "message" in response.json()


def test_top_secret_split_put():
    response = client.put(
        "/topsecret_split/kenobi",
        json={
            "name": "kenobi",
            "distance": 0,
            "coordinates": {
                "x": 180,
                "y": 180
            },
            "message": ["Este", "es", "otro", "", "", "mensaje", ""]
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "kenobi",
        "distance": 0,
        "coordinates": {
            "x": 180,
            "y": 180
        },
        "message": ["Este", "es", "otro", "", "", "mensaje", ""]
    }


def test_top_secret_split_get():
    response = client.get("/topsecret_split/kenobi")
    assert response.status_code == 200
    assert response.json() == {
        "name": "kenobi",
        "distance": 0,
        "coordinates": {
            "x": 180,
            "y": 180
        },
        "message": ["Este", "es", "otro", "", "", "mensaje", ""]
    }
