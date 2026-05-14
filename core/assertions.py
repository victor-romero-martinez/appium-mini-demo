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
