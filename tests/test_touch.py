from pages.animation_page import *
from core.actions import *
from core.assertions import *
from time import sleep


def test_touch_at():
    tap_on(MULTITOUCH_BUTTON)
    assert_visible(TOUCH_BOX_CONTAINER)
    tap_at(250, 800)
    sleep(2)
    tap_at(320, 1200)
    back()
