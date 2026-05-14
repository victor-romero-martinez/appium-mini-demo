import re
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.appiumby import AppiumBy
from core.context import context
from core.waits import wait_visible


def tap_on(locator: tuple[str, str]) -> None:
    """
    Realiza un toque (tap) sobre un elemento identificado por el locador.
    Espera a que el elemento sea visible antes de interactuar.

    Ejemplo:
        tap_on((AppiumBy.ID, "com.example:id/login_button"))
    """
    element = wait_visible(locator)
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
    element = wait_visible(locator)
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


def get_text(locator: tuple[str, str]) -> str:
    """
    Obtiene el texto de un elemento.
    Espera a que el elemento sea visible antes de interactuar.

    Ejemplo:
        get_text((AppiumBy.ID, "com.example:id/login_button"))
    """
    element = wait_visible(locator)
    return (
        element.text or element.get_attribute("text") or element.get_attribute("label")
    )


def take_screenshot(filename: str, path: str = "reportes/screenshots") -> None:
    """
    Toma una captura de pantalla y la guarda en el directorio especificado.

    Ejemplo:
        take_screenshot("home_page.png")
    """
    import os

    os.makedirs(path, exist_ok=True)
    context.driver.save_screenshot(f"{path}/{filename}")


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


def swipe(
    direction: str,
    count: int = 1,
    locator: tuple[str, str] = None,
    container_locator: tuple[str, str] = None,
) -> None:
    """
    Realiza un deslizamiento (swipe) en la dirección especificada.

    Args:
        direction: 'up', 'down', 'left', 'right'.
        count: Cantidad máxima de swipes a realizar.
        locator: Opcional. Tupla (By, Value) para detener el swipe al encontrar el elemento.
        container_locator: Opcional. Tupla (By, Value) del elemento contenedor donde se hará el swipe.
    """
    # 1. Determinar el área de acción
    if container_locator:
        container = wait_visible(container_locator)
        rect = container.rect
        ax, ay, aw, ah = rect["x"], rect["y"], rect["width"], rect["height"]
    else:
        size = context.driver.get_window_size()
        ax, ay, aw, ah = 0, 0, size["width"], size["height"]

    # 2. Calcular coordenadas relativas al área (inicio y fin)
    coords = {
        "up": {
            "start": (ax + aw * 0.5, ay + ah * 0.8),
            "end": (ax + aw * 0.5, ay + ah * 0.2),
        },
        "down": {
            "start": (ax + aw * 0.5, ay + ah * 0.2),
            "end": (ax + aw * 0.5, ay + ah * 0.8),
        },
        "left": {
            "start": (ax + aw * 0.8, ay + ah * 0.5),
            "end": (ax + aw * 0.2, ay + ah * 0.5),
        },
        "right": {
            "start": (ax + aw * 0.2, ay + ah * 0.5),
            "end": (ax + aw * 0.8, ay + ah * 0.5),
        },
    }

    if direction not in coords:
        raise ValueError(
            f"Dirección inválida: {direction}. Use 'up', 'down', 'left' o 'right'."
        )

    start_x, start_y = coords[direction]["start"]
    end_x, end_y = coords[direction]["end"]

    for _ in range(count):
        # Verificar si el elemento objetivo ya es visible para detenerse
        if locator:
            try:
                elements = context.driver.find_elements(*locator)
                if elements and elements[0].is_displayed():
                    return
            except:
                pass

        # Ejecutar Swipe usando W3C Actions
        actions = ActionChains(context.driver)
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.6)  # Pausa para asegurar el swipe
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()


def back() -> None:
    """
    Navega hacia atrás en la aplicación.
    En Android equivale al botón físico/sistema 'Atrás'.
    En iOS intenta volver a la vista anterior si la navegación lo permite.
    """
    context.driver.back()
