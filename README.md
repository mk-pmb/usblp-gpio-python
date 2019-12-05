
<!--#echo json="package.json" key="name" underline="=" -->
usblp-gpio-python
=================
<!--/#echo -->

<!--#echo json="package.json" key="description" -->
My attempt at GPIO (general purpose input/output) via usblp.
<!--/#echo -->


Comparison of Strategies
------------------------

If you aim for cost efficiency and your time is worth any money,
ditch usblp and get a [NodeMCU](http://www.nodemcu.com/) instead.
When I checked, prices were comparable to a usblp, but you get proper control,
custom logic, and wifi.

Still reading? Wondering what you can do with usblp while you wait for your
shipment of NodeMCUs? You could…

* Try and make your [usblp work in SPP mode][hackaday-spp].
  However, my Prolific PL2305 refused,
  and also it lied about the supported modes.
* Make [a circuit][thx8411-ttl] that properly does the busy/ack handshake.
* If you have a second usblp, they can ack each other.

* Connect busy and ack to something that blinks or flickers randomly.
  * Stuff you could use:
    * An actual timer circuit?
    * A blinky toy?
    * Some audio source?
    * A spare audio amplifier? If you use a cheap one, if will even provide
      its own noise!
    * A piece of lightweight metal on a spinning computer chassis fan?
    * Maybe the USB data lines?
      * Do beware it might have bad side effects if your usblp is built in
        an unlucky way.
  * Having signals on ack/busy during printer mode negotioation phase
    might result in more complex protocols being decided.
    * Thus, you might want to use something that only blinks while a strobe
      is fired, or a bit later. If you have a spare transistor or sth.,
      you might be able to logically "AND" your blinkentoy with the strobe.
    * With my Prolific PL2305, it seemed to have caused all data bits to be
      set to GND in the gaps between host data transmissions.

* Or wire it such that your usblp will always be busy, and soft-reset it
  before each byte you send.
  You'll get the usual USB device (dis)connection messages in syslog,
  and the data bits may be dark or weird while it reconnects.
  However, if you only rarely need to set a bit (e.g. flip a latching relay),
  this might be the easiest approach.







Known issues
------------

* Needs more/better tests and docs.




&nbsp;

  [thx8411-ttl]: http://thx8411.over-blog.com/pages/Add_TTL_outputs_to_your_USB_Laptop_Part_1_Hardware-3229030.html
  [hackaday-spp]: https://hackaday.io/project/10512-potentially-usefulobscure-linux-stuff/log/43345-usb-parallel-port-adapter-low-level-coding-usblpc



License
-------
<!--#echo json="package.json" key=".license" -->
ISC
<!--/#echo -->
