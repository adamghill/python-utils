import pytest
from django.utils.timezone import now

from unicorn.components.strftime import StrftimeView


@pytest.fixture
def component():
    component = StrftimeView(component_name="strftime", component_id="asdf")
    component.datetime = now()
    return component


@pytest.mark.freeze_time("2021-02-08 8:07:01")
def test_format_datetime(component):
    component.format = "%c"

    expected = "<span class='has-tooltip-arrow has-tooltip-multiline' style='background-color: #FFDF00' data-tooltip='%c: Locale’s appropriate date and time representation.'>Mon Feb  8 08:07:01 2021</span>"
    component.format_datetime()
    actual = component.result

    assert expected == actual


@pytest.mark.freeze_time("2021-02-08 8:07:01")
def test_format_datetime_with_extra_text(component):
    component.format = "%ctest"

    expected = "<span class='has-tooltip-arrow has-tooltip-multiline' style='background-color: #FFDF00' data-tooltip='%c: Locale’s appropriate date and time representation.'>Mon Feb  8 08:07:01 2021</span>test"
    component.format_datetime()
    actual = component.result

    assert expected == actual


@pytest.mark.freeze_time("2021-02-08 8:07:01")
def test_format_datetime_with_extra_percentage(component):
    component.format = "%ctest%oc"

    expected = "<span class='has-tooltip-arrow has-tooltip-multiline' style='background-color: #FFDF00' data-tooltip='%c: Locale’s appropriate date and time representation.'>Mon Feb  8 08:07:01 2021</span>test%oc"
    component.format_datetime()
    actual = component.result

    assert expected == actual
