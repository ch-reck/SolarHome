#!/usr/bin/python3

import csv
import time
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils

wp = {
  'RESCONTROL_WP': ModbusClient(host="192.168.1.233", port=502, unit_id=255, auto_open=True),
  'RESCONTROL_HK': ModbusClient(host="192.168.1.234", port=502, unit_id=255, auto_open=True)
}

past = ''
line = []
reader = csv.DictReader(open('/opt/res_control/res_control.csv'))
for r in reader:
  #print(r)
  for retry in range(3):
    rc = r['ResControl']
    adr = int(r['Adresse'])
    reg = wp[rc].read_holding_registers(adr, 1)
    if reg:
      reg = utils.get_2comp(reg[0], 16)
      e = int(r['Exponent'])
      value = reg if e == 0 else round(float(reg) * (10 ** e),3)
      module = r['Modul']
      # outut previous line if started reading new module
      if past != '' and past != module:
        print(rc + ',module=' + past + ' ' + (','.join(line)) + ' ' + str(time.time_ns()) )
        # prepare to create a new influxdb line
        line = []
      line.append( r['Namen'] + '=' + str(value) )
      past = module
      break
    else:
      print("read error", rc, adr)
      time.sleep(0.300)
if len(line) != 0:
  print(rc + ',module=' + past + ' ' + (','.join(line)) + ' ' + str(time.time_ns()) )
