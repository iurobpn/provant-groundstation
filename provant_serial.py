#! /usr/bin/env python
# -*- coding:utf-8 -*-
# 
import serial
from multwii_const import *



class ProvantSerial:
    def __init__(self, serial_name='/dev/ttyUSB11', baudrate_value=460800, debug_mode=False):
        ser = serial.Serial(serial_name, baudrate_value)
        ser.flush()
        self.ser = ser
        self.debug = debug_mode
        self.attitude = Attitude()
        self.raw_gps = Raw_gps()
        self.comp_gps = Comp_gps()
        self.analog = Analog()
        self.altitude = Altitude()
        self.status = Status()
        self.debug = Debug()
        self.rc = Rc()
        self.pid = Pid()
        self.ident = Ident()
        self.servo = Servo()
        self.motor_pins = Motor_pins()
        self.motor = Motor()


    def decode32(self, data):
        #print data
        result = (ord(data[0]) & 0xff) + ((ord(data[1]) & 0xff) << 8) + ((ord(data[2]) & 0xff) << 16) + ((ord(data[3]) & 0xff) << 24)
        is_negative = ord(data[3]) >= 128
        if is_negative:
            result -= 2**32
        return result

    def decode16(self, data):
        #print data
        result = (ord(data[0]) & 0xff) + ((ord(data[1]) & 0xff) << 8)
        is_negative = ord(data[1]) >= 128
        if is_negative:
            result -= 2**16
        return result


    def update(self):
        while self.ser.inWaiting() > 10:
            self.takeHead()

    def takeHead(self):
        if (ord(self.ser.read()) == MSP_HEAD[0]):  # checkhead1
            if (ord(self.ser.read()) == MSP_HEAD[1]):  #checkhead2
                if (ord(self.ser.read()) == MSP_HEAD[2]):  #checkhead3
                    self.solve_type()

    def solve_type(self):
        self.size = ord(self.ser.read())  # pega tamanho
        self.who = ord(self.ser.read())  # descobre quem é
        self.word = self.ser.read(self.size + 1)  # pega os dados + checksum
        self.L = list(self.word)  # passa para uma lista
        self.takeData()

    def takeData(self):
        if (self.who == MSP_ATTITUDE):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                self.attitude.x = self.decode16(self.L[0:2])
                self.attitude.y = self.decode16(self.L[2:4])
                self.attitude.z = self.decode16(self.L[4:6])
                '''
                print("attitude",self.attitude.x,self.attitude.y,self.attitude.z)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
                '''

        if (self.who == MSP_RAW_GPS):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                self.raw_gps.fix = ord(self.L[0])
                self.raw_gps.numsats = ord(self.L[1])
                self.raw_gps.lat = self.decode32(self.L[2:6])
                self.raw_gps.lon = self.decode32(self.L[6:10])
                self.raw_gps.alt = self.decode16(self.L[10:12])
                self.raw_gps.speed = self.decode16(self.L[12:14])
                self.raw_gps.ggc = self.decode16(self.L[14:16])
                '''
                print("gps raw",self.raw_gps.fix,self.raw_gps.numsats,self.raw_gps.lat,self.raw_gps.lon,self.raw_gps.alt,self.raw_gps.speed,self.raw_gps.ggc)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
                '''

        if (self.who == MSP_COMP_GPS):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                self.comp_gps.distance = self.decode16(self.L[0:2])
                self.comp_gps.direction = self.decode16(self.L[2:4])
                self.comp_gps.update = ord(self.L[4])
            '''
                print("gps comp",self.comp_gps.distance,self.comp_gps.direction,self.comp_gps.update)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
            '''

        if (self.who == MSP_ANALOG):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                self.analog.vbat = ord(self.L[0])
                self.analog.power = self.decode16(self.L[1:3])
                self.analog.rssi = self.decode16(self.L[3:5])
                self.analog.current = self.decode16(self.L[5:7])
            '''
                print("analog",self.analog.vbat,self.analog.power,self.analog.rssi,self.analog.current)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
            '''

        if (self.who == MSP_ALTITUDE):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                self.altitude.alt = self.decode32(self.L[0:4])
                self.altitude.vario = self.decode16(self.L[4:6])
            '''
                print("altitude",self.altitude.alt,self.altitude.vario)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
            '''

        if (self.who == MSP_STATUS):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                self.status.cycleTime = self.decode16(self.L[0:2])
                self.status.i2cec = self.decode16(self.L[2:4])
                self.status.sensor = self.decode16(self.L[4:6])
                self.status.flag = self.decode32(self.L[6:10])
                self.status.gccs = ord(self.L[10])
            '''
                print("status",self.status.cycleTime,self.status.i2cec,self.status.sensor,self.status.flag,self.status.gccs)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
            '''

        if (self.who == MSP_DEBUG):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                debug = [None] * (self.size / 2)
                for x in xrange(0, self.size / 2):
                    self.debug.debug[x] = ord(self.L[x * 2]) + (ord(self.L[x * 2 + 1]) << 8)
                '''
                print("debug",self.debug.debug)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
                '''

        if (self.who == MSP_RC):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                channel = [None] * (self.size / 2)
                for x in xrange(0, self.size / 2):
                    self.rc.channel[x] = ord(self.L[x * 2]) + (ord(self.L[x * 2 + 1]) << 8)
                '''
                print("rc",self.rc.channel)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
                '''

        if (self.who == MSP_PID):
            print("PID!")
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                pid = [None] * self.size
                for x in xrange(0, self.size):
                    self.pid.pid[x] = ord(self.L[x])
                print("pid", self.pid.pid)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]), check)

        if (self.who == MSP_IDENT):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                self.ident.version = ord(self.L[0])
                self.ident.multtype = ord(self.L[1])
                self.ident.mspversion = ord(self.L[2])
                self.ident.capability = ord(self.L[3]) + (ord(self.L[4]) << 8) + (ord(self.L[5]) << 16) + (
                ord(self.L[6]) << 24)
                '''
                print("ident",self.ident.version,self.ident.multtype,self.ident.mspversion,self.ident.capability)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
                '''

        if (self.who == MSP_SERVO):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                servo = [None] * (self.size / 2)
                for x in xrange(0, self.size / 2):
                    self.servo.servo[x] = self.decode16(self.L[x*2:x*2+2])
                '''
                print("servo",self.servo.servo)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
                '''

        if (self.who == MSP_MOTOR_PINS):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                pins = [None] * (self.size)
                for x in xrange(0, self.size):
                    self.motor_pins.pin[x] = ord(self.L[x])
                '''
                print("motor pins",self.motor_pins.pin)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
                '''

        if (self.who == MSP_MOTOR):
            check = self.who ^ self.size
            for x in xrange(0, self.size):
                check ^= ord(self.L[x])
            if (check == ord(self.L[self.size])):
                motor = [None] * (self.size / 2)
                for x in xrange(0, self.size / 2):
                    self.motor.motor[x] = ord(self.L[x * 2]) + (ord(self.L[x * 2 + 1]) << 8)
                '''
                print("motor",self.motor.motor)
            else:
                print("checksum error !")
                print(ord(self.L[self.size]),check)
                '''


if __name__ == '__main__':
    provant = ProvantSerial()

    while (1):
        provant.update()
        print("attitude", provant.attitude.x, provant.attitude.y, provant.attitude.z)
        print("gps raw", provant.raw_gps.fix, provant.raw_gps.numsats, provant.raw_gps.lat, provant.raw_gps.lon,
              provant.raw_gps.alt, provant.raw_gps.speed, provant.raw_gps.ggc)
        print("gps comp", provant.comp_gps.distance, provant.comp_gps.direction, provant.comp_gps.update)
        print("analog", provant.analog.vbat, provant.analog.power, provant.analog.rssi, provant.analog.current)
        print("altitude", provant.altitude.alt, provant.altitude.vario)
        print("status", provant.status.cycleTime, provant.status.i2cec, provant.status.sensor, provant.status.flag,
              provant.status.gccs)
        print("debug", provant.debug.debug)
        print("rc", provant.rc.channel)
        print("pid", provant.pid.pid)
        print(
        "ident", provant.ident.version, provant.ident.multtype, provant.ident.mspversion, provant.ident.capability)
        print("servo", provant.servo.servo)
        print("motor pins", provant.motor_pins.pin)
        print("motor", provant.motor.motor)
