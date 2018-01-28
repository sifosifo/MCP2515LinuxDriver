#!/usr/bin/python

from mcp2515 import mcp2515

class can:
	def __init__(self):
		self.mcp2515 = mcp2515()
		self.mcp2515.WriteRegister(mcp2515.CNF3, [0x07, 0x9A, 0x01])
		print self.mcp2515.ReadRegister(mcp2515.CNF3, 3)
		self.mcp2515.WriteRegister(TXRTSCTRL, [0])
		self.mcp2515.WriteRegister(BFPCTRL, (1<<B0BFE)|(1<<B1BFE)|(1<<B0BFM)|(1<<B1BFM))
		self.mcp2515.WriteRegister(CANCTRL, [CLKOUT_PRESCALER])
		SetMode(LOOPBACK_MODE)

	def SetMode(self, Mode):
		if Mode == LISTEN_ONLY_MODE:
			reg = (1<<REQOP1)|(1<<REQOP0)
		if Mode == LOOPBACK_MODE:
			reg = (1<<REQOP1)
		if Mode == SLEEP_MODE:
			req = REQOP0
		self.mcp2515.BitModify(CANCTRL, (1<<REQOP2)|(1<<REQOP1)|(1<<REQOP0), reg)
		ready = 0x1FF
		while (ready & 0xe0) != reg:
			ready = self.mcp2515.ReadRegister(1)


	def Send(self, ID, Data):
		tmp = ID
		self.mcp2515.WriteRegiteri(tmp)

	def Receive(self):
		return(0)



