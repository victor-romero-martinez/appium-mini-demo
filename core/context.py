from appium.webdriver.webdriver import WebDriver


class Context:
    """
    Clase para mantener el estado global de la ejecución, 
    principalmente la instancia del driver de Appium.
    """
    driver: WebDriver | None = None

    @property
    def platform(self) -> str:
        """Retorna la plataforma actual en minúsculas (ej: 'android' o 'ios')."""
        if self.driver and self.driver.capabilities:
            return self.driver.capabilities.get("platformName", "").lower()
        return ""


context = Context()
