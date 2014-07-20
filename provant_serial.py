#! /usr/bin/env python
# -*- coding:utf-8 -*-

import serial
from multwii_const import *
ser = serial.Serial('/dev/ttyUSB11', 460800, timeout=1)
ser.flush()
while(1):
	#pega head
	if(ord(ser.read())==MSP_HEAD[0]):			#checkhead1
		if(ord(ser.read())==MSP_HEAD[1]):		#checkhead2
			if(ord(ser.read())==MSP_HEAD[2]):	#checkhead3
				size=ord(ser.read())	 		#pega tamanho		
				who=ord(ser.read())				#descobre quem é
				word=ser.read(size+1)			#pega os dados + checksum
				L = list(word)					#passa para uma lista


				if(who==MSP_ATTITUDE):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						x=ord(L[0])+(ord(L[1])<<8)
						y=ord(L[2])+(ord(L[3])<<8)
						z=ord(L[4])+(ord(L[5])<<8)
						print("attitude",x,y,z)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_RAW_GPS):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						fix    =ord(L[0])
						numsats=ord(L[1])
						lat    =ord(L[2])+(ord(L[3])<<8)+(ord(L[4])<<16)+(ord(L[5])<<24)
						lon    =ord(L[6])+(ord(L[7])<<8)+(ord(L[8])<<16)+(ord(L[9])<<24)
						alt    =ord(L[10])+(ord(L[11])<<8)
						speed  =ord(L[12])+(ord(L[13])<<8)
						ggc    =ord(L[14])+(ord(L[15])<<8)
						print("gps raw",fix,numsats,lat,lon,alt,speed,ggc)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_COMP_GPS):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						distance  =ord(L[0])+(ord(L[1])<<8)
						direction =ord(L[2])+(ord(L[3])<<8)
						update    =ord(L[4])
						print("gps comp",distance,direction,update)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_ANALOG):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						vbat      =ord(L[0])
						power     =ord(L[1])+(ord(L[2])<<8)
						rssi      =ord(L[3])+(ord(L[4])<<8)
						current   =ord(L[5])+(ord(L[6])<<8)
						print("analog",vbat,power,rssi,current)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_ALTITUDE):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						alt       =ord(L[0])+(ord(L[1])<<8)+(ord(L[2])<<16)+(ord(L[3])<<24)
						vario     =ord(L[4])+(ord(L[5])<<8)
						print("altitude",alt,vario)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_STATUS):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						cycleTime  =ord(L[0])+(ord(L[1])<<8)
						i2cec      =ord(L[2])+(ord(L[3])<<8)
						sensor     =ord(L[4])+(ord(L[5])<<8)
						flag       =ord(L[6])+(ord(L[7])<<8)+(ord(L[8])<<16)+(ord(L[9])<<24)
						gccs       =ord(L[10])
						print("status",cycleTime,i2cec,sensor,flag,gccs)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_DEBUG):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						debug=[None]*(size/2)
						for x in xrange(0,size/2):
							debug[x]  =ord(L[x*2])+(ord(L[x*2+1])<<8)
						print("debug",debug)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_RC):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						channel=[None]*(size/2)
						for x in xrange(0,size/2):
							channel[x]  =ord(L[x*2])+(ord(L[x*2+1])<<8)
						print("rc",channel)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_PID):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						pid=[None]*size
						for x in xrange(0,size):
							pid[x]  =ord(L[x])
						print("pid",pid)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_IDENT):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						version      =ord(L[0])
						multtype     =ord(L[1])
						mspversion   =ord(L[2])
						capability   =ord(L[3])+(ord(L[4])<<8)+(ord(L[5])<<16)+(ord(L[6])<<24)
						print("ident",version,multtype,mspversion,capability)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_SERVO):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						servo=[None]*(size/2)
						for x in xrange(0,size/2):
							servo[x]  =ord(L[x*2])+(ord(L[x*2+1])<<8)
						print("servo",servo)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_MOTOR_PINS):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						pins=[None]*(size)
						for x in xrange(0,size):
							pins[x]  =ord(L[x])
						print("motor pins",pins)
					else:
						print("checksum error !")
						print(ord(L[size]),check)

				if(who==MSP_MOTOR):
					check=who^size
					for x in xrange(0,size):
						check^=ord(L[x])
					if(check==ord(L[size])):
						motor=[None]*(size/2)
						for x in xrange(0,size/2):
							motor[x]  =ord(L[x*2])+(ord(L[x*2+1])<<8)
						print("motor",motor)
					else:
						print("checksum error !")
						print(ord(L[size]),check)



					


ser.close()