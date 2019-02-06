#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import serial

class AIRQ():
    def __init__(self, ser):
        self.ser = ser

    def debug(self):
        byteData = self.ser.read(7) # read one, blocking
        byteData += self.ser.read(self.ser.inWaiting()).encode('hex')
        print byteData.encode('hex')
        time.sleep(1)

    def num_format(self, num_hex):
        num_int = int(num_hex, 16)
        return float(format(num_int, '.10f'))

    def get_vout(self, hex_str):
        #0005004d52ffaa
        #找到数据开始位aa
        index = hex_str.find('aa')
        #获取Vout_h索引位置
        if index==12:
            Vout_h_index = 0
        else:
            Vout_h_index = index + 2
        #获取Vout_l索引位置
        if Vout_h_index==12:
            Vout_l_index = 0
        else:
            Vout_l_index = Vout_h_index + 2

        #开始计算
        Vout_h = self.num_format(hex_str [Vout_h_index:Vout_h_index+2])
        Vout_l = self.num_format(hex_str [Vout_l_index:Vout_l_index+2])
        #输入电压
        Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5
        Vout = round(Vout, 3)
        return Vout

    def get_serial_data(self):
        # read one, blocking
        bytes = 7
        byteData = self.ser.read(bytes)
        byteData += self.ser.read(self.ser.inWaiting()).encode('hex')
        line = byteData.encode('hex')
        return line

    def get_density(slef, Vout):
        A = 550

        #灰尘密度,单位 ug/m3
        Dustdensity = int(A * Vout)
        return Dustdensity

    def show(self):

        line = self.get_serial_data()

        Vout = self.get_vout(line)
        #Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5    #输入电压
        DustDensity = self.get_density(Vout)
        #print "====================="
        #print "Vout:" + str(Vout) + "V"
        #DustDensity = "DustDensity:" + str(Dustdensity) + "ug/m3"

        sys.stdout.write("[  Vout: %s V     |    DustDensity: %s ug/m3 ] \r" % (Vout, DustDensity))
        sys.stdout.flush()
        time.sleep(1)
