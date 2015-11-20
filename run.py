#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time,serial


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('/dev/tty.usbserial', 2400)
ser = serial.Serial(
        port='/dev/tty.usbserial',
        baudrate=2400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
)
#ser.open()
#ser.write("testing")

def num_format(num_hex):
    num_int = int(num_hex, 16)
    return float(format(num_int, '.10f'))

def show():
    line = ser.readline().encode('hex')
    #Dustdensity 灰尘密度
    #Vout       输入电压
    #004d57ffaa000a
    A = 550  #比例系数,由用户自定义
    Start = num_format(line [8:10])
    Vout_h = num_format(line [10:12])
    Vout_l = num_format(line [12:14])
    Verf_h = num_format(line [0:2])
    Verf_l = num_format(line [2:4])
    Verf = num_format(line [4:6])
    Stop = num_format(line [6:8])

    Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5     #输入电压
    Dustdensity = int(A * Vout)                     #灰尘密度,单位 ug/m3
    print "====================="
    #print "Start:" + str(Start)
    #print "Vout_h:" + str(Vout_h)
    #print "Vout_l:" + str(Vout_l)
    #print "Verf_h:" + str(Verf_h)
    #print "Verf_l:" + str(Verf_l)
    #print "Verf:" + str(Verf)
    #print "Stop:" + str(Stop)
    print "Vout:" + str(Vout) + "V"
    print "Dustdensity:" + str(Dustdensity) + "ug/m3"
    #time.sleep(1)

def debug():
    line = ser.readline().encode('hex')
    print line


try:
    while 1:
        show()

except KeyboardInterrupt:
    ser.close()
