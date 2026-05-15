import time
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.context import context


def wait_visible(locator: tuple[str, str], timeout: int = 10) -> WebElement:
    """
    Espera explícita hasta que un elemento sea visible en el DOM y en la pantalla.

    Args:
        locator: Tupla (By, Value).
        timeout: Tiempo máximo de espera en segundos (por defecto 10).

    Returns:
        WebElement: El elemento encontrado.
    """
    return WebDriverWait(context.driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def wait_for_animation_end(locator: tuple[str, str] = None, timeout: int = 5) -> None:
    """
    Espera a que las animaciones terminen.

    Si se proporciona un locator, espera a que ese elemento específico deje de moverse
    (estabilidad de coordenadas x, y y tamaño).
    Si no se proporciona, intenta usar configuraciones del driver para esperar a que
    la aplicación esté en estado 'ocioso' (idle/quiescence).

    Args:
        locator: Opcional, tupla (By, Value) del elemento a monitorear.
        timeout: Tiempo máximo de espera en segundos.
    """
    if locator:
        element = wait_visible(locator, timeout)
        end_time = time.time() + timeout
        last_rect = None

        while time.time() < end_time:
            # rect devuelve {'x':..., 'y':..., 'width':..., 'height':...}
            current_rect = element.rect
            if last_rect == current_rect:
                return  # El elemento se ha estabilizado
            last_rect = current_rect
            time.sleep(0.3)  # Intervalo corto para detectar movimiento
    else:
        # Espera global basada en settings del driver
        platform = context.platform
        if platform == "android":
            context.driver.update_settings({"waitForIdleTimeout": 1000})
            # Forzamos una operación ligera para que el driver aplique el wait for idle
            _ = context.driver.current_package
        elif platform == "ios":
            context.driver.update_settings({
                "waitForQuiescence": True,
                "animationIdlenessTimeout": timeout
            })
            # Forzamos una operación ligera
            _ = context.driver.orientation
