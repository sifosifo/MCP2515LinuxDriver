#!/usr/bin/python

from can import can

class Foo:
	def __init__(self):
			self.can = can()
			self.can.Send(0x10, [0x01, 0x02, 0x03])
			print self.can.Receive()

foo = Foo()

