from airq import airq
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
# if uses Rpi serial port, the serial port login must be disable/stop first
# sudo systemctl stop serial-getty@ttyS0.service
ser = serial.Serial(
    port = 'COM7', # COM7 for windows
    baudrate = 2400,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

try:
    aq = airq.AIRQ(ser)

    while 1:
        aq.show()
        # debug()
        # print get_serial_data()
        # time.sleep(1)

except KeyboardInterrupt:
    aq.ser.close()
