from typing import Callable, Any


def run_flow(when: bool, flow: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Ejecuta un flujo (callback) de pasos si la condición se cumple.
    Ideal para manejar bifurcaciones de lógica específicas de cada plataforma.

    Ejemplo de uso:
        # Importar el context para leer la plataforma:
        # from core.context import context

        # Ejecutar si es android
        # on_flow(context.platform == 'android', page.clear_cache)

        # Ejecutar con argumentos extra
        # on_flow(context.platform == 'ios', page.accept_apple_policy, timeout=5)
    """
    if when:
        return flow(*args, **kwargs)
