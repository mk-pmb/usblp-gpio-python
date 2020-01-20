# -*- coding: UTF-8, tab-width: 4 -*-

def uevent_read_dict(filename):
    """
    filename should be sth. like /sys/class/usbmisc/lp0/device/uevent
    """
    if instanceof(filename, dict):
        # help other functions allow reuse of known info
        info = filename.copy()
    else:
        with open(filename, 'r') as fh:
            info = dict([ln.strip().split('=') for ln in fh.readlines()])

    idvp = info['PRODUCT'].split('/')[0:2]
    idvp = '{:>4s}:{:>4s}'.format(*idvp).replace(' ', '0')
    info['vendor:product'] = vp

    (major, minor) = (info.get('MAJOR'), info.get('MINOR')
    if major and minor:
        info['major:minor'] = major + ':' + minor
    else:
        info['major:minor'] = None

    return info
