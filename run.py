#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time,sys,serial


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
        port='/dev/tty.usbserial',
        baudrate=2400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = 1
)
#ser.open()
#ser.write("testing")

def debug():
    byteData = ser.read(7) # read one, blocking
    byteData += ser.read(ser.inWaiting()).encode('hex')
    print byteData.encode('hex')

def num_format(num_hex):
    num_int = int(num_hex, 16)
    return float(format(num_int, '.10f'))

def get_vout(hex_str):
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
    Vout_h = num_format(hex_str [Vout_h_index:Vout_h_index+2])
    Vout_l = num_format(hex_str [Vout_l_index:Vout_l_index+2])

    Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5     #输入电压
    Vout = round(Vout, 3)
    return Vout

def show():
    byteData = ser.read(7)                          # read one, blocking
    byteData += ser.read(ser.inWaiting()).encode('hex')
    line = byteData.encode('hex')

    A = 550                                         #比例系数,由用户自定义
    Vout = get_vout(line)                           #输入电压
    #Vout = ((Vout_h * 256) + Vout_l) / 1024 * 5    #输入电压
    Dustdensity = int(A * Vout)                     #灰尘密度,单位 ug/m3
    #print "====================="
    #print "Vout:" + str(Vout) + "V"
    #DustDensity = "DustDensity:" + str(Dustdensity) + "ug/m3"
    sys.stdout.write("[  Vout: %s V     |    DustDensity: %s ug/m3 ] \r" % (Vout, Dustdensity))
    sys.stdout.flush()
    time.sleep(1)

try:
    while 1:
        show()

except KeyboardInterrupt:
    ser.close()
