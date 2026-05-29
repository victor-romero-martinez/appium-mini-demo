import json
import os
import pytest
import subprocess
from dotenv import load_dotenv

# Cargar variables de entorno al inicio de la ejecución de los tests
load_dotenv()

from core.context import context
from core.driver_factory import create_driver


def _load_device_config(platform: str, worker_id: str) -> dict:
    """
    Carga la configuración de un dispositivo del pool definido en devices.json.
    Asigna un dispositivo exclusivo a cada worker según su índice numérico.
    Si no hay pool o no hay suficientes dispositivos, hace fallback a las variables .env.
    """
    devices = []
    if os.path.exists("devices.json"):
        try:
            with open("devices.json", "r") as f:
                config = json.load(f)
                devices = config.get(platform, [])
        except Exception as e:
            print(f"[conftest] Error al leer devices.json: {e}")

    # Extraer el índice del worker (ej: 'gw0' -> 0, 'gw1' -> 1, 'master' -> 0)
    index = 0
    if worker_id.startswith("gw"):
        try:
            index = int(worker_id[2:])
        except ValueError:
            pass

    if index < len(devices):
        return devices[index]

    # Fallback a variables de entorno si no hay pool suficiente
    return {
        "deviceName": os.getenv("DEVICE_NAME"),
        "platformVersion": os.getenv("PLATFORM_VERSION"),
        "udid": os.getenv("UDID"),
        "systemPort": 8200 + index,
        "wdaLocalPort": 8100 + index,
    }


@pytest.fixture(scope="session")
def worker_id(request):
    """Retorna el id del worker asignado por pytest-xdist, o 'master' si es secuencial."""
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["workerid"]
    return "master"


@pytest.fixture(scope="session", autouse=True)
def setup_driver(worker_id):
    platform = os.getenv("PLATFORM_NAME", "android").lower()
    device_config = _load_device_config(platform, worker_id)

    context.driver = create_driver(device_config)

    yield

    if context.driver:
        context.driver.quit()


@pytest.fixture(scope="session")
def current_platform():
    return context.platform


@pytest.fixture(scope="session", autouse=True)
def disconnected_wdr(request):
    yield

    if context.driver:
        platform = context.platform
        if platform != "ios":
            return

        try:
            subprocess.run(["pkill", "-f", "WebDriverAgentRunner"], check=True)
        except Exception as e:
            print(f"No se pudo detener el proceso WebDriverAgentRunner: {e}")
