#!/usr/bin/python2.7
# -*- coding: UTF-8, tab-width: 4 -*-

import sys
import idvp_autohex
import sysfs_usb


repl_input_stack = sys.argv[1:]
if len(repl_input_stack) < 1:
    repl_input_stack += ['interactive']

ans_var_slot = '_'
repl_vars = {
    'lp': 0,
    }

def is_interactive():
    return bool(repl_vars.get('interactive'))


def repl_read():
    if len(repl_input_stack) > 0:
        return repl_input_stack.pop(0)
    if is_interactive():
        return sys.stdin.readline().rstrip()


def repl_main():
    while True:
        cmd = repl_read().strip()
        if cmd in ('Q', 'quit', 'exit', None):
            return
        ret = repl_cmd(cmd)()
        if  is_interactive() and (ret is not None):
            print repr(ret)
            repl_vars[ans_var_slot] = ret


def repl_cmd(cmd):
    if cmd.startswith('#'):
        return

    if ' ' in cmd:
        cmd = cmd.split(' ')
        repl_input_stack = cmd[1:] + repl_input_stack
        cmd = cmd[0]

    func = globals().get('cmd_' + cmd)
    if func is not None:
        return func
    raise NotImplementedError('No such repl command', cmd)


def cmd_execfile():
    filename = repl_read()
    with open(filename, 'r') as fh:
        lines = [ln.strip() for ln in fh.readlines()]
    repl_input_stack = lines + repl_input_stack


def cmd_interactive():
    repl_vars['interactive'] = True


def cmd_lp():
    repl_vars['lp'] = int(repl_read(), 10)


def cmd_echo():
    tpl = repl_read()
    print tpl.format(**repl_vars)


def cmd_var():
    type = repl_read()
    if type == 'list':
        print repr(repl_vars)
        return

    key = repl_read()
    if type == 'show':
        print repr(repl_vars.get(key))
        return
    elif type in ('^', 'ans',):
        val = repl_vars.get(ans_var_slot)
    elif type in ('$', 'var',):
        val = repl_vars.get(repl_read())
    elif type in ('N', 'none',):
        val = None
    elif type in ('T', 'true',):
        val = True
    elif type in ('F', 'false',):
        val = False
    elif type in ('s', 'str',):
        val = unicode(repl_read())
    elif type in ('i', 'int',):
        val = int(repl_read(), 10)
    elif type in ('h', 'hex',):
        val = int(repl_read(), 16)
    elif type in ('%', 'cmd',):
        val = repl_cmd(repl_read())
    else:
        raise TypeError('Unsupported repl var type', type)
    cli_vars[key] = val


def cmd_find_usbdev():
    v = repl_read()
    if v == 'lp':
        v = '/sys/class/usbmisc/lp{0}/device/uevent'.format(repl_vars['lp'])
    if v.startswith('/uevent'):
        # see docs/sysfs/uevent.md
        v = sysfs_usb.uevent_read_dict(v)
    p = v.split(':')
    if len(p) == 2:
        (v, p) = p
    else:
        p = repl_read()
    (v, p) = [int(x, 16) for x in (v, p,)]
    dev = idvp_autohex.find_device(idVendor=v, idProduct=p)
    repl_vars['usbdev'] = dev
    return dev


def cmd_reset_usbdev():
    repl_vars['usbdev'].reset()













if __name__ == '__main__':
    repl_main()
