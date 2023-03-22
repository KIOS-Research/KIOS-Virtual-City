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

while step < 50:
   traci.simulationStep()
   step += 1
   t1 = traci.trafficlight.getIDList()
   print(t1)

   # print (t1)

traci.close()
# t = traci.trafficlight.getIDList() done
# t1 = traci.trafficlight.getIDCount() done
# t2 = traci.trafficlight.getRedYellowGreenState('50000') done
# t3 = traci.trafficlight.getPhaseDuration('50000') done
# t4 = traci.trafficlight.getControlledLinks('50000')
# t5 = traci.trafficlight.getControlledLanes('50000')
# t6 = traci.trafficlight.getPhase ('50001') done
# t7 = traci.trafficlight.getProgram ('50000')
# t8 = traci.trafficlight.getAllProgramLogics('50000')
# t9 = traci.trafficlight.getNextSwitch ('50000')
# t10 = traci.trafficlight.getBlockingVehicles('50000',0)
# t11 = traci.trafficlight.getRivalVehicles('50000',4)
# t12 = traci.trafficlight.getPriorityVehicles('50000',1)

# t1 = traci.trafficlight.setRedYellowGreenState ('50000', 'rryyG') done
# t2 = traci.trafficlight.setLinkState ('50000', 1, 'rryyG') done
# t3 = traci.trafficlight.setPhase ('50000', 1) done
# t4 = traci.trafficlight.setProgram ('50000','programname') ???????
# t5 = traci.trafficlight.setPhaseDuration ('50000', 0.25) done
# t6 = traci.trafficlight.setProgramLogic('50000','Logic') ?????

