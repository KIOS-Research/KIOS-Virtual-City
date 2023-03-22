import os, sys


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    tools = os.path.join("/usr/bin/sumo/", 'tools')
    sys.path.append(tools)

sumoBinary = "/usr/bin/sumo"
sumoCmd = [sumoBinary, "-c", "lim.sumocfg"]


import traci
traci.start(sumoCmd)
step = 0
while step < 100:
    traci.simulationStep()
    if step == 99:
        traci.vehicle.highlight(vehID="1000000000", color=(255, 0, 0, 255), size=-1, alphaMax=-1, duration=-1, type=0)
    step += 1

traci.close()
