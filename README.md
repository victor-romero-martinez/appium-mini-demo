# Appium Mini Demo

Este es un proyecto base para la automatización de pruebas móviles utilizando **Appium**, **Python** y **Pytest**.

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.10+
- Appium Server funcionando
- Emulador de Android o Simulador de iOS configurado

### Instalación

1. Clona el repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura tu archivo `.env` (puedes basarte en `.env.example`).

## 📁 Estructura del Proyecto

```text
├── core/           # Lógica base y acciones del framework
├── pages/          # locators de las pantallas (Page Objects simplificados)
├── tests/          # Casos de prueba
├── docs/           # Documentación adicional
└── conftest.py     # Configuración y fixtures de Pytest
```

## 🛠️ Uso y Mejores Prácticas

Para mantener el código limpio y mantenible, seguimos estas reglas:

1. **locators en `pages/`**: Cada pantalla debe tener su archivo de locators. **No agregues lógica aquí.**
2. **Tests en `tests/`**: Los tests deben ser declarativos y utilizar las acciones de `core/`.
3. **Acciones en `core/`**: Si necesitas una interacción nueva, agrégala en `core/actions.py`.

Para más detalles, consulta la [Guía de Uso](docs/usage.md) y la [Referencia del Módulo Core](docs/core_reference.md).

## 🧪 Ejecutar Pruebas

Puedes usar el `Makefile` para ejecutar las pruebas fácilmente:

```bash
make ios # para correr en iOS o make android para Android
```

O directamente con pytest:

```bash
DEVICE_NAME="NOMBRE DEL DISPOSITIVO ANDROID" PLATFORM_VERSION="ANDROID VERSION" pytest tests/
```
