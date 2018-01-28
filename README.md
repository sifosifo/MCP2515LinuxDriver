# MCP2515LinuxDriver
Userspace Linux driver for MCP2515 chip based CAN boards

If you want to add CAN interface using MCP2515 chip based boarid to your linux board (e.g. Raspberry Pi, Orange Pi or any similar board), but you use Linux distribution that lacks mcp251x driver, this might be for you.

Why might and not is?
Well if it is possible for you to switch to Distribution that includes this driver, that would be best thing to to.
If you're stuck with your distribution for whatever reason, next est thing would be compile existing kernel driver for your kernel and use it.
But if you are not kernel driver guru like me, next best thing is to use user space driver and that is exactly what you find in this repository.

What you gain:
- You don't need super deep understanding of linux kernel to make this user driver work, you need just working SPI interface and Python installed


What you loose:
- This is not fully featured driver, you don't get can interface in /dev and therefore stadard CAN tools available in linux cannot be used

Bottomline:
- If you don't have skill or time to make proper kernel driver work on your linux distribution and it is sufficient use basic functionality this driver provide using your own Python script, this is good solution for you.

CURRENT STATE:
- In development - very basic transmission and reception works in loop mode
- Needs to rework a bit - create message structure
- Working driver is expected by beginning of february 2018


