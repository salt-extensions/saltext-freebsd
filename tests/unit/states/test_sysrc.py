"""
:codeauthor: Rahul Handay <rahulha@saltstack.com>
"""

import pytest

from saltext.freebsd.states import sysrc
from tests.support.mock import MagicMock
from tests.support.mock import patch


@pytest.fixture
def configure_loader_modules():
    return {sysrc: {}}


def test_managed():
    """
    Test to ensure a sysrc variable is set to a specific value.
    """
    ret = {"name": "salt", "changes": {}, "result": True, "comment": ""}
    mock = MagicMock(side_effect=[{"key1": {"salt": "stack"}}, None, None])
    mock1 = MagicMock(return_value=True)
    with patch.dict(sysrc.__salt__, {"sysrc.get": mock, "sysrc.set": mock1}):
        ret.update({"comment": "salt is already set to the desired value."})
        assert sysrc.managed("salt", "stack") == ret

        with patch.dict(sysrc.__opts__, {"test": True}):
            ret.update(
                {
                    "changes": {"new": "salt = stack will be set.", "old": None},
                    "comment": 'The value of "salt" will be changed!',
                    "result": None,
                }
            )
            assert sysrc.managed("salt", "stack") == ret

        with patch.dict(sysrc.__opts__, {"test": False}):
            ret.update(
                {
                    "changes": {"new": True, "old": None},
                    "comment": 'The value of "salt" was changed!',
                    "result": True,
                }
            )
            assert sysrc.managed("salt", "stack") == ret


@pytest.mark.parametrize("value,expected", [(True, "YES"), (False, "NO"), (2222, "2222")])
def test_managed_test_mode_non_string_value(value, expected):
    """
    In test mode a non-string value (YAML turns an unquoted YES into True)
    must not raise TypeError, and the preview must show the value that
    sysrc.set would actually write.
    """
    mock_get = MagicMock(return_value=None)
    with patch.dict(sysrc.__salt__, {"sysrc.get": mock_get}):
        with patch.dict(sysrc.__opts__, {"test": True}):
            ret = sysrc.managed("vm_enable", value)
    assert ret == {
        "name": "vm_enable",
        "changes": {"old": None, "new": f"vm_enable = {expected} will be set."},
        "result": None,
        "comment": 'The value of "vm_enable" will be changed!',
    }


@pytest.mark.parametrize("value,current", [(True, "YES"), (False, "NO"), (2222, "2222")])
def test_managed_non_string_value_already_set(value, current):
    """
    A non-string value that matches the current setting once normalized
    (True == "YES", 2222 == "2222") is already in the desired state: no
    change is reported and sysrc.set is not called.
    """
    mock_get = MagicMock(return_value={"/etc/rc.conf": {"vm_enable": current}})
    mock_set = MagicMock()
    with patch.dict(sysrc.__salt__, {"sysrc.get": mock_get, "sysrc.set": mock_set}):
        with patch.dict(sysrc.__opts__, {"test": False}):
            ret = sysrc.managed("vm_enable", value)
    assert ret == {
        "name": "vm_enable",
        "changes": {},
        "result": True,
        "comment": "vm_enable is already set to the desired value.",
    }
    mock_set.assert_not_called()


@pytest.mark.parametrize(
    "value,current,expected", [(True, "NO", "YES"), (False, "YES", "NO"), (2222, "22", "2222")]
)
def test_managed_non_string_value_differs_from_current(value, current, expected):
    """
    Inverse of the already-set case: a normalized value must not match a
    different current value. The change is made, and sysrc.set gets the
    normalized string.
    """
    mock_get = MagicMock(return_value={"/etc/rc.conf": {"vm_enable": current}})
    mock_set = MagicMock(return_value={"/etc/rc.conf": {"vm_enable": expected}})
    with patch.dict(sysrc.__salt__, {"sysrc.get": mock_get, "sysrc.set": mock_set}):
        with patch.dict(sysrc.__opts__, {"test": False}):
            ret = sysrc.managed("vm_enable", value)
    assert ret["result"] is True
    assert ret["changes"] == {
        "old": {"/etc/rc.conf": {"vm_enable": current}},
        "new": {"/etc/rc.conf": {"vm_enable": expected}},
    }
    mock_set.assert_called_once_with(name="vm_enable", value=expected)


@pytest.mark.parametrize("test_mode", [True, False])
@pytest.mark.parametrize("value", [1.5, None])
def test_managed_rejects_other_non_string_values(value, test_mode):
    """
    Values that sysrc.set cannot write (YAML loads an unquoted 1.5 as a float
    and an empty value as None) are rejected with a clear message in both
    modes, instead of test mode reporting a change that the real run would
    then fail to make.
    """
    mock_get = MagicMock()
    mock_set = MagicMock()
    with patch.dict(sysrc.__salt__, {"sysrc.get": mock_get, "sysrc.set": mock_set}):
        with patch.dict(sysrc.__opts__, {"test": test_mode}):
            ret = sysrc.managed("vm_enable", value)
    assert ret == {
        "name": "vm_enable",
        "changes": {},
        "result": False,
        "comment": (
            'Invalid value for "vm_enable": expected a string, got '
            f"{type(value).__name__}. Quote the value in YAML."
        ),
    }
    mock_get.assert_not_called()
    mock_set.assert_not_called()


def test_absent():
    """
    Test to ensure a sysrc variable is absent.
    """
    ret = {"name": "salt", "changes": {}, "result": True, "comment": ""}
    mock = MagicMock(side_effect=[None, True, True])
    mock1 = MagicMock(return_value=True)
    with patch.dict(sysrc.__salt__, {"sysrc.get": mock, "sysrc.remove": mock1}):
        ret.update({"comment": '"salt" is already absent.'})
        assert sysrc.absent("salt") == ret

        with patch.dict(sysrc.__opts__, {"test": True}):
            ret.update(
                {
                    "changes": {"new": '"salt" will be removed.', "old": True},
                    "comment": '"salt" will be removed!',
                    "result": None,
                }
            )
            assert sysrc.absent("salt") == ret

        with patch.dict(sysrc.__opts__, {"test": False}):
            ret.update(
                {
                    "changes": {"new": True, "old": True},
                    "comment": '"salt" was removed!',
                    "result": True,
                }
            )
            assert sysrc.absent("salt") == ret
