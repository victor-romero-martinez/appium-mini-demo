from core.waits import wait_visible


def assert_visible(locator: tuple[str, str]) -> None:
    """
    Verifica que un elemento sea visible en la pantalla.
    Lanza una AssertionError si el elemento no aparece dentro del tiempo de espera.

    Ejemplo:
        assert_visible((AppiumBy.ID, "welcome_message"))
    """
    element = wait_visible(locator)
    assert element.is_displayed()


def assert_enabled(locator: tuple[str, str]) -> None:
    """
    Verifica que un elemento esté habilitado (enabled).
    Ejemplo:
        assert_enabled((AppiumBy.ID, "welcome_message"))
    """
    element = wait_visible(locator)
    assert (
        element.is_enabled()
    ), f"Error: El elemento {locator} debería estar habilitado pero está deshabilitado."


def assert_disabled(locator: tuple[str, str]) -> None:
    """
    Verifica que un elemento esté deshabilitado (disabled).
    Ejemplo:
        assert_disabled((AppiumBy.ID, "welcome_message"))
    """
    element = wait_visible(locator)
    assert (
        not element.is_enabled()
    ), f"Error: El elemento {locator} debería estar deshabilitado pero está habilitado."
