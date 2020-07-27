#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-

import usb.core

# /sys/class/usbmisc/$LPDEV/device

lp = usb.core.find(idVendor=0x067b, idProduct=0x2305)
# lp.reset()
print 'Bus', lp.bus, 'Device', lp.address

ifaces = lp.get_active_configuration().interfaces()
for iface in ifaces:
    print 'interface', iface
    for endpt in iface.endpoints():
        print 'endpoint', endpt
