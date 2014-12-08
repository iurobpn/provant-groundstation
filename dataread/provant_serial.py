#! /usr/bin/env python
# -*- coding:utf-8 -*-
# 
__author__ = 'Patrick'
import serial
import struct
import sys
from multwii_const import *
from provant_const import *
from array import *



class ProvantSerial:
    def __init__(self,window = None, serial_name='/dev/ttyVirtual2', baudrate_value=460800, debug_mode=False):
        ser = serial.Serial(serial_name, baudrate_value)
        ser.flush()
        self.window = window
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
        self.rcn = Rcnormalize()
        self.pid = Pid()
        self.ident = Ident()
        self.servo = Servo()
        self.motor_pins = Motor_pins()
        self.motor = Motor()
        self.imu = RawIMU()
        self.controldatain = Controldatain()
        self.controldataout = Controldataout()
        self.escdata = Escdata()
        self.sampleCount=0

    def write(self,char):
        self.ser.write(char)

    def decodeFloat(self, data):
        return struct.unpack('<f', ''.join(data))[0]

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

    def decode216(self, result):
        #print data
        is_negative = ((result>>8)&0xff) >= 128
        if is_negative:
            result -= 2**16
        return result

    def checksum_matches(self):
        check = self.who ^ self.size
        for x in xrange(0, self.size):
            check ^= ord(self.L[x])
        if((check == ord(self.L[self.size]))):
            self.sampleCount+=1
        return (check == ord(self.L[self.size]))

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

    def readSampleCount(self):
        return self.sampleCount

