from pages.app_page import *
from core.actions import *
from core.assertions import *


def test_swipe_with_count_left():
    tap_on(GESTURE_BUTTON)
    swipe("left", 2, container_locator=SWIPE_BOX_CONTAINER)


def test_swipe_with_count_right():
    tap_on(GESTURE_BUTTON)
    swipe("right", 3, container_locator=SWIPE_BOX_CONTAINER)
