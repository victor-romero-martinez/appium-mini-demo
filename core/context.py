from appium.webdriver.webdriver import WebDriver


class Context:
    """
    Clase para mantener el estado global de la ejecución, 
    principalmente la instancia del driver de Appium.
    """
    driver: WebDriver | None = None


context = Context()
