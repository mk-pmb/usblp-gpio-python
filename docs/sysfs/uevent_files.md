
sysfs uevent files
==================


The basic USB device
--------------------

This chapter is about the device as seen from the general USB driver's view.
For the virtual printer device, see next chapter.


Example syslog message when connecting my usblp:

```text
kernel: [0000.00] usb 2-1.2: new full-speed USB device number 47 using ehci-pci
```

In usblp, that would be

```text
Bus 002 Device 047: ID 067b:2305 Prolific Technology, Inc. PL2305 Parallel Port
```

That `2-1.2` in the syslog is the symlink name in `/sys/bus/usb/devices/`,
thus the path `/sys/bus/usb/devices/2-1.2/uevent` would be one way to point
to the USB device's uevent file.

Example uevent file content:

```text
MAJOR=189
MINOR=174
DEVNAME=bus/usb/002/047
DEVTYPE=usb_device
DRIVER=usb
PRODUCT=67b/2305/200
TYPE=0/0/0
BUSNUM=002
DEVNUM=047
```

* __DEVNAME__ is a subpath of `/dev`. `/dev/bus/usb/002/038` is a character
  device with major/minor numbers 189/165.
  * This is the USB device, not a usblp endpoint! (For that, see below.)
* __MAJOR__ is a number indicating which driver is used for that device.
* __MINOR__ is the device instance number, because one driver might manage
  multiple devices.
* __PRODUCT__ gives the three numbers that `lsusb --verbose` would call
  idVendor/idProduct/bcdDevice, but beware the number formats:
  * idVendor and idProduct are in hex, but probably without leading zeroes,
    so pad them if you need fixed length.
  * bcdDevice ("Device Release Number", probably sth. like the device's
    firmware version) is given in BCD = binary coded decimal, but without
    the decimal separator. `lsusb --verbose` displays it with always
    exactly two digits.



The virtual printer device
--------------------------

… as seen from the `usblp` driver's view.

With the example setup from above, it can be found via its symlink
`/sys/class/usbmisc/lp0` which points to
`…/usb2/2-1/2-1.2/2-1.2:1.0/usbmisc/lp0/`,
which is the same as `/sys/bus/usb/devices/2-1.2/2-1.2:1.0/usbmisc/lp0`.
Thus, knowing the USB device path from above, we could glob for the
subdirectory:

```bash
$ printf '%s\n' /sys/bus/usb/devices/2-1.2/*:*/usbmisc/lp*
/sys/bus/usb/devices/2-1.2/2-1.2:1.0/usbmisc/lp0
```

Or to glob for all usblps:

```bash
$ printf '%s\n' /sys/bus/usb/devices/*/*:*/usbmisc/lp*
/sys/bus/usb/devices/1-1.1.3/1-1.1.3:1.0/usbmisc/lp1
/sys/bus/usb/devices/2-1.2/2-1.2:1.0/usbmisc/lp0
```

Example content of the relevant uevent files:

#### /sys/bus/usb/devices/2-1.2/2-1.2:1.0/uevent

```text
DEVTYPE=usb_interface
DRIVER=usblp
PRODUCT=67b/2305/200
TYPE=0/0/0
INTERFACE=7/1/2
MODALIAS=usb:v067Bp2305d0200dc00dsc00dp00ic07isc01ip02in00
```

#### /sys/bus/usb/devices/2-1.2/2-1.2:1.0/usbmisc/lp0/uevent

```text
MAJOR=180
MINOR=0
DEVNAME=usb/lp0
```

#### /sys/bus/usb/devices/1-1.1/1-1.1:1.0/uevent

```text
DEVTYPE=usb_interface
DRIVER=usblp
PRODUCT=67b/2305/200
TYPE=0/0/0
INTERFACE=7/1/2
MODALIAS=usb:v067Bp2305d0200dc00dsc00dp00ic07isc01ip02in00
```

#### /sys/bus/usb/devices/1-1.1/1-1.1:1.0/usbmisc/lp1/uevent

```text
MAJOR=180
MINOR=1
DEVNAME=usb/lp1
```


Find a virtual printer's USB device
-----------------------------------

The symlinks `/sys/class/usbmisc/lp0/device` point to the related
usblp device:

#### /sys/class/usbmisc/lp0/device/uevent

```text
DEVTYPE=usb_interface
DRIVER=usblp
PRODUCT=67b/2305/200
TYPE=0/0/0
INTERFACE=7/1/2
MODALIAS=usb:v067Bp2305d0200dc00dsc00dp00ic07isc01ip02in00
```

… and since that usblp device directory is a subdirectory of the basic usb
device, we can find the basic device via its parent directory:

#### /sys/class/usbmisc/lp0/device/../uevent

```text
MAJOR=189
MINOR=174
DEVNAME=bus/usb/002/047
DEVTYPE=usb_device
DRIVER=usb
PRODUCT=67b/2305/200
TYPE=0/0/0
BUSNUM=002
DEVNUM=047
```











