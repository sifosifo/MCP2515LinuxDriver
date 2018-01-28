#!/usr/bin/python

from can import can

class Foo():
	self.can_fd = can.can()
	self.can_fd.Send()
	print self.can_fd.Receive()

foo = Foo()

