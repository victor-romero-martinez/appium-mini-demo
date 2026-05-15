# Directorio de Tests

Aquí se encuentran los casos de prueba automatizados.

## Reglas
- **Limpieza**: Los tests deben ser legibles y enfocados en el "qué" y no en el "cómo".
- **Abstracción**: Usar las acciones de `core.actions` y locators de `pages`.
- **Independencia**: Cada test debe poder ejecutarse de forma independiente.

## Ejemplo
```python
from core.actions import *
from pages.welcome_page import *

def test_navigation_to_home():
    tap_on(START_BUTTON)
    # Aserción aquí
```
