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
   # if step == 10 :
   #     t = traci.route.add('!132', ('24706084#9', '-29121886#4', '-29121886#3', '-29121886#2', '-29121886#1', '-29121886#0', '-166682861#8', '-166682861#7', '-166682861#6', '-166682861#5', '-166682861#4', '-166682861#3', '-166682861#2', '426568352', '-426568355', '348513095', '543574677'))
   #     print (t)
   traci.simulationStep()
   step += 1

traci.close()

# t = traci.route.getIDList () done
# t1 = traci.route.getIDCount() done
# t2 = traci.route.getEdges ('!132') done

# t1 = traci.route.add ('!999', (
# '24706084#9', '-29121886#4', '-29121886#3', '-29121886#2', '-29121886#1', '-29121886#0', '-166682861#8', '-166682861#7',
# '-166682861#6', '-166682861#5', '-166682861#4', '-166682861#3', '-166682861#2', '426568352', '-426568355', '348513095',
# '543574677'))

