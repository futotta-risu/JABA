import pytest

from gui.component.label.CoolCenterTitleLabel import CoolCenterTitleLabel


def test_coolcentertitlelabel_constructor(qtbot):
    # Given

    # When
    try:
        CoolCenterTitleLabel("Title")
        # Then
    except Exception:
        pytest.fail("Could not create CoolCenterTitleLable")
