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
        print("STEP: ", step)
        # traci.vehicle.setStop(vehID="1000000000", edgeID="29149366#1", pos=1.0, laneIndex=0, duration=-1073741824.0, flags=0, startPos=-1073741824.0, until=-1073741824.0)
        # traci.vehicle.setBusStop(vehID="?????", stopID="?????", duration=-1073741824.0, until=-1073741824.0, flags=0)
        # traci.vehicle.setContainerStop(vehID="????", stopID="?????", duration=-1073741824.0, until=-1073741824.0, flags=0)
        # traci.vehicle.setChargingStationStop(vehID="1000000000", stopID="?????", duration=-1073741824.0, until=-1073741824.0,flags=0)
        # traci.vehicle.setParkingAreaStop(vehID="1000000000", stopID="???????", duration=-1073741824.0, until=-1073741824.0, flags=1)
        # traci.vehicle.changeLane(vehID="1000000000", laneIndex=0, duration=10)
        # traci.vehicle.changeSublane(vehID="1000000000", latDist=-1)
        # traci.vehicle.slowDown(vehID="1000000000", speed=10, duration=10)
        # traci.vehicle.resume(vehID="1000000000")
        # traci.vehicle.changeTarget(vehID="1000000000", edgeID="-111429737#1")
        # traci.vehicle.setSpeed(vehID="1000000000", speed=10)
        # traci.vehicle.setColor(vehID="1000000000", color=(255,0,0,0))
        # traci.vehicle.setRouteID(vehID="1000000000", routeID="?????")
        # traci.vehicle.setRoute(vehID="1000000000", edgeList=['???','?????','?????'])
        # traci.vehicle.rerouteParkingArea(vehID="1000000000", parkingAreaID="????")
        # traci.vehicle.dispatchTaxi(vehID="????", reservations=['???','????','????','????'])
        # traci.vehicle.setAdaptedTraveltime(vehID="1000000000", edgeID="-111429737#1", time=None, begTime=None, endTime=None)
        # traci.vehicle.setEffort(vehID="1000000000", edgeID="-111429737#1", effort=None, begTime=None, endTime=None)
        # traci.vehicle.setSignals(vehID="1000000000", signals=1)
        # traci.vehicle.setRoutingMode(vehID="1000000000", routingMode=1)
        # traci.vehicle.moveTo(vehID="1000000000", laneID="??????", pos=1, reason=0)
        # traci.vehicle.moveToXY(vehID="1000000000", edgeID="-111429737#1", lane=0, x=2, y=1, angle=-1073741824.0, keepRoute=1)
        # traci.vehicle.replaceStop(vehID="1000000000", nextStopIndex=0, edgeID="-111429737#1", pos=1.0, laneIndex=0, duration=-1073741824.0, flags=0, startPos=-1073741824.0, until=-1073741824.0)
        # traci.vehicle.rerouteTraveltime(vehID="1000000000", currentTravelTimes=False)
        # traci.vehicle.rerouteEffort(vehID="1000000000")
        # traci.vehicle.setSpeedMode(vehID="1000000000", sm=1)
        # traci.vehicle.setSpeedFactor(vehID="1000000000", factor=1)
        # traci.vehicle.setMaxSpeed(vehID="1000000000", speed=100)
        # traci.vehicle.setLaneChangeMode(vehID="1000000000", lcm=1)
        # traci.vehicle.updateBestLanes(vehID="1000000000")
        # traci.vehicle.add(vehID="111111", routeID="????", typeID='DEFAULT_VEHTYPE', depart=None, departLane='first', departPos='base', departSpeed='0', arrivalLane='current', arrivalPos='max', arrivalSpeed='current', fromTaz='', toTaz='', line='', personCapacity=0, personNumber=0)
        # traci.vehicle.addLegacy(vehID="111111", routeID="??????", depart=-3, pos=0, speed=0, lane=-6, typeID='DEFAULT_VEHTYPE')
        # traci.vehicle.remove(vehID="1000000000", reason=3)
        # traci.vehicle.setLength(vehID="1000000000", length=5)
        # traci.vehicle.setVehicleClass(vehID="1000000000", clazz="test")
        # traci.vehicle.setEmissionClass(vehID="1000000000", clazz="test")
        # traci.vehicle.setWidth(vehID="1000000000", width=5)
        # traci.vehicle.setHeight(vehID="1000000000", height=5)
        # traci.vehicle.setMinGap(vehID="1000000000", minGap=5)
        # traci.vehicle.setShapeClass(vehID="1000000000", clazz="test")
        # traci.vehicle.setAccel(vehID="1000000000", accel=20)
        # traci.vehicle.setDecel(vehID="1000000000", decel=20)
        # traci.vehicle.setImperfection(vehID="1000000000", imperfection=5)
        # traci.vehicle.setTau(vehID="1000000000", tau=5)
        # traci.vehicle.setType(vehID="1000000000", typeID="test")
        # traci.vehicle.setVia(vehID="1000000000", edgeList=['111349534#0','111349534#1','111349534#2'])
        # traci.vehicle.setMaxSpeedLat(vehID="1000000000", speed=10)
        # traci.vehicle.setMinGapLat(vehID="1000000000", minGapLat=10)
        # traci.vehicle.setLateralAlignment(vehID="1000000000", align="????")
        # traci.vehicle.setParameter(objID="1000000000", param="buffer_stop", value="true")
        # traci.vehicle.setActionStepLength(vehID="1000000000", actionStepLength=2, resetActionOffset=True) !!!!!!!!!step-method.ballistic was not set
        traci.vehicle.highlight(vehID="1000000000", color=(255, 0, 0, 255), size=-1, alphaMax=-1, duration=-1, type=0)
    step += 1

traci.close()
