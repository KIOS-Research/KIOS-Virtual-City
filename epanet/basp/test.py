from influxdb import InfluxDBClient
import uuid
import random
import time
import wntr

try:
    client = InfluxDBClient(host='localhost', port=8086, username='kios',
                            password='kios1234!', database='virtual_city')
except:
    client.close()


query = 'SELECT * FROM water_output_stepexecution2_sensors'
results = client.query(query)
print(len(results))
'''
client_write_start_time = time.perf_counter()

print(round(time.time() * 1000))
test = ['influx33_sensors,sensorid=pressure_1,sensortype=pressure,nodelink=node,nodelinkid=n1,min=0.0,max=100.0,resolution=0.1,uncertainty=5,uncertaintydist=uniform,lat=34.68618568144877,long=33.03823996696676 expname="influx33" 1612510628602']

client.write_points(test, database='virtual_city', time_precision='ms', batch_size=10000, protocol='line')

client_write_end_time = time.perf_counter()

print("Client Library Write: {time}s".format(time=client_write_end_time - client_write_start_time))
'''