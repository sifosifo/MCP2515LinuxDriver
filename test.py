#!/usr/bin/python

from can import can
import time

class Foo:
	def __init__(self):
		self.can = can()
		while True:
			message = []
			self.can.Send(0x100, [0x01])
			message.append(self.can.Receive())
			message.append(self.can.Receive())
			time.sleep(0.5)
			self.can.Send(0x104, [0x03])
			message.append(self.can.Receive())
			message.append(self.can.Receive())
			time.sleep(0.5)
			self.can.Send(0x106, [0x04])
			message.append(self.can.Receive())
			message.append(self.can.Receive())
			time.sleep(0.5)
			self.can.Send(0x108, [0x05])
			message.append(self.can.Receive())
			message.append(self.can.Receive())
			for mes in message:
				if mes != 0:
					if mes[0] == 0x105:	# Primary
						print "Primary"
						print "TempInlet=%.1fC\tTempOutlet=%.1fC\tFlow=%ddcl/min\tPower=%dW" % self.GetData(mes)
					elif mes[0] == 0x107:	# Secondary
						print "Secondary"
						print "TempInlet=%.1fC\tTempOutlet=%.1fC\tFlow=%ddcl/min\tPower=%dW" % self.GetData(mes)
					elif mes[0] == 0x109:	# Tank
						print "TankUp=%.1fC\tTankDown=%.1fC" % \
							((((mes[2]<<8)+mes[1])/16.0), ((mes[4]<<8)+mes[3])/16.0)
					else:
						print mes
	def GetData(self, mes):
		Temp1 = ((mes[2]<<8) + mes[1])/16.0
		Temp2 = ((mes[4]<<8) + mes[3])/16.0
		Flow = mes[5]
		Power = (mes[8]<<8) + mes[7]
		return(Temp1, Temp2, Flow, Power)

foo = Foo()

