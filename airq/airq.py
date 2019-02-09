#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import serial

class AIRQ():
    def __init__(self, ser):
        self.ser = ser

    def debug(self):
        # read one, blocking
        byteData = self.ser.read(7)
        byteData += self.ser.read(self.ser.inWaiting()).encode('hex')
        print byteData.encode('hex')
        time.sleep(1)

    def num_format(self, num_hex):
        num_int = int(num_hex, 16)
        return float(format(num_int, '.10f'))

    def get_vout_by_serial(self, hex_str):
        #0005004d52ffaa
        #search for the start byte:aa
        index = hex_str.find('aa')

        # Get Vout_h index position
        if index==12:
            Vout_h_index = 0
        else:
            Vout_h_index = index + 2

        # Get Vout_l index position
        if Vout_h_index==12:
            Vout_l_index = 0
        else:
            Vout_l_index = Vout_h_index + 2

        # Start to caculate
        Vout_h = self.num_format(hex_str [Vout_h_index:Vout_h_index+2])
        Vout_l = self.num_format(hex_str [Vout_l_index:Vout_l_index+2])

        # Caculate the Vout
        Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5
        Vout = round(Vout, 3)
        return Vout

    def get_vout(self):
        line = self.get_serial_data()
        Vout = self.get_vout_by_serial(line)
        return Vout

    def get_serial_data(self):

        # read one, blocking
        bytes = 7
        byteData = self.ser.read(bytes)
        byteData += self.ser.read(self.ser.inWaiting()).encode('hex')
        line = byteData.encode('hex')
        return line

    def get_density(self):
        line = self.get_serial_data()
        Vout = self.get_vout_by_serial(line)
        A = 550

        # Dust density, unit: ug/m3
        dust_density = int(A * Vout)
        return dust_density


if __name__ == '__main__':

    def show(aq):

        #Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5    #输入电压
        Vout = aq.get_vout()
        dust_density = aq.get_density()
        #print "====================="
        #print "Vout:" + str(Vout) + "V"
        #dust_density = "dust_density:" + str(dust_density) + "ug/m3"

        sys.stdout.write("[  Vout: %s V     |    Dust density: %s ug/m3 ] \r" % (Vout, dust_density))
        sys.stdout.flush()
        time.sleep(1)

    try:
        ser = serial.Serial(
            port = 'COM7', # COM7 for windows
            baudrate = 2400,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1
        )

        aq = AIRQ(ser)
        while 1:
            show(aq)
    except KeyboardInterrupt:
        ser.close()
        print "\nQuit!"
