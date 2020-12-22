#!/usr/bin/python3

import time;
import datetime
import json
import urllib.request
from influxdb import InfluxDBClient

KostalPico_IP = '192.168.1.10'
baseUrl = 'http://' + KostalPico_IP + '/api/dxs.json?'

INFLUXDB_ADDRESS = '192.168.1.6'
INFLUXDB_PORT = 8086
INFLUXDB_USER = 'username'
INFLUXDB_PASSWORD = 'password'
INFLUXDB_DATABASE = 'kostal_pico'

dxsEntries = [
  {'key':'Status','Description':'Operating status [0:Off 1:idle 2:starting 3:MPP feeding 4:limit 5:feed]','type':'integer','dxs':'16780032'},
  {'key':'PV_DC_W','Description':'Power Values Total DC input [W]','type':'double','dxs':'33556736'},
  {'key':'PV1in_V','Description':'PV DC input 1 Voltage [V]','type':'double','dxs':'33555202'},
  {'key':'PV1in_A','Description':'PV DC input 1 Current [A]','type':'double','dxs':'33555201'},
  {'key':'PV1in_W','Description':'PV DC input 1 Power [W]','type':'double','dxs':'33555203'},
  {'key':'PV2in_V','Description':'PV DC input 2 Voltage [V]','type':'double','dxs':'33555458'},
  {'key':'PV2in_A','Description':'PV DC input 2 Current [A]','type':'double','dxs':'33555457'},
  {'key':'PV2in_W','Description':'PV DC input 2 Power [W]','type':'double','dxs':'33555459'},
  {'key':'P_SelfConsumption','Description':'Power Values Self consumption [W]','type':'double','dxs':'83888128'},
  {'key':'Batt_V','Description':'Battery Voltage [V]','type':'double','dxs':'33556226'},
  {'key':'Batt_level','Description':'Battery Charging status [%]','type':'double','dxs':'33556229'},
  {'key':'Batt_charge_A','Description':'Battery Charging [A]','type':'double','dxs':'33556238'},
  {'key':'Batt_mode','Description':'Battery Charge/discharge status [0:charge 1:discharge]','type':'integer','dxs':'33556230'},
  {'key':'Batt_cycles','Description':'Battery Charge cycles','type':'integer','dxs':'33556228'},
  {'key':'Batt_temp','Description':'Battery Temperature [C]','type':'double','dxs':'33556227'},
  {'key':'Home_consumption_solar','Description':'Home consumption covered by Solar generator [W]','type':'double','dxs':'83886336'},
  {'key':'Home_consumption_batt','Description':'Home consumption covered by Battery [W]','type':'double','dxs':'83886592'},
  {'key':'Home_consumption_grid','Description':'House Home consumption covered by Grid [W]','type':'double','dxs':'83886848'},
  {'key':'Home_consumption_phase1','Description':'Phase selective home consumption Phase 1 [W]','type':'double','dxs':'83887106'},
  {'key':'Home_consumption_phase2','Description':'House Phase selective home consumption Phase 2 [W]','type':'double','dxs':'83887362'},
  {'key':'Home_consumption_phase3','Description':'House Phase selective home consumption Phase 3 [W]','type':'double','dxs':'83887618'},
  {'key':'Grid_ouput_W','Description':'Grid Output power [W]','type':'double','dxs':'67109120'},
  {'key':'Grid_frequency','Description':'Grid Grid frequency [Hz]','type':'double','dxs':'67110400'},
  {'key':'Grid_cosPhi','Description':'Grid CosPhi','type':'double','dxs':'67110656'},
  {'key':'Grid_limiting','Description':'Grid Limitation on [%]','type':'double','dxs':'67110144'},
  {'key':'Grid_phase1_V','Description':'Grid Phase 1 - Voltage [V]','type':'double','dxs':'67109378'},
  {'key':'Grid_phase1_A','Description':'Grid Phase 1 - Current [A]','type':'double','dxs':'67109377'},
  {'key':'Grid_phase_W','Description':'Grid Phase 1 - Power [W]','type':'double','dxs':'67109379'},
  {'key':'Grid_phase2_V','Description':'Grid Phase 2 - Voltage [V]','type':'double','dxs':'67109634'},
  {'key':'Grid_phase2_A','Description':'Grid Phase 2 - Current [A]','type':'double','dxs':'67109633'},
  {'key':'Grid_phase2_W','Description':'Grid Phase 2 - Power [W]','type':'double','dxs':'67109635'},
  {'key':'Grid_phase3_V','Description':'Grid Phase 3 - Voltage [V]','type':'double','dxs':'67109890'},
  {'key':'Grid_phase3_A','Description':'Grid Phase 3 - Current [A]','type':'double','dxs':'67109889'},
  {'key':'Grid_phase3_W','Description':'Grid Phase 3 - Power [W]','type':'double','dxs':'67109891'},
  {'key':'AnalogInput1_V','Description':'Analog input 1 [V]','type':'double','dxs':'167772417'},
  {'key':'AnalogInput2_V','Description':'Analog input 2 [V]','type':'double','dxs':'167772673'},
  {'key':'AnalogInput3_V','Description':'Analog input 3 [V]','type':'double','dxs':'167772929'},
  {'key':'AnalogInput4_V','Description':'Analog input 4 [V]','type':'double','dxs':'167773185'},
  {'key':'S0_PulsesPerUnit','Description':'S0 input Number of energy pulses per unit','type':'integer','dxs':'184549632'},
  {'key':'S0_PulseUnit_Sec','Description':'S0 input Number of energy pulses unit [seconds]','type':'integer','dxs':'150995968'},
  {'key':'Day_yield_Wh','Description':'Day Yield [Wh]','type':'double','dxs':'251658754'},
  {'key':'Day_homeConsumption_Wh','Description':'Day Home consumption [Wh]','type':'double','dxs':'251659010'},
  {'key':'Day_selfConsumption_Wh','Description':'Day Self consumption [Wh]','type':'double','dxs':'251659266'},
  {'key':'Day_selfConsumption_Perc','Description':'Day Self consumption rate [%]','type':'double','dxs':'251659278'},
  {'key':'Day_selfSufficiency_Perc','Description':'Day Degree of self sufficiency [%]','type':'double','dxs':'251659279'},
  {'key':'Total_yield_kWh','Description':'Total Yield [kWh]','type':'double','dxs':'251658753'},
  {'key':'Total_homeConsumption_kWh','Description':'Total Home consumption [kWh]','type':'double','dxs':'251659009'},
  {'key':'Total_selfConsumption_kWh','Description':'Total Self consumption [kWh]','type':'double','dxs':'251659265'},
  {'key':'Total_selfConsumption_Perc','Description':'Total Self consumption rate [%]','type':'double','dxs':'251659280'},
  {'key':'Total_selfSufficiency_Perc','Description':'Total Degree of self sufficiency [%]','type':'double','dxs':'251659281'},
  {'key':'Total_operationTime_H','Description':'Total Operation time [h]','type':'integer','dxs':'251658496'},
]

