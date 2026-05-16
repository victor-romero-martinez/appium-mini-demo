# Guía de Uso del Framework

Este framework está diseñado para facilitar la automatización de pruebas móviles utilizando Appium y Pytest.

## Estructura del Proyecto

- `core/`: Contiene la lógica base del framework, acciones comunes y configuración del driver.
- `pages/`: **IMPORTANTE** Aquí se deben definir únicamente los locators (locators) de cada pantalla. No debe contener lógica de negocio ni acciones complejas.
- `tests/`: Contiene los archivos de prueba. Se espera que los tests sean limpios y utilicen las acciones de `core` junto con los locators de `pages`.
- `docs/`: Documentación detallada del proyecto.

## Cómo escribir un Test

Para mantener el proyecto organizado y escalable, seguimos el patrón de separar los locators de la lógica del test.

### 1. Definir locators en `pages/`

Crea un archivo por pantalla en `pages/`. Por ejemplo, `pages/login_page.py`:

```python
from appium.webdriver.common.appiumby import AppiumBy

USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "username_input")
PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "password_input")
LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "login_btn")
```

### 2. Escribir el Test en `tests/`

Utiliza las acciones de `core.actions` y los locators definidos. Se recomienda el uso de `import *` para mantener el test limpio. Ejemplo `tests/test_login.py`:

```python
from core.actions import *
from pages.login_page import *

def test_successful_login():
    input_text(USERNAME_FIELD, "usuario_demo")
    input_text(PASSWORD_FIELD, "password123")
    tap_on(LOGIN_BUTTON)
    # Agregar aserciones usando core.assertions si es necesario
```

## Referencia del Módulo Core

Para conocer todas las funciones disponibles (acciones, aserciones, esperas, etc.), consulta la [Referencia del Módulo Core](core_reference.md).

## Consideraciones Importantes

- **Limpieza**: Los archivos en `tests/` deben leerse casi como lenguaje natural. Evita usar `driver` directamente en los tests; usa las funciones de `core.actions`.
- **Locators Únicos**: Mantén los locators centralizados en `pages/` para que, si la UI cambia, solo tengas que actualizar un archivo.
- **Descripciones**: Las funciones de `core.actions` aceptan un parámetro `description`. Úsalo opcionalmente para que los logs sean legibles.
