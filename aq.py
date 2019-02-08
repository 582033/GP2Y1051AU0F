from airq import airq
import serial

import random
import prometheus_client
from prometheus_client import Gauge
from flask import Response, Flask

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

app = Flask(__name__)
exporter_value = Gauge("dust_density", "Dust density of the request")
@app.route("/metrics")
def r_value():
    aq = airq.AIRQ(ser)
    dust_density = aq.get_density()
    exporter_value.set(dust_density)
    return Response(prometheus_client.generate_latest(exporter_value), mimetype="text/plain")

try:
    app.run(host="0.0.0.0")
    # while 1:
        # aq.show()
        # debug()
        # print get_serial_data()
        # time.sleep(1)

except KeyboardInterrupt:
    aq.ser.close()
