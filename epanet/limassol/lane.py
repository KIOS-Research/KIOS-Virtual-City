import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    tools = os.path.join("/usr/bin/sumo/", 'tools')
    sys.path.append(tools)

sumoBinary = "/usr/bin/sumo"
sumoCmd = [sumoBinary, "-c", "lim.sumocfg"]
# export SUMO_HOME="/usr/bin/sumo/"
import traci
traci.start(sumoCmd)
step = 0
# t1 = traci.lane.getFoes(":1212820385_3_0",":1212820385_6_0")
# print(t1)
t1 = traci.lane.setMaxSpeed(":1212820385_3_0",8.6)
t8 = traci.lane.getMaxSpeed(":1212820385_3_0")
print (t8)
while step < 150:
    traci.simulationStep ()
    step += 1
    # t = traci.lane.getDisallowed(":1212820385_3_0")
    # print (t)

traci.close ()

# t1 = traci.lane.getIDList() done
# t2 = traci.lane.getIDCount() done
# t3 = traci.lane.getLinkNumber('gneE11_0')
# t4 = traci.lane.getEdgeID('gneE11_0')
# t5 = traci.lane.getLinks('gneE11_0')
# t6 = traci.lane.getAllowed('gneE11_0')
# t7 = traci.lane.getDisallowed('gneE11_0')
# t8 = traci.lane.getLength('gneE11_0') done
# t9 = traci.lane.getMaxSpeed('gneE11_0') done
# t10 = traci.lane.getShape('gneE11_0')
# t11 = traci.lane.getWidth('gneE11_0')
# t12 = traci.lane.getCO2Emission('gneE11_0') done
# t13 = traci.lane.getCOEmission('gneE11_0') done
# t14 = traci.lane.getHCEmission('gneE11_0') done
# t15 = traci.lane.getPMxEmission('gneE11_0') done
# t16 = traci.lane.getNOxEmission ('gneE11_0') done
# t17 = traci.lane.getFuelConsumption ('gneE11_0') done
# t18 = traci.lane.getNoiseEmission ('gneE11_0') done
# t19 = traci.lane.getElectricityConsumption ('gneE11_0')
# t20 = traci.lane.getLastStepVehicleNumber ('gneE11_0')
# t21 = traci.lane.getLastStepMeanSpeed ('gneE11_0')
# t22 = traci.lane.getLastStepVehicleIDs ('gneE11_0')
# t23 = traci.lane.getLastStepOccupancy ('gneE11_0')
# t24 = traci.lane.getLastStepLength ('gneE11_0')
# t25 = traci.lane.getWaitingTime ('gneE11_0') ##  argument: 'laneID' not getWaitingTime ()
# t26 = traci.lane.getTraveltime ('gneE11_0')
# t27 = traci.lane.getLastStepHaltingNumber ('gneE11_0')
# t28 = traci.lane.getFoes(":1212820385_3_0",":1212820385_6_0")

# t1 = traci.lane.setAllowed(":1212820385_3_0",['tram', 'rail_urban', 'rail']) done
# t2 = traci.lane.setDisallowed(":1212820385_3_0",['tram', 'rail_urban', 'rail']) done
# t3 = traci.lane.setLength(":1212820385_3_0",15.6) done
# t4 = traci.lane.setMaxSpeed(":1212820385_3_0",8.6) done
