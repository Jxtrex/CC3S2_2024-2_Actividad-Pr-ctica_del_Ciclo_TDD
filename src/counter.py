from flask import Flask
import src.status
from flask import request

app = Flask(__name__)

COUNTERS = {}

@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Crea un contador"""
    app.logger.info(f"Solicitud para crear el contador: {name}")
    global COUNTERS

    # Verifica si el contador ya existe
    if name in COUNTERS:
        return {"message": f"El contador {name} ya existe"}, src.status.HTTP_409_CONFLICT

    # Si no existe, inicializa el contador en 0
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, src.status.HTTP_201_CREATED


@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """Actualiza el valor de un contador"""
    global COUNTERS

    # Verifica si el contador existe
    if name not in COUNTERS:
        return {"message": f"El contador {name} no existe"}, src.status.HTTP_404_NOT_FOUND

    # Obtiene el nuevo valor del contador desde el cuerpo de la solicitud
    data = request.get_json()
    nuevoValor = data.get("valor")

    # Verifica que el nuevo valor sea un número entero
    if not isinstance(nuevoValor, int):
        return {"message": "El valor debe ser un entero"}, src.status.HTTP_400_BAD_REQUEST

    # Actualiza el valor del contador
    COUNTERS[name] = nuevoValor
    return {name: COUNTERS[name]}, src.status.HTTP_200_OK
