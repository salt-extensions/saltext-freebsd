"""
State to work with sysrc

"""

# define the module's virtual name
__virtualname__ = "sysrc"


def __virtual__():
    """
    Only load if sysrc executable exists
    """
    if __salt__["cmd.has_exec"]("sysrc"):
        return True
    return (False, "Command not found: sysrc")


def managed(name, value, **kwargs):
    """
    Ensure a sysrc variable is set to a specific value.

    name
        The variable name to set
    value
        Value to set the variable to. Quote it in YAML. An unquoted ``YES`` or
        ``NO`` (also ``true``, ``false``, ``on`` and ``off``) is loaded as a
        boolean and written as ``YES`` or ``NO``, and an unquoted integer is
        written as its decimal value, so ``0755`` becomes ``755``. Other
        unquoted values, such as ``1.5`` or an empty value, are rejected.
    file
        (optional) The rc file to add the variable to.
    jail
        (option) the name or JID of the jail to set the value in.

    Example:

    .. code-block:: yaml

        syslogd:
          sysrc.managed:
            - name: syslogd_flags
            - value: -ss

        sshd:
          sysrc.managed:
            - name: sshd_enable
            - value: "YES"
    """

    ret = {"name": name, "changes": {}, "result": False, "comment": ""}

    # YAML turns unquoted YES/NO/True/False into booleans and bare numbers into
    # ints, but sysrc values are strings. Normalize them the same way sysrc.set
    # does, so the comparison with the current value and the test-mode preview
    # both use what will actually be written.
    if isinstance(value, bool):
        value = "YES" if value else "NO"
    elif isinstance(value, int):
        value = str(value)
    if not isinstance(value, str):
        ret["comment"] = (
            f'Invalid value for "{name}": expected a string, got '
            f"{type(value).__name__}. Quote the value in YAML."
        )
        return ret

    # Check the current state
    current_state = __salt__["sysrc.get"](name=name, **kwargs)
    if current_state is not None:
        for rcdict in current_state.values():
            if rcdict[name] == value:
                ret["result"] = True
                ret["comment"] = f"{name} is already set to the desired value."
                return ret

    if __opts__["test"] is True:
        ret["comment"] = f'The value of "{name}" will be changed!'
        ret["changes"] = {
            "old": current_state,
            "new": f"{name} = {value} will be set.",
        }

        # When test=true return none
        ret["result"] = None

        return ret

    new_state = __salt__["sysrc.set"](name=name, value=value, **kwargs)

    ret["comment"] = f'The value of "{name}" was changed!'

    ret["changes"] = {"old": current_state, "new": new_state}

    ret["result"] = True

    return ret


def absent(name, **kwargs):
    """
    Ensure a sysrc variable is absent.

    name
        The variable name to set
    file
        (optional) The rc file to add the variable to.
    jail
        (option) the name or JID of the jail to set the value in.
    """

    ret = {"name": name, "changes": {}, "result": False, "comment": ""}

    # Check the current state
    current_state = __salt__["sysrc.get"](name=name, **kwargs)
    if current_state is None:
        ret["result"] = True
        ret["comment"] = f'"{name}" is already absent.'
        return ret

    if __opts__["test"] is True:
        ret["comment"] = f'"{name}" will be removed!'
        ret["changes"] = {
            "old": current_state,
            "new": f'"{name}" will be removed.',
        }

        # When test=true return none
        ret["result"] = None

        return ret

    new_state = __salt__["sysrc.remove"](name=name, **kwargs)

    ret["comment"] = f'"{name}" was removed!'

    ret["changes"] = {"old": current_state, "new": new_state}

    ret["result"] = True

    return ret
