from pages.app_page import *
from core.actions import *
from core.assertions import *
from core.waits import wait_for_animation_end


def test_scroll_by_xpath_to_country_py():
    tap_on(COUNTRIES_LIST_BUTTON)
    wait_for_animation_end()
    scroll_until_visibility(PARAGUAY_LABEL_BY_XPATH)
    assert_visible(PARAGUAY_LABEL_BY_XPATH)
