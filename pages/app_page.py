# App para hacer pruebas
# https://play.google.com/store/apps/details?id=com.expandtesting.practice


from appium.webdriver.common.appiumby import AppiumBy

COMPANY_NAME_LABEL = (AppiumBy.ACCESSIBILITY_ID, "company-name")

ANIMATION_DEMO_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "go-to-animation-screen")
SLIDE_MESSAGE_BUTTON = (AppiumBy.ID, "com.expandtesting.practice:id/btnSlideMessage")
SLIDE_MESSAGE = (AppiumBy.ID, "com.expandtesting.practice:id/tvMessage")

COUNTRIES_LIST_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "go-to-countries-list-screen")
PARAGUAY_LABEL_BY_XPATH = (
    AppiumBy.XPATH,
    '//android.widget.TextView[@resource-id="com.expandtesting.practice:id/tv_country_name" and @text="Paraguay"]',
)

GESTURE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "go-to-gesture-screen")
SWIPE_BOX_CONTAINER = (AppiumBy.ID, "com.expandtesting.practice:id/tvSwipeMe")

MULTITOUCH_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "go-to-multi_touch-screen")
TOUCH_BOX_CONTAINER = (AppiumBy.ID, "com.expandtesting.practice:id/touchView")
