# ReckSolarHome

This project uses simple python scripts to read the values from a solar inverter and battery system and feed the values into an Influx database. Current setup is tested to support:
* ```kostal2influxdb.py```  solar Kostal Pico 8.5 inverter
  https://www.kostal-solar-electric.com/en-gb/download/archiv#Solar%20Inverter/PIKO%204.2%20-%208.5/
* ```vartaElement2influxdb.py``` Varta Element 6 battery
  https://www.varta-storage.com/en/energiespeicher/element

Additionally a grafana configuration is included to depict the values.
![grafana kostal and varta](/images/grafana_KostalVarta.png)

A cronjob can be used to retrieve the information from the monitored systems and pass it to the influxdb:
```
*/5    *  *  *  *   /usr/bin/python3 /root/bin/vartaElement2influxdb.py 2>&1 >> /var/log/varta2db.log
*/5    *  *  *  *   /usr/bin/python3 /root/bin/kostal2influxdb.py 2>&1 >> /var/log/kostal2db.log
```

I'm running this in a RaspberryPI locally.

I wrote these scripts, since I did not find equal functionality searching the internet. For the Kostal system there are many code fragments and code to read the modbus interface, but none complete using the UI API.

TODOs:
* in grafana aggregate the values to a daily production and consumption graphs. 
* in the python scripts possibly compare the current values with the previously recorded measurements and thin the values written out to contain only the changed ones.
* in the influxdb aggregate values after a year into daily and monthly values and delete the single ingestions to limit the storage consumption.

Please let me know if it was useful to you and if you see any further desirable improvements.
