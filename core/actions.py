import re
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.appiumby import AppiumBy
from core.context import context
from core.waits import wait_is_visible


def tap_on(locator: tuple[str, str]) -> None:
    """
    Realiza un toque (tap) sobre un elemento identificado por el locador.
    Espera a que el elemento sea visible antes de interactuar.

    Ejemplo:
        tap_on((AppiumBy.ID, "com.example:id/login_button"))
    """
    element = wait_is_visible(locator)
    element.click()


def tap_at(x: int, y: int) -> None:
    """
    Realiza un toque (tap) en coordenadas específicas (x, y) de la pantalla.
    Usa el protocolo W3C Actions para mayor precisión.

    Ejemplo:
        tap_at(500, 1000)
    """
    actions = ActionChains(context.driver)
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pointer_up()
    actions.perform()


def input_text(locator: tuple[str, str], text: str) -> None:
    """
    Escribe texto en un campo de entrada.
    Espera a que el campo sea visible, hace clic para ganar foco y envía el texto.
    Intenta ocultar el teclado automáticamente al finalizar.

    Ejemplo:
        input_text((AppiumBy.ACCESSIBILITY_ID, "user_field"), "mi_usuario")
    """
    element = wait_is_visible(locator)
    element.click()
    actions = ActionChains(context.driver)
    actions.send_keys(text)
    actions.perform()

    if context.driver.is_keyboard_shown():
        try:
            context.driver.hide_keyboard()
        except Exception:
            # En iOS el ocultar teclado puede fallar dependiendo del estado del teclado
            pass


def scroll_until_visibliity(locator: tuple[str, str]) -> None:
    """
    Realiza un scroll hasta que el elemento indicado sea visible.
    En Android usa UiScrollable (nativo y rápido).
    En iOS usa el script 'mobile: scroll' (nativo).

    Ejemplo:
        scroll_until_visibliity((AppiumBy.ACCESSIBILITY_ID, "footer_element"))
    """
    platform = context.platform
    strategy, value = locator

    if platform == "android":
        selector = None
        if strategy == AppiumBy.ID:
            resource_id = value.split(":id/")[-1]
            selector = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().resourceIdMatches(".*{resource_id}"))'
        elif strategy == AppiumBy.ACCESSIBILITY_ID:
            selector = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("{value}"))'
        elif strategy == AppiumBy.XPATH and "@text=" in value:
            text_match = re.search(r"@text=['\"](.*?)['\"]", value)
            if text_match:
                text = text_match.group(1)
                selector = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))'

        if selector:
            context.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)

    elif platform == "ios":
        element = context.driver.find_element(*locator)
        context.driver.execute_script(
            "mobile: scroll", {"elementId": element.id, "toVisible": True}
        )
