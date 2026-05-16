import os
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


def create_driver() -> WebDriver:
    """
    Crea e inicializa la instancia del driver de Appium basado en las variables de entorno.
    Lee PLATFORM_NAME para decidir si configurar Android o iOS.

    Variables clave: PLATFORM_NAME, PLATFORM_VERSION, DEVICE_NAME, APPIUM_URL.
    """
    platform = os.getenv("PLATFORM_NAME", "android").lower()

    if platform == "android":
        options = UiAutomator2Options()

        options.platform_name = "Android"
        options.platform_version = os.getenv("PLATFORM_VERSION")
        options.device_name = os.getenv("DEVICE_NAME")
        options.app_package = os.getenv("APP_PACKAGE")
        options.app_activity = os.getenv("APP_ACTIVITY")
        options.auto_grant_permissions = True

    elif platform == "ios":
        options = XCUITestOptions()

        aux_prebuilt_wda_val = os.getenv("USE_PREBUILT_WDA", "false").lower()
        options.use_prebuilt_wda = aux_prebuilt_wda_val == "true"

        options.platform_name = "iOS"
        options.xcode_signing_id = "Apple Development"
        options.device_name = os.getenv("DEVICE_NAME")
        options.platform_version = os.getenv("PLATFORM_VERSION")
        options.udid = os.getenv("UDID")
        options.bundle_id = os.getenv("IOS_BUNDLE_ID", os.getenv("APP_PACKAGE"))
        options.xcode_org_id = os.getenv("XCODE_ORG_ID")
        options.updated_wda_bundle_id = os.getenv("IOS_WDA_BUNDLE_ID")
        options.auto_accept_alerts = True
        options.auto_grant_permissions = True

    else:
        raise Exception(f"Unsupported platform: {platform}")

    driver = webdriver.Remote(command_executor=os.getenv("APPIUM_URL"), options=options)

    return driver
