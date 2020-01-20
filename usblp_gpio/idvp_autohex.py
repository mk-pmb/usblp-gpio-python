# -*- coding: UTF-8, tab-width: 4 -*-

import usb.core as _usb_core


def parse(spec):
    if isinstance(spec, str):
        if spec.startswith('0x'):
            spec = spec[2:]
        return int(spec, 16)

    return spec


def autohexify(origfunc):
    def idvp_autohexed(*args, **kwargs):
        for key in ('idVendor', 'idProduct',):
            val = kwargs.get(key)
            if val is not None:
                kwargs[key] = parse(val)
        return origfunc(*args, **kwargs)

    return idvp_autohexed


find_device = autohexify(_usb_core.find)
