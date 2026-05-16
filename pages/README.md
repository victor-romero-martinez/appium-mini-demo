# Directorio de Pages

En este directorio se deben incluir exclusivamente los **locators** de cada pantalla.

## Reglas
- **Solo locators**: No agregar funciones de clic, scroll o lógica de negocio.
- **Tuplas**: Definir cada locador como una tupla `(By, "valor")`.

## Ejemplo
```python
from appium.webdriver.common.appiumby import AppiumBy

START_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "start_btn")
```
