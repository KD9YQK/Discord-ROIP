import sounddevice as sd
import numpy as np
import os
import serial
from color_codes import colors
from config import RX_ADDRESS, TX_ADDRESS, DELAY, RX_THRESHOLD, TX_THRESHOLD
from pynput.keyboard import Key, Controller

#OPCODES
IDLE = 0
RX = 1
TX = 2

kb = Controller()

class ptt():
	stream = None
	rx_rms = 0.0
	tx_rms = 0.0
	ptt = None

	def __init__(self):
		self.ptt = serial.Serial()
		self.ptt.port = '/dev/ttyUSB0'
		self.ptt.baudrate = 9600
		self.ptt.rts = False
		print(f'{colors.fg.green}PTT Script Starting{colors.reset}')
		print('CTRL-C to quit')

	def disp(self,opcode):
		t = str(int(self.tx_rms))#[0:3]
		r = str(int(self.rx_rms))#[0:3]
		print(" "*50, end='\r')
		message = ""
		if opcode == IDLE:
			message = f"Status: {colors.fg.yellow}IDLE  {colors.reset}RX_RMS: {r}  TX_RMS: {t}"
		elif opcode == RX:
			message = f"Status: {colors.fg.green} RX   {colors.reset}RX_RMS: {colors.fg.green}{r}{colors.reset}  TX_RMS: {t}"
		elif opcode == TX:
			message = f"Status: {colors.fg.red} TX   {colors.reset}RX_RMS: {r}  TX_RMS: {colors.fg.red}{t}{colors.reset}"
		print(message, end = '\r')

	def set_rx_rms(self,indata, frames, time, status):
		self.rx_rms = np.linalg.norm(indata)*10
		
	def set_tx_rms(self,indata, frames, time, status):
		self.tx_rms = np.linalg.norm(indata)*10
		
	def setSource(self,source):
		os.system(f'pactl set-default-source "{source}"')

	def update_loop(self):
		self.setSource(RX_ADDRESS)
		self.stream = sd.InputStream(callback=self.set_rx_rms)
		with self.stream:
			sd.sleep(DELAY)
		if self.rx_rms < RX_THRESHOLD:
			kb.release(Key.shift)
			self.disp(IDLE)
			self.setSource(TX_ADDRESS)
			self.stream = sd.InputStream(callback=self.set_tx_rms)
			with self.stream:
				sd.sleep(DELAY)
			if self.tx_rms > TX_THRESHOLD:
				self.disp(TX)
				self.ptt.open()
				while True:
					self.ptt.rts = True
					self.stream = sd.InputStream(callback=self.set_tx_rms)
					with self.stream:
						sd.sleep(DELAY)
					if self.tx_rms <= TX_THRESHOLD:
						self.disp(IDLE)
						self.ptt.close()
						self.ptt.rts = False
						break
					else:
						self.disp(TX)
		else:
			kb.press(Key.shift)
			self.disp(RX)

t = ptt()
try:
	while True:
		t.update_loop()
except KeyboardInterrupt:
	t.ptt.close()
	t.ptt.rts = False
	print('')
	print('Goodbye')
	exit()
