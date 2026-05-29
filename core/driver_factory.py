import os
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


def create_driver(device_config: dict = None) -> WebDriver:
    """
    Crea e inicializa la instancia del driver de Appium basado en las variables de entorno
    y en la configuración específica del dispositivo asignado al worker actual.

    Args:
        device_config: Diccionario con la configuración del dispositivo del pool (devices.json).
                       Puede incluir: deviceName, udid, platformVersion, systemPort (Android),
                       wdaLocalPort (iOS). Si es None, se usan solo las variables de entorno.

    Variables clave: PLATFORM_NAME, PLATFORM_VERSION, DEVICE_NAME, APPIUM_URL.
    """
    platform = os.getenv("PLATFORM_NAME", "android").lower()
    if device_config is None:
        device_config = {}

    if platform == "android":
        options = UiAutomator2Options()

        options.platform_name = "Android"
        options.platform_version = (
            device_config.get("platformVersion") or os.getenv("PLATFORM_VERSION")
        )
        options.device_name = (
            device_config.get("deviceName") or os.getenv("DEVICE_NAME", "Android Emulator")
        )
        options.udid = device_config.get("udid") or os.getenv("UDID")
        options.app_package = os.getenv("APP_PACKAGE")
        options.app_activity = os.getenv("APP_ACTIVITY")
        options.auto_grant_permissions = True

        # Puerto de comunicación del driver UiAutomator2.
        # Cada worker paralelo DEBE tener un puerto exclusivo para evitar colisiones.
        system_port = device_config.get("systemPort")
        if system_port:
            options.system_port = int(system_port)

    elif platform == "ios":
        options = XCUITestOptions()

        aux_prebuilt_wda_val = os.getenv("USE_PREBUILT_WDA", "false").lower()
        options.use_prebuilt_wda = aux_prebuilt_wda_val == "true"

        options.platform_name = "iOS"
        options.xcode_signing_id = "Apple Development"
        options.device_name = (
            device_config.get("deviceName") or os.getenv("DEVICE_NAME")
        )
        options.platform_version = (
            device_config.get("platformVersion") or os.getenv("PLATFORM_VERSION")
        )
        options.udid = device_config.get("udid") or os.getenv("UDID")
        options.bundle_id = os.getenv("IOS_BUNDLE_ID", os.getenv("APP_PACKAGE"))
        options.xcode_org_id = os.getenv("XCODE_ORG_ID")
        options.updated_wda_bundle_id = os.getenv("IOS_WDA_BUNDLE_ID")
        options.auto_accept_alerts = True
        options.auto_grant_permissions = True

        # Puerto local del WebDriverAgent.
        # Cada worker paralelo DEBE tener un puerto exclusivo para evitar colisiones.
        wda_local_port = device_config.get("wdaLocalPort")
        if wda_local_port:
            options.wda_local_port = int(wda_local_port)

    else:
        raise Exception(f"Unsupported platform: {platform}")

    driver = webdriver.Remote(command_executor=os.getenv("APPIUM_URL"), options=options)

    return driver