#print("length={}".format(len(dxsEntries)))

# for dxsEntry in dxsEntries[0:10]:
  # key = dxsEntry['key']
  # description = dxsEntry['Description']
  # type = dxsEntry['type']
  # dxs = dxsEntry['dxs']
  # print(key,description,type,dxs)

#print(list(entry['dxs'] for entry in dxsEntries[0:20]))

def query(entries):
  query = 'dxsEntries=' + '&dxsEntries='.join(list(entry['dxs'] for entry in entries))
  content = urllib.request.urlopen(baseUrl + query).read()
  js = json.loads(content)
  return js['dxsEntries']

def addToLookup(entries, lookup):
  for entry in entries:
    dxs = str(entry['dxsId'])
    value = entry['value']
    # print(dxs + "=" + str(value))
    lookup[dxs] = value

# now start the queries
current_time = time.gmtime()
results = {}
addToLookup(query(dxsEntries[0:20]),results)
addToLookup(query(dxsEntries[20:39]),results)
addToLookup(query(dxsEntries[39:51]),results)

# print()
# print("length " + str(len(results)))
# print()
# print(results)
# print()

# for dxsEntry in dxsEntries:
  # key = dxsEntry['key']
  # description = dxsEntry['Description']
  # type = dxsEntry['type']
  # dxs = str(dxsEntry['dxs'])
  # #value = next((entry for entry in results if (entry.get('dxsId') == dxs) and print( entry.get('dxsId') ) ), None)
  # #value = search(dxs, results)
  # # value = next(filter(lambda entry: entry['dxsId'] == str(dxs), results), None)
  # value = results[dxs]
  # print(dxs,key,type,value,description)

#print(list(entry['value'] for entry in results))

# setup data for DB row
data = dict()
for dxsEntry in dxsEntries:
  key = dxsEntry['key']
  dxs = str(dxsEntry['dxs'])
  value = results[dxs]
  data[key] = value;
  #print(dxs,key,type,value,description)

# create influx DB ingestion message and write to server
json_body = []
timestamp = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
json_body.append({'time':timestamp, 'measurement':'inverter', 'tags': {'location':'reck_kostal'}, 'fields':data})
print(json_body)

# now feed the data into the influxdb
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
databases = influxdb_client.get_list_database()
if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
    influxdb_client.create_database(INFLUXDB_DATABASE)
    print('INFO', 'initialized DB')
influxdb_client.switch_database(INFLUXDB_DATABASE)
influxdb_client.write_points(json_body)

print("Done.")
