from core.action_logger import log_action
from core.waits import wait_visible


def assert_visible(locator: tuple[str, str], description: str = None) -> None:
    """
    Verifica que un elemento sea visible.
    """
    msg = description or f"Verificando visibilidad de: {locator}"
    with log_action(msg):
        element = wait_visible(locator)
        assert element.is_displayed()


def assert_enabled(locator: tuple[str, str], description: str = None) -> None:
    """
    Verifica que un elemento esté habilitado.
    """
    msg = description or f"Verificando que esté habilitado: {locator}"
    with log_action(msg):
        element = wait_visible(locator)
        assert (
            element.is_enabled()
        ), f"Error: El elemento {locator} debería estar habilitado pero está deshabilitado."


def assert_disabled(locator: tuple[str, str], description: str = None) -> None:
    """
    Verifica que un elemento esté deshabilitado.
    """
    msg = description or f"Verificando que esté deshabilitado: {locator}"
    with log_action(msg):
        element = wait_visible(locator)
        assert (
            not element.is_enabled()
        ), f"Error: El elemento {locator} debería estar deshabilitado pero está habilitado."
