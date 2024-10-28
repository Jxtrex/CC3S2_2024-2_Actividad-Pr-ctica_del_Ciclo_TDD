"""
Casos de prueba para el servicio web de contador
"""
import pytest
from src.counter import app
from http import HTTPStatus

@pytest.fixture
def client():
    # Configuración del cliente de prueba de Flask
    return app.test_client()

  

def test_create_a_counter(client):
    """Debe crear un contador"""
    result = client.post("/counters/test_counter")
    
    data = result.get_json()

    assert result.status_code == HTTPStatus.CREATED
    assert "test_counter" in data
    assert data["test_counter"] == 0

def test_duplicate_counter(client):
    """Debe devolver un error para duplicados"""
    
    result1 = client.post("/counters/test_counter1")
    
    result2 = client.post("/counters/test_counter1")
    assert result1.status_code == HTTPStatus.CREATED
    assert result2.status_code == HTTPStatus.CONFLICT


def test_update_a_counter(client):
    """Debe actualizar el valor de un contador existente"""
    # Crear el contador antes de intentar actualizarlo
    client.post("/counters/test_counter2")

    # Actualizar el contador con un nuevo valor
    response = client.put("/counters/test_counter2", json={"valor": 10})
    
    data = response.get_json()
    assert response.status_code == HTTPStatus.OK
    assert data["test_counter2"] == 10

def test_update_a_counter_invalid_data(client):
    """Debe devolver un error para datos inváldos"""
    # Crear el contador antes de intentar actualizarlo
    client.post("/counters/test_counter4")

    # Actualizar el contador con un nuevo valor
    response = client.put("/counters/test_counter4", json={"valor": "abc"})
    data = response.get_json()

    assert response.status_code == HTTPStatus.BAD_REQUEST