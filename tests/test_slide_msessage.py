from core.actions import *
from core.assertions import *
from core.waits import wait_for_animation_end, wait_invisible
from pages.animation_page import *


def test_animation_slide():
    tap_on(ANIMATION_DEMO_BUTTON)
    tap_on(SLIDE_MESSAGE_BUTTON)
    assert_visible(SLIDE_MESSAGE)
    wait_invisible(SLIDE_MESSAGE)
    back()
