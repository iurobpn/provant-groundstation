__author__ = 'will'
import os
import serial
from serial.tools import list_ports

# def list_serial_ports():
#     # Windows
#     if os.name == 'nt':
#         # Scan for available ports.
#         available = []
#         for i in range(256):
#             try:
#                 s = serial.Serial(i)
#                 available.append('COM'+str(i + 1))
#                 s.close()
#             except serial.SerialException:
#                 pass
#         return available
#     else:
#         # Mac / Linux
#         return [port[0] for port in list_ports.comports ()]
#
#
import sys
import glob

def list_serial_ports():
    """Returns all available COM ports
    """
    if sys.platform.startswith('win'):
        result = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                s.close()
                result.append('COM' + str(i + 1))
            except serial.SerialException:
                pass
        return result

    elif sys.platform.startswith('linux'):
        paths = ['/dev/rf*','/dev/tty*']
        lists = [file for file in [glob.glob(path) for path in paths]]#list(glob.glob('/dev/tty*')) or list(glob.glob('/def/rf*'))
        newlist = []
        for list in lists:
            newlist.extend(list)
        return newlist

    elif sys.platform.startswith('darwin'):
        return glob.glob('/dev/tty.*')