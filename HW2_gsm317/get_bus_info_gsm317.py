#Author: Gregory Mayes, NYU, September 2016
############################
#Code written to pull next stop information for each vehicle
#on a bus line from the MTA API interface and output to csv.
#For HW2, Assignment 2 of PUI2016.
############################

from __future__ import print_function
import json
import urllib2
import sys
import numpy
import matplotlib
matplotlib.use('agg')
import pylab as pl
import csv

#input error message

if not len(sys.argv) == 4:
    print("Invalid number of arguments. Run as: python get_bus_info.py MTA_KEY BUS_LINE FILE_NAME")
    sys.exit()

#Pull json data from MTA bustime
#key = 5d9e7639-7cac-45c2-934d-2f274b5e63c7
    
mtakey = sys.argv[1]
busline = sys.argv[2]
filename = sys.argv[3]

url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s"%(mtakey, busline)

response = urllib2.urlopen(url)
data = response.read().decode("utf-8")
data1 = json.loads(data)
data2 = data1['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

#Modified from example by 'the Tin Man' at 
#http://stackoverflow.com/questions/1871524/how-can-i-convert-json-to-csv-with-python

stop_name = data2[0]['MonitoredVehicleJourney']['MonitoredCall']['StopPointName']

if len(stop_name) > 0:
    stop_name2 = stop_name
else:
    stop_name2 = "N/A"
    
stop_status = data2[0]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']

if len(stop_status) > 0:
    stop_status2 = stop_status
else:
    stop_status2 = "N/A"

fout = csv.writer(open(filename, 'wb+'))

fout.writerow(['Latitude', 'Longitude', 'Stop Name', 'Stop Status'])

for data2 in data2:
    fout.writerow([data2['MonitoredVehicleJourney']['VehicleLocation']['Latitude'],
                  data2['MonitoredVehicleJourney']['VehicleLocation']['Longitude'],
                  stop_name2,
                  data2['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']])
