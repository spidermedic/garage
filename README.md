## Garage Door System
This is a simple system running on a Raspberry Pi using Flask, that allows the
user to operate and view the status of their gargage door(s). The program is
currently set up for two doors, but the code can be easily adapted to as many or
as few as are required. 

## Requirements
### Raspberry Pi:
I have been running this on a Pi Zero W without any issues


### Relay Board:
The relay get its input from the Raspberry Pi GPIO pins and the output is
connected to the physical door switch. Make sure you have connected the switch
side to the 'normally open' outputs of the relay.

This is the relay setup that I used, but any should work fine.

(Not an affiliate link)

https://amazon.com/gp/product/B00E0NTPP4/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1


### Magnetic Switches
The magnet is attached to the garage door and the switch needs to be in a fixed
position so that the two line up when the door is closed. The wires get
connected to the 'NO' or 'normally open' terminals.

Again any similar product should work as well.

(Not an affiliate link)

https://amazon.com/gp/product/B076J5TQ7V/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1


### Other Stuff
You will also need wiring and some resistors to connect the relays and switches
back to the RPi.
Schematics will be posted in the near future.