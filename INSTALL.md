
Installation
============

pyusb
-----

If you get an error `ImportError: No module named 'usb'`,
1.  `git clone https://github.com/walac/pyusb`
1.  Inside that repo, `sudo --preserve-env ./setup.py install`
    * The `--preserve-env` is meant for stuff like proxies and/or
      `PYTHONDONTWRITEBYTECODE=1`.
```

* As of 2019-12-03 it seems like it only supports python 2.7.x. :-(

