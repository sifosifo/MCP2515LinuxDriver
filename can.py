#!/usr/bin/python

from mcp2515 import mcp2515
import time

class can:
	def __init__(self):
		self.mcp2515 = mcp2515()
		# On board with 8MHz oscilator, this initializes 125kBaud/s CAN speed 
		#self.mcp2515.WriteRegister(mcp2515.CNF3, [0x07, 0x9A, 0x01])
		self.mcp2515.WriteRegister(mcp2515.CNF3, [0x07, 0x9A, 0x00])
		print self.mcp2515.ReadRegister(mcp2515.CNF3, 3)
		
		self.mcp2515.WriteRegister(mcp2515.TXRTSCTRL, [0])
		
		self.mcp2515.WriteRegister(mcp2515.BFPCTRL, \
			[(1<<mcp2515.B0BFE)|(1<<mcp2515.B1BFE)| \
			(1<<mcp2515.B0BFM)|(1<<mcp2515.B1BFM)])
		# No prescaler	
		self.mcp2515.WriteRegister(mcp2515.CANCTRL, [0])
		#self.SetMode(mcp2515.OPMODE_LOOPBACK)
		self.SetMode(mcp2515.OPMODE_NORMAL)

	def SetMode(self, Mode):
		print "Changinig mode to: ",
		if Mode == mcp2515.OPMODE_LISTEN:
			print "Listen"
			reg = mcp2515.REQOP_LISTEN
		elif Mode == mcp2515.OPMODE_LOOPBACK:
			print "loopback"
			reg = mcp2515.REQOP_LOOPBACK
		elif Mode == mcp2515.OPMODE_SLEEP:
			print "Sleep"
			reg = mcp2515.REQOP_SLEEP
		elif Mode == mcp2515.OPMODE_NORMAL:
			print "Normal"
			reg = mcp2515.REQOP_NORMAL		

		self.mcp2515.BitModify(mcp2515.CANCTRL, mcp2515.REQOP, reg)

		done = False
		while not done:
			ready = self.mcp2515.ReadRegister(mcp2515.CANSTAT, 1)
			# ReadRegister returns always list, so we select [0]
			if (ready[0] & mcp2515.REQOP) == reg:
				done = True
			else:
				time.sleep(1)
				print "Writing 0x%x to register 0x%x" % (reg, mcp2515.CANCTRL)
				print "Reading 0x%x from register 0x%x" % (ready[0], mcp2515.CANSTAT)

	def Send(self, ID, Data):
		# Check state of buffers
		status = self.mcp2515.ReadStatus(mcp2515.SPI_READ_STATUS)
		
		if (status & 2) == 0:
			address = 0
		elif (status & 4) == 0:
			address = 0x10
		elif (status & 6) == 0:
			address = 0x20
		else:
			print "No empty buffer"
			return(0)
		
		# Set ID
		Header = [ID>>3, \
			(ID&0x07)<<5, 0, 0, \
			len(Data)]
		Raw = Header + Data

		# Copy data to buffer
		self.mcp2515.WriteRegister(mcp2515.TXB0SIDH + address, Raw)
		for one in Raw:		
			print "0x%x\t" % one,
		print ''
		# Send data
		self.mcp2515.BitModify(mcp2515.TXB0CTRL + address, mcp2515.TXREQ, mcp2515.TXREQ)
		
	def Receive(self):
		ReceiveBuffer = 0
		while ReceiveBuffer == 0:
			status = self.mcp2515.ReadRegister(mcp2515.CANINTF, 1)
			if (status[0] & mcp2515.RX0IF) != 0:
				ReceiveBuffer = 1
			elif (status[0] & mcp2515.RX1IF) != 0:
				ReceiveBuffer = 2
			else:	 
				time.sleep(1)
		ReceiveBuffer -= 1
		print "Received message in buffer %d" % ReceiveBuffer
		Data = self.mcp2515.ReadRegister(mcp2515.RXB0SIDH + ReceiveBuffer, 5)
		dlc = Data[4] & 0x0F
		id = (Data[0]<<3) + (Data[1]>>5) 
		print "DLC:%d, ID:0x%x" % (dlc, id)
		for one in Data:		
			print "0x%x\t" % one,
		print ''
		print 'Data: ',
		Data = self.mcp2515.ReadRegister(mcp2515.RXB0D0 + ReceiveBuffer, dlc)
		for one in Data:		
			print "0x%x\t" % one,
		print ''
		return(Data)


#typedef struct
#{
#		uint32_t id;				//!< ID der Nachricht (11 oder 29 Bit)
#		struct {
#			int rtr : 1;			//!< Remote-Transmit-Request-Frame?
#			int extended : 1;		//!< extended ID?
#		} flags;
#	uint8_t length;				//!< Anzahl der Datenbytes
#	uint8_t data[8];			//!< Die Daten der CAN Nachricht
	
#} can_t;


