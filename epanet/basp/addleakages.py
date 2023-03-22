import pandas as pd
import numpy as np
import wntr
import yaml
# import time
from math import sqrt
import json


def addwaterleak(yalmfile, wn):
    leak_pipes = yaml.load(yalmfile, Loader=yaml.FullLoader)
    start_time = leak_pipes['times']['StartTime']
    end_time = leak_pipes['times']['EndTime']
    leakages = leak_pipes['leakages']
    leakages = leakages[1:]
    number_of_leaks = len(leakages)
    for name, node in wn.junctions():
        node.required_pressure = 25

    time_step = round(wn.options.time.hydraulic_timestep)
    time_stamp = pd.date_range(start_time, end_time, freq=str(time_step / 60) + "min")

    wn.options.time.duration = (len(time_stamp) - 1) * 300  # 5min step

    TIMESTEPS = int(wn.options.time.duration / wn.options.time.hydraulic_timestep)

    # Initialize parameters for the leak
    leak_node = {}
    leak_diameter = {}
    leak_area = {}
    leak_type = {}
    leak_starts = {}
    leak_ends = {}
    leak_peak_time = {}
    leak_param = {}

    for leak_i in range(0, number_of_leaks):
        # Split pipe and add a leak node
        # leakages: pipeID, startTime, endTime, leakDiameter, leakType (abrupt, incipient)
        leakage_line = leakages[leak_i].split(',')

        # Start time of leak
        ST = time_stamp.get_loc(leakage_line[1])

        # End Time of leak
        ET = time_stamp.get_loc(leakage_line[2])

        # Get leak type
        leak_type[leak_i] = leakage_line[4]

        # Split pipe to add a leak
        pipe_id = wn.get_link(leakage_line[0])
        node_leak = f'{pipe_id}_leaknode'
        wn = wntr.morph.split_pipe(wn, pipe_id, f'{pipe_id}_Bleak', node_leak)
        leak_node[leak_i] = wn.get_node(wn.node_name_list[wn.node_name_list.index(node_leak)])

        if 'incipient' in leak_type[leak_i]:
            # END TIME
            ET = ET + 1
            PT = time_stamp.get_loc(leakage_line[5]) + 1

            # Leak diameter as max magnitude for incipient
            nominal_pres = 100
            leak_diameter[leak_i] = float(leakage_line[3])
            leak_area[leak_i] = 3.14159 * (leak_diameter[leak_i] / 2) ** 2

            # incipient
            leak_param[leak_i] = 'demand'
            increment_leak_diameter = leak_diameter[leak_i] / (PT - ST)
            increment_leak_diameter = np.arange(increment_leak_diameter, leak_diameter[leak_i], increment_leak_diameter)
            increment_leak_area = 0.75 * sqrt(2 / 1000) * 990.27 * 3.14159 * (increment_leak_diameter / 2) ** 2
            leak_magnitude = 0.75 * sqrt(2 / 1000) * 990.27 * leak_area[leak_i]
            pattern_array = [0] * (ST) + increment_leak_area.tolist() + [leak_magnitude] * (ET - PT + 1) + [0] * (
                        TIMESTEPS - ET)

            # basedemand
            leak_node[leak_i].demand_timeseries_list[0]._base = 1
            pattern_name = f'{str(leak_node[leak_i])}'
            wn.add_pattern(pattern_name, pattern_array)
            leak_node[leak_i].demand_timeseries_list[0].pattern_name = pattern_name
            leak_node[leak_i].required_pressure = nominal_pres
            leak_node[leak_i].minimum_pressure = 0

            # save times of leak
            leak_starts[leak_i] = time_stamp[ST]
            leak_starts[leak_i] = leak_starts[leak_i]._date_repr + ' ' + leak_starts[leak_i]._time_repr
            leak_ends[leak_i] = time_stamp[ET - 1]
            leak_ends[leak_i] = leak_ends[leak_i]._date_repr + ' ' + leak_ends[leak_i]._time_repr
            leak_peak_time[leak_i] = time_stamp[PT - 1]._date_repr + ' ' + time_stamp[PT - 1]._time_repr

        else:
            leak_param[leak_i] = 'leak_demand'
            PT = ST
            leak_diameter[leak_i] = float(leakage_line[3])
            leak_area[leak_i] = 3.14159 * (leak_diameter[leak_i] / 2) ** 2

            leak_node[leak_i]._leak_end_control_name = str(leak_i) + 'end'
            leak_node[leak_i]._leak_start_control_name = str(leak_i) + 'start'

            leak_node[leak_i].add_leak(wn, discharge_coeff=0.75,
                                       area=leak_area[leak_i],
                                       start_time=ST * time_step,
                                       end_time=(ET + 1) * time_step)

            leak_starts[leak_i] = time_stamp[ST]
            leak_starts[leak_i] = leak_starts[leak_i]._date_repr + ' ' + leak_starts[leak_i]._time_repr
            leak_ends[leak_i] = time_stamp[ET]
            leak_ends[leak_i] = leak_ends[leak_i]._date_repr + ' ' + leak_ends[leak_i]._time_repr
            leak_peak_time[leak_i] = time_stamp[PT]._date_repr + ' ' + time_stamp[PT]._time_repr

    #wn.write_inpfile('basp/Water/Watergggggg.inp')
    return wn
# wn.write_inpfile('Water_with_leaknodes.inp')

'''
sim = wntr.sim.WNTRSimulator(wn)
results = sim.run_sim()
jsontoexport = {"NodeID": {}, "NodeType": {}, "NodeDemand": {}, "NodeHead": {}, "NodePressure": {},
				"NodeQuality": {}, "LinkID": {}, "LinkType": {}, "LinkFlow": {}, "LinkFriction": {},
				"LinkHeadLoss": {}, "LinkQuality": {}, "LinkReactionRate": {}, "LinkSetting": {}, "LinkStatus": {},
				"LinkVelocity": {}}
x = 0

for value in results.node['demand'].keys():
	if value == 'n215': 
		jsontoexport["NodeID"][str(x)] = value
		jsontoexport["NodeType"][str(x)] = wn.get_node(value).node_type
		dem = results.node['demand'][value]
		dem = [elem * 3600 for elem in dem]
		jsontoexport["NodeDemand"][str(x)] = dem
		jsontoexport["NodePressure"][str(x)] = list(results.node['pressure'][value])
		x += 1

x = 0
for value in wn.link_name_list:
	if value == 'n215': 
		jsontoexport["LinkID"][str(x)] = value
		jsontoexport["LinkType"][str(x)] = wn.get_link(value).link_type
		jsontoexport["LinkFlow"][str(x)] = list(results.link['flowrate'][value])
		flows = results.link['flowrate'][value]
		flows = [elem * 3600 for elem in flows]
		#flows = flows[:len(self.time_stamp)]
		jsontoexport["LinkFlow"][str(x)] = flows
		x += 1
with open('test.json', 'w') as outfile:
	json.dump(jsontoexport, outfile)
'''