###############  PROPER MESSAGE DECODING IS HERE ##################################

    def takeData(self):
        if (self.who == MSP_ATTITUDE):
            if self.checksum_matches():
                self.attitude.roll = self.decode16(self.L[0:2])/10
                self.attitude.pitch = self.decode16(self.L[2:4])/10
                self.attitude.yaw = self.decode16(self.L[4:6])

                if self.window:
                    self.window.addArray('Attitude.Filtered',
                                         (self.attitude.roll, self.attitude.pitch, self.attitude.yaw),
                                         ('Roll','Pitch','Yaw'))



        if (self.who == MSP_RAW_GPS):
            if self.checksum_matches():
                self.raw_gps.fix = ord(self.L[0])
                self.raw_gps.numsats = ord(self.L[1])
                self.raw_gps.lat = self.decode32(self.L[2:6])
                self.raw_gps.lon = self.decode32(self.L[6:10])
                self.raw_gps.alt = self.decode16(self.L[10:12])
                self.raw_gps.speed = self.decode16(self.L[12:14])
                self.raw_gps.ggc = self.decode16(self.L[14:16])

                if self.window:
                    self.window.addArray('GPS',
                                         (self.raw_gps.fix,self.raw_gps.numsats,self.raw_gps.lat,self.raw_gps.lon,self.raw_gps.alt,self.raw_gps.speed,self.raw_gps.ggc),
                                         ('Fix','Numsats','Lat','Long','Alt','Veloc','GGC'))

        if (self.who == MSP_COMP_GPS):
            if self.checksum_matches():
                self.comp_gps.distance = self.decode16(self.L[0:2])
                self.comp_gps.direction = self.decode16(self.L[2:4])
                self.comp_gps.update = ord(self.L[4])

                if self.window:
                    self.window.addArray('Comp_gps',
                                         (self.comp_gps.distance,self.comp_gps.direction,self.comp_gps.update),
                                         ('Dist','Direction','Update'))                

        if (self.who == MSP_ANALOG):
            if self.checksum_matches():
                self.analog.vbat = ord(self.L[0])
                self.analog.power = self.decode16(self.L[1:3])
                self.analog.rssi = self.decode16(self.L[3:5])
                self.analog.current = self.decode16(self.L[5:7])

                if self.window:
                    self.window.addArray('Analog',
                                         (self.analog.vbat, self.analog.power,self.analog.rssi,self.analog.current),
                                         ('Vbat','Power','Rssi','Current'))

        if (self.who == MSP_ALTITUDE):
            if self.checksum_matches():
                self.altitude.alt = self.decode32(self.L[0:4])
                self.altitude.vario = self.decode16(self.L[4:6])

                if self.window:
                    self.window.addArray('Altitude',
                                         (self.altitude.alt,self.altitude.vario),
                                         ('Alt','Vario'))
                    self.window.verticalSlider_3.setValue(self.altitude.alt)


        if (self.who == MSP_STATUS):
            if self.checksum_matches():
                self.status.cycleTime = self.decode16(self.L[0:2])
                self.status.i2cec = self.decode16(self.L[2:4])
                self.status.sensor = self.decode16(self.L[4:6])
                self.status.flag = self.decode32(self.L[6:10])
                self.status.gccs = ord(self.L[10])

                if self.window:
                    self.window.addArray('Status',
                                         (self.status.cycleTime,self.status.i2cec,self.status.sensor,self.status.flag,self.status.gccs),
                                         ('CycleTime','Numi2cerror','Sensor','Flag','Gccs'))

        if (self.who == MSP_DEBUG):
            if self.checksum_matches():
                for i in xrange(0, self.size / 2):
                    self.debug.debug[i] = self.decode16(self.L[i*2:i*2+2])
                
                if self.window:
                    self.window.addArray('Debug', self.debug.debug)


        if (self.who == MSP_RC):
            if self.checksum_matches():
                for x in xrange(0, self.size / 2):
                    self.rc.channel[x] = ord(self.L[x * 2]) + (ord(self.L[x * 2 + 1]) << 8)

                if self.window:
                    self.window.addArray('RC_channel', self.rc.channel)

        if (self.who == MSP_PID):
            if self.checksum_matches():
                for x in xrange(0, self.size):
                    self.pid.pid[x] = ord(self.L[x])


        if (self.who == MSP_IDENT):
            if self.checksum_matches():
                self.ident.version = ord(self.L[0])
                self.ident.multtype = ord(self.L[1])
                self.ident.mspversion = ord(self.L[2])
                self.ident.capability = ord(self.L[3]) + (ord(self.L[4]) << 8) + (ord(self.L[5]) << 16) + (
                ord(self.L[6]) << 24)

        if (self.who == MSP_SERVO):
            if self.checksum_matches():
                for x in xrange(0, self.size / 2):
                    self.servo.servo[x] = self.decode16(self.L[x*2:x*2+2])
                if self.window:
                    self.window.addArray('ServoAngle',
                                         self.servo.servo[4:6],
                                         ('LServoAngle', 'RServoAngle'))


        if (self.who == MSP_MOTOR_PINS):
            if self.checksum_matches():
                pins = [None] * (self.size)
                for x in xrange(0, self.size):
                    self.motor_pins.pin[x] = ord(self.L[x])

        if (self.who == MSP_RAW_IMU):
            if self.checksum_matches():
                for i in range(3):
                    self.imu.acc[i] = self.decode16(self.L[i*2:i*2+2])
                for i in range(3, 6):
                    self.imu.gyr[i-3] = self.decode16(self.L[i*2:i*2+2])
                for i in range(6, 9):
                    self.imu.mag[i-6] = self.decode16(self.L[i*2:i*2+2])

                if self.window:
                    self.window.addArray('Attitude.Gyro', self.imu.gyr,('X','Y','Z'))
                    self.window.addArray('Attitude.Acc', self.imu.acc,('X','Y','Z'))
                    self.window.addArray('Attitude.Mag', self.imu.mag,('X','Y','Z'))

        if (self.who == MSP_MOTOR):
            if self.checksum_matches():
                for x in xrange(0, self.size / 2):
                    self.motor.motor[x] = ord(self.L[x * 2]) + (ord(self.L[x * 2 + 1]) << 8)

                if self.window:
                    self.window.addArray('MotorSetpoint',
                                         self.motor.motor[0:2],
                                         ('Lmotor', 'Rmotor'))
                    self.window.lMotorSetpoint.setValue(self.motor.motor[0])
                    self.window.rMotorSetpoint.setValue(self.motor.motor[1])



        if (self.who == MSP_CONTROLDATAIN):
            if self.checksum_matches():
                for x in xrange(0, 3):
                    self.controldatain.rpy[x]= self.decodeFloat(self.L[x*4:4+x*4])
                for x in xrange(3, 6):
                    self.controldatain.drpy[x-3]= self.decodeFloat(self.L[x*4:4+x*4])
                for x in xrange(6, 9):
                    self.controldatain.position[x-6]= self.decodeFloat(self.L[x*4:4+x*4])
                for x in xrange(9, 12):
                    self.controldatain.velocity[x-9]= self.decodeFloat(self.L[x*4:4+x*4])
                if self.window:
                    data = self.controldatain
                    self.window.addArray("Data.rpy",
                                         data.rpy,)
                    self.window.addArray("Data.drpy",
                                         data.drpy,)
                    self.window.addArray("Data.Position",
                                         data.position,)
                    self.window.addArray("Data.Velocity",
                                         data.velocity,)

        if (self.who == MSP_CONTROLDATAOUT):
            if self.checksum_matches():
                self.controldataout.servoLeft = self.decodeFloat(self.L[0:4])
                self.controldataout.escLeftNewtons  = self.decodeFloat(self.L[4:8])
                self.controldataout.escRightNewtons = self.decodeFloat(self.L[8:12])
                self.controldataout.servoRight = self.decodeFloat(self.L[12:16])
                self.controldataout.escLeftSpeed = self.decodeFloat(self.L[16:20])
                self.controldataout.escRightSpeed = self.decodeFloat(self.L[20:24])
                if self.window:
                    data = self.controldataout
                    self.window.addArray("ActuatorsCommand.Left",
                                         (data.escLeftNewtons, data.escLeftSpeed, data.servoLeft),
                                         ('Newtons', 'Speed', 'Servo'))
                    self.window.addArray("ActuatorsCommand.Right",
                                         (data.escRightNewtons, data.escRightSpeed, data.servoRight),
                                         ('Newtons', 'Speed', 'Servo'))

        if (self.who == MSP_ESCDATA):
            if self.checksum_matches():
                for x in xrange(0, 2):
                    self.escdata.rpm[x] = self.decode16(self.L[x*10:x*10+2])
                    self.escdata.current[x] = self.decodeFloat(self.L[x*10+2:x*10+6])
                    self.escdata.voltage[x] = self.decodeFloat(self.L[x*10+6:x*10+10])
                if self.window:
                    for i, escName in enumerate(['EscFeedbackLeft', 'EscFeedbackRight']):
                        self.window.addArray(escName,
                                             (self.escdata.rpm[i], self.escdata.current[i], self.escdata.voltage[i]),
                                             ('Rpm', 'Current', 'Voltage'))
                    self.window.lMotorRpm.setValue(self.escdata.rpm[0])
                    self.window.rMotorRpm.setValue(self.escdata.rpm[1])

        if (self.who == MSP_RCNORMALIZE):
            if self.checksum_matches():
                for x in xrange(0, self.size / 2):
                    self.rcn.channel[x] = self.decode16(self.L[x*2:x*2+2])
                #test
                if self.window:
                    self.window.addArray('RCN', self.rcn.channel[0:7])
                    self.window.left_joystick.move(self.rcn.channel[3], self.rcn.channel[2])
                    self.window.right_joystick.move(self.rcn.channel[0],self.rcn.channel[1])

   #                 self.window.verticalSlider_2.setValue(self.rcn.channel[0])
                    self.window.radioButton.setAutoExclusive(False);
                    self.window.radioButton_2.setAutoExclusive(False);
                    if self.rcn.channel[5]>50:
                        self.window.radioButton.setChecked(1)
                    else:
                        self.window.radioButton.setChecked(0)
                    if self.rcn.channel[6]>50:
                        self.window.radioButton_2.setChecked(1)
                    else:
                        self.window.radioButton_2.setChecked(0)
                    self.window.dial.setValue(self.rcn.channel[4])

if __name__ == '__main__':
    provant = ProvantSerial()

    while (1):
        provant.update()
        print("attitude", provant.attitude.roll, provant.attitude.pitch, provant.attitude.yaw)
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
        print("ident", provant.ident.version, provant.ident.multtype, provant.ident.mspversion, provant.ident.capability)
        print("imu:", provant.imu.gyr,provant.imu.acc,provant.imu.mag)
        print("servo", provant.servo.servo)
        print("motor pins", provant.motor_pins.pin)
        print("motor", provant.motor.motor)
        print("controldatain",provant.controldatain.rpy,provant.controldatain.drpy,provant.controldatain.position,provant.controldatain.velocity )
        print("controldataout",provant.controldataout.servoLeft,provant.controldataout.escLeftNewtons,provant.controldataout.escLeftSpeed,provant.controldataout.servoRight,provant.controldataout.escRightNewtons,provant.controldataout.escRightSpeed)
        print("escdata",provant.escdata.rpm,provant.escdata.current,provant.escdata.voltage)
