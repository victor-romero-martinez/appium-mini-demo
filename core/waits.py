from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.context import context


def wait_is_visible(locator: tuple[str, str], timeout: int = 10) -> WebElement:
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
