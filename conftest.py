import json
import os
import pytest
import subprocess
from dotenv import load_dotenv

# Cargar variables de entorno al inicio de la ejecución de los tests
load_dotenv()

from core.context import context
from core.driver_factory import create_driver


@pytest.fixture(scope="function", autouse=True)
def setup_driver():
    context.driver = create_driver()

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
