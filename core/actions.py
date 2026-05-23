import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from appium.webdriver.common.appiumby import AppiumBy
from core.action_logger import log_action
from core.context import context
from core.waits import wait_visible


def tap_on(locator: tuple[str, str], description: str = None) -> None:
    """
    Realiza un toque (tap) sobre un elemento.
    """
    msg = description or f"Tocando en el elemento: {locator}"
    with log_action(msg):
        element = wait_visible(locator)
        element.click()


def tap_at(x: int, y: int, description: str = None) -> None:
    """
    Realiza un toque (tap) en coordenadas específicas (x, y).
    """
    msg = description or f"Tocando en coordenadas: ({x}, {y})"
    with log_action(msg):
        x, y = int(x), int(y)
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions = ActionBuilder(context.driver, mouse=finger)

        finger.create_pointer_move(duration=0, x=x, y=y)
        finger.create_pointer_down(button=0)
        finger.create_pointer_up(button=0)

        actions.perform()


def input_text(locator: tuple[str, str], text: str, description: str = None) -> None:
    """
    Escribe texto en un campo de entrada.
    """
    msg = description or f"Escribiendo '{text}' en: {locator}"
    with log_action(msg):
        element = wait_visible(locator)
        element.click()
        actions = ActionChains(context.driver)
        actions.send_keys(text)
        actions.perform()

        if context.driver.is_keyboard_shown():
            try:
                context.driver.hide_keyboard()
            except Exception:
                pass


def get_text(locator: tuple[str, str], description: str = None) -> str:
    """
    Obtiene el texto de un elemento.
    """
    msg = description or f"Obteniendo texto de: {locator}"
    with log_action(msg):
        element = wait_visible(locator)
        return (
            element.text
            or element.get_attribute("text")
            or element.get_attribute("label")
        )


def take_screenshot(
    filename: str, path: str = "reportes/screenshots", description: str = None
) -> None:
    """
    Toma una captura de pantalla.
    """
    import os

    msg = description or f"Guardando captura de pantalla: {filename}"
    with log_action(msg):
        os.makedirs(path, exist_ok=True)
        context.driver.save_screenshot(f"{path}/{filename}")


def scroll_until_visibility(locator: tuple[str, str], description: str = None) -> None:
    """
    Realiza un scroll hasta que el elemento sea visible.
    """
    msg = description or f"Haciendo scroll hasta encontrar: {locator}"
    platform = context.platform
    strategy, value = locator

    with log_action(msg):
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
    description: str = None,
) -> None:
    """
    Realiza un deslizamiento (swipe).
    """
    msg = description or f"Haciendo swipe hacia {direction}"
    with log_action(msg):
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

        # Asegurar coordenadas enteras
        start_x, start_y = int(start_x), int(start_y)
        end_x, end_y = int(end_x), int(end_y)

        for _ in range(count):
            # Verificar si el elemento objetivo ya es visible para detenerse
            if locator:
                try:
                    elements = context.driver.find_elements(*locator)
                    if elements and elements[0].is_displayed():
                        return
                except:
                    pass

            # Ejecutar Swipe usando W3C Actions (Touch Pointer)
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            actions = ActionBuilder(context.driver, mouse=finger)

            finger.create_pointer_move(duration=0, x=start_x, y=start_y)
            finger.create_pointer_down(button=0)
            finger.create_pointer_move(duration=600, x=end_x, y=end_y)
            finger.create_pointer_up(button=0)

            actions.perform()


def back(description: str = None) -> None:
    """
    Vuelve atrás.
    """
    msg = description or "Navegando hacia atrás"
    with log_action(msg):
        context.driver.back()
