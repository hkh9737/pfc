# -*- coding: utf-8 -*-
#!/bin/bash
import serial
import smbus
import time
import sys
import os
import termios
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pfc_connection_arduino import pfc_connection_arduino


class dht11_hum:
	SLAVE_ADDRESS = pfc_connection_arduino.SLAVE_ADDRESS
	I2C_BUS = None
	ACT_TMPL = pfc_connection_arduino.ACTUATOR_MES_TMPL
	ACT_INDICATOR = None
	MESS = None
	def __init__(self):
		self.I2C_BUS = smbus.SMBus(1)
		self.connect()
	def connect(self):
		for (act_idx,act_key) in enumerate(self.ACT_TMPL):
			if act_key[0] == "dht11_hum":
				self.ACT_INDICATOR = act_idx
				break;
		self.MESS = [0]*(len(self.ACT_TMPL))


	def getValue(self):
		self.MESS[self.ACT_INDICATOR] = 1
		self.I2C_BUS.write_i2c_block_data(self.SLAVE_ADDRESS, int(self.ACT_INDICATOR), self.MESS)
		print(int(self.ACT_INDICATOR))
		time.sleep(5)
		receive_data = self.I2C_BUS.read_i2c_block_data(self.SLAVE_ADDRESS,0)
		res = ""
		for v in receive_data:
			if v == 255:
				break;
			else:
				res += chr(v)
		return res

if __name__ == '__main__':
	dht11_hum = dht11_hum()
	order = sys.argv[1]

	if order == 'get':
		v = dht11_hum.getValue()
		print("result=" + str(v)+ "," + str(datetime.now()))
