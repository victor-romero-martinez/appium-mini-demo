# Referencia del Módulo Core

El directorio `core/` contiene las herramientas fundamentales para interactuar con la aplicación y realizar verificaciones.

---

## 🛠️ Acciones (`core.actions`)
Módulo principal para la interacción con elementos de la interfaz.

| Función | Descripción | Argumentos Principales |
| :--- | :--- | :--- |
| `tap_on` | Realiza un clic en un elemento. | `locator`, `description` |
| `tap_at` | Realiza un clic en coordenadas (x, y). | `x`, `y`, `description` |
| `input_text` | Escribe texto en un campo y oculta el teclado. | `locator`, `text`, `description` |
| `get_text` | Obtiene el texto de un elemento. | `locator`, `description` |
| `take_screenshot` | Guarda una captura de pantalla. | `filename`, `path`, `description` |
| `scroll_until_visibliity` | Hace scroll hasta que el elemento sea visible. | `locator`, `description` |
| `swipe` | Desliza en una dirección (`up`, `down`, `left`, `right`). | `direction`, `count`, `locator`, `container_locator` |
| `back` | Navega hacia atrás en la aplicación. | `description` |

---

## ✅ Aserciones (`core.assertions`)
Funciones para validar el estado de la aplicación.

| Función | Descripción |
| :--- | :--- |
| `assert_visible` | Verifica que el elemento esté presente y visible. |
| `assert_enabled` | Verifica que el elemento esté habilitado para interacción. |
| `assert_disabled` | Verifica que el elemento esté deshabilitado. |

---

## ⏳ Esperas (`core.waits`)
Manejo de tiempos y sincronización.

| Función | Descripción |
| :--- | :--- |
| `wait_visible` | Espera hasta que un elemento sea visible (timeout por defecto: 10s). |
| `wait_for_animation_end` | Espera a que las animaciones de un elemento o de la app terminen. |

---

## 🔄 Flujos y Utilidades (`core.flows`, `core.context`)

### `run_flow`
Permite ejecutar un bloque de código basado en una condición. Ideal para pasos específicos de una plataforma.
```python
run_flow(context.platform == 'android', mi_funcion_android, arg1="valor")
```

### `context`
Objeto global que mantiene el estado de la ejecución.
- `context.driver`: Instancia activa de Appium.
- `context.platform`: Plataforma actual (`android` o `ios`).
