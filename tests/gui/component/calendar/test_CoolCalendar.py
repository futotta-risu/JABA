import pytest

from PyQt5.QtCore import QDate

from gui.component.calendar.CoolCalendar import CoolCalendar


def test_coolcalendar_constructor(qtbot):
    # Given
    # When
    try:
        CoolCalendar()
        # Then
    except Exception:
        pytest.fail("Could not create CoolCalendar")

def test_coolcalendar_set_color(qtbot):
    calendar = CoolCalendar()
    calendar.set_color('18BEBC')
    
    assert calendar.color == QtGui.QColor('18BEBC')

def test_coolcalendar_reset_dates(qtbot):
    # Given
    calendar = CoolCalendar()
    try:
        # When
        calendar.reset_dates([QDate(2010, 35, 7), QDate(2010, 5, 7)])
        
        # Then
    except Exception:
        pytest.fail("Could not create CoolCalendar")
