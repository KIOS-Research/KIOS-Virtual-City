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


def countVehicles():
    return traci.vehicle.getIDCount()


def listVehicles():
    return traci.vehicle.getIDList()


def vehicleSpeed(vehID):
    return traci.vehicle.getSpeed(vehID)


def vehicleLateralSpeed(vehID):
    return traci.vehicle.getLateralSpeed(vehID)


def vehicleAcceleration(vehID):
    return traci.vehicle.getAcceleration(vehID)

def vehiclePosition(vehID):
    return traci.vehicle.getPosition(vehID)


def vehiclePosition3D(vehID):
    return traci.vehicle.getPosition3D(vehID)


def vehicleAngle(vehID):
    return traci.vehicle.getAngle(vehID)


def vehicleRoadID(vehID):
    return traci.vehicle.getRoadID(vehID)


def vehicleLaneID(vehID):
    return traci.vehicle.getLaneID(vehID)


def vehicleLaneIndex(vehID):
    return traci.vehicle.getLaneIndex(vehID)


def vehicleTypeID(vehID):
    return traci.vehicle.getTypeID(vehID)


def vehicleRouteID(vehID):
    return traci.vehicle.getRouteID(vehID)


def vehicleRouteIndex(vehID):
    return traci.vehicle.getRouteIndex(vehID)


def vehicleRoute(vehID):
    return traci.vehicle.getRoute(vehID)


def vehicleColor(vehID):
    return traci.vehicle.getColor(vehID)


def vehicleLanePosition(vehID):
    return traci.vehicle.getLanePosition(vehID)


def vehicleDistance(vehID):
    return traci.vehicle.getDistance(vehID)


def vehicleSignals(vehID):
    return traci.vehicle.getSignals(vehID)


def vehicleRoutingMode(vehID):
    return traci.vehicle.getRoutingMode(vehID)


def vehicleTaxiFleet(flag):
    # 0: empty
    # 1: pickup
    # 2: occupied
    return traci.vehicle.getTaxiFleet(flag)


def vehicleCO2Emission(vehID):
    return traci.vehicle.getCO2Emission(vehID)


def vehicleCOEmission(vehID):
    return traci.vehicle.getCOEmission(vehID)


def vehicleHCEmission(vehID):
    return traci.vehicle.getHCEmission(vehID)


def vehiclePMxEmission(vehID):
    return traci.vehicle.getPMxEmission(vehID)


def vehicleNOxEmission(vehID):
    return traci.vehicle.getNOxEmission(vehID)


def vehicleFuelConsumption(vehID):
    return traci.vehicle.getFuelConsumption(vehID)


def vehicleNoiseEmission(vehID):
    return traci.vehicle.getNoiseEmission(vehID)


def vehicleElectricityConsumption(vehID):
    return traci.vehicle.getElectricityConsumption(vehID)


def vehicleBestLanes(vehID):
    return traci.vehicle.getBestLanes(vehID)


def vehicleStopState(vehID):
    return traci.vehicle.getStopState(vehID)


def vehicleIsAtBusStop(vehID):
    return traci.vehicle.isAtBusStop(vehID)


def vehicleIsAtContainerStop(vehID):
    return traci.vehicle.isAtContainerStop(vehID)


def vehicleIsStopped(vehID):
    return traci.vehicle.isStopped(vehID)


def vehicleIsStoppedParking(vehID):
    return traci.vehicle.isStoppedParking(vehID)


def vehicleIsStoppedTriggered(vehID):
    return traci.vehicle.isStoppedTriggered(vehID)


def vehicleLength(vehID):
    return traci.vehicle.getLength(vehID)


def vehicleMaxSpeed(vehID):
    return traci.vehicle.getMaxSpeed(vehID)


def vehicleAccel(vehID):
    return traci.vehicle.getAccel(vehID)


def vehicleDecel(vehID):
    return traci.vehicle.getDecel(vehID)

def vehicleTau(vehID):
    return traci.vehicle.getTau(vehID)


def vehicleImperfection(vehID):
    return traci.vehicle.getImperfection(vehID)


def vehicleSpeedFactor(vehID):
    return traci.vehicle.getSpeedFactor(vehID)


def vehicleSpeedDeviation(vehID):
    return traci.vehicle.getSpeedDeviation(vehID)


def vehicleVehicleClass(vehID):
    return traci.vehicle.getVehicleClass(vehID)


def vehicleEmissionClass(vehID):
    return traci.vehicle.getEmissionClass(vehID)


def vehicleShapeClass(vehID):
    return traci.vehicle.getShapeClass(vehID)


def vehicleMinGap(vehID):
    return traci.vehicle.getMinGap(vehID)


def vehicleWidth(vehID):
    return traci.vehicle.getWidth(vehID)


def vehicleHeight(vehID):
    return traci.vehicle.getHeight(vehID)


def vehiclePersonCapacity(vehID):
    return traci.vehicle.getPersonCapacity(vehID)


def vehicleWaitingTime(vehID):
    return traci.vehicle.getWaitingTime(vehID)


def vehicleAccumulatedWaitingTime(vehID):
    return traci.vehicle.getAccumulatedWaitingTime(vehID)


def vehicleNextTLS(vehID):
    return traci.vehicle.getNextTLS(vehID)


def vehicleNextStops(vehID):
    return traci.vehicle.getNextStops(vehID)


def vehiclePersonIDList(vehID):
    return traci.vehicle.getPersonIDList(vehID)


def vehicleSpeedMode(vehID):
    return traci.vehicle.getSpeedMode(vehID)


def vehicleLaneChangeMode(vehID):
    return traci.vehicle.getLaneChangeMode(vehID)


def vehicleSlope(vehID):
    return traci.vehicle.getSlope(vehID)


def vehicleAllowedSpeed(vehID):
    return traci.vehicle.getAllowedSpeed(vehID)


def vehicleLine(vehID):
    return traci.vehicle.getLine(vehID)


def vehiclePersonNumber(vehID):
    return traci.vehicle.getPersonNumber(vehID)


def vehicleVia(vehID):
    return traci.vehicle.getVia(vehID)


def vehicleSpeedWithoutTraCI(vehID):
    return traci.vehicle.getSpeedWithoutTraCI(vehID)


def vehicleIsRouteValid(vehID):
    return traci.vehicle.isRouteValid(vehID)


def vehicleLateralLanePosition(vehID):
    return traci.vehicle.getLateralLanePosition(vehID)


def vehicleMaxSpeedLat(vehID):
    return traci.vehicle.getMaxSpeedLat(vehID)


def vehicleMinGapLat(vehID):
    return traci.vehicle.getMinGapLat(vehID)


def vehicleLateralAlignment(vehID):
    return traci.vehicle.getLateralAlignment(vehID)


def vehicleParameter(objID, param):
    return traci.vehicle.getParameter(objID, param)


def vehicleActionStepLength(vehID):
    return traci.vehicle.getActionStepLength(vehID)


def vehicleLastActionTime(vehID):
    return traci.vehicle.getLastActionTime(vehID)

# Extended--------------------------------------------------------
def vehicleAdaptedTraveltime(vehID, time, edgeID):
    return traci.vehicle.getAdaptedTraveltime(vehID, time, edgeID)


def vehicleEffort(vehID, time, edgeID):
    return traci.vehicle.getEffort(vehID, time, edgeID)


def vehicleDrivingDistance(vehID, edgeID, pos, laneIndex=0):
    return traci.vehicle.getDrivingDistance(vehID, edgeID, pos, laneIndex)


def vehicleDrivingDistance2D(vehID, x, y):
    return traci.vehicle.getDrivingDistance2D(vehID, x, y)


def vehicleLaneChangeState(vehID, direction):
    return traci.vehicle.getLaneChangeState(vehID, direction)


def vehicleCouldChangeLane(vehID, direction, state=None):
    return traci.vehicle.couldChangeLane(vehID, direction, state)


def vehicleWantsAndCouldChangeLane(vehID, direction, state=None):
    return traci.vehicle.wantsAndCouldChangeLane(vehID, direction, state)

def vehicleNeighbors(vehID, mode):
    return traci.vehicle.getNeighbors(vehID, mode)


def vehicleLeftFollowers(vehID, blockingOnly=False):
    return traci.vehicle.getLeftFollowers(vehID, blockingOnly)


def vehicleLeftLeaders(vehID, blockingOnly=False):
    return traci.vehicle.getLeftLeaders(vehID, blockingOnly)


def vehicleRightFollowers(vehID, blockingOnly=False):
    return traci.vehicle.getRightFollowers(vehID, blockingOnly)


def vehicleRightLeaders(vehID, blockingOnly=False):
    return traci.vehicle.getRightLeaders(vehID, blockingOnly)

def vehicleFollowSpeed(vehID, speed, gap, leaderSpeed, leaderMaxDecel, leaderID=''):
    return traci.vehicle.getFollowSpeed(vehID, speed, gap, leaderSpeed, leaderMaxDecel, leaderID)


def vehicleSecureGap(vehID, speed, leaderSpeed, leaderMaxDecel, leaderID=''):
    return traci.vehicle.getSecureGap(vehID, speed, leaderSpeed, leaderMaxDecel, leaderID)


def vehicleStopSpeed(vehID, speed, gap):
    return traci.vehicle.getStopSpeed(vehID, speed, gap)

traci.start(sumoCmd)
step = 0
while step < 100:
    traci.simulationStep()

    if step == 80:
        print("STEP: ", step)
        print(vehicleStopSpeed(listVehicles()[0],100,10))
        print(vehicleLeftFollowers(listVehicles()[0]))
        print(vehicleLeftLeaders(listVehicles()[0]))
        print(vehicleNeighbors(listVehicles()[0],0))

        print(vehicleCouldChangeLane(listVehicles()[0],-1))
    if step == 80:
        print("STEP: ", step)
        print(vehicleLaneID(listVehicles()[0]))
        print(vehicleLaneIndex(listVehicles()[0]))
        print(vehicleTypeID(listVehicles()[0]))
        print(vehicleRouteID(listVehicles()[0]))
        print(vehicleRouteIndex(listVehicles()[0]))
        print(vehicleRoute(listVehicles()[0]))
        print(vehicleColor(listVehicles()[0]))
        print(vehicleLanePosition(listVehicles()[0]))
        print(vehicleDistance(listVehicles()[0]))
        print(vehicleSignals(listVehicles()[0]))
        print(vehicleRoutingMode(listVehicles()[0]))
        print(vehicleCO2Emission(listVehicles()[0]))
        print(vehicleCOEmission(listVehicles()[0]))
        print(vehicleHCEmission(listVehicles()[0]))
        print(vehiclePMxEmission(listVehicles()[0]))
        print(vehicleNOxEmission(listVehicles()[0]))
        print(vehicleFuelConsumption(listVehicles()[0]))
        print(vehicleNoiseEmission(listVehicles()[0]))
        print(vehicleElectricityConsumption(listVehicles()[0]))
        print(vehicleBestLanes(listVehicles()[0]))
        print(vehicleStopState(listVehicles()[0]))
        print(vehicleIsAtBusStop(listVehicles()[0]))
        print(vehicleIsAtContainerStop(listVehicles()[0]))
        print(vehicleIsStopped(listVehicles()[0]))
        print(vehicleIsStoppedParking(listVehicles()[0]))
        print(vehicleIsStoppedTriggered(listVehicles()[0]))
        print(vehicleLength(listVehicles()[0]))
        print(vehicleMaxSpeed(listVehicles()[0]))
        print(vehicleAccel(listVehicles()[0]))
        print(vehicleDecel(listVehicles()[0]))
        print(vehicleTau(listVehicles()[0]))
        print(vehicleImperfection(listVehicles()[0]))
        print(vehicleSpeedFactor(listVehicles()[0]))
        print(vehicleSpeedDeviation(listVehicles()[0]))
        print(vehicleVehicleClass(listVehicles()[0]))
        print(vehicleEmissionClass(listVehicles()[0]))
        print(vehicleShapeClass(listVehicles()[0]))
        print(vehicleMinGap(listVehicles()[0]))
        print(vehicleWidth(listVehicles()[0]))
        print(vehicleHeight(listVehicles()[0]))
        print(vehiclePersonCapacity(listVehicles()[0]))
        print(vehicleWaitingTime(listVehicles()[0]))
        print(vehicleAccumulatedWaitingTime(listVehicles()[0]))
        print(vehicleNextTLS(listVehicles()[0]))
        print(vehicleNextStops(listVehicles()[0]))
        print(vehiclePersonIDList(listVehicles()[0]))
        print(vehicleSpeedMode(listVehicles()[0]))
        print(vehicleLaneChangeMode(listVehicles()[0]))
        print(vehicleSlope(listVehicles()[0]))
        print(vehicleAllowedSpeed(listVehicles()[0]))
        print(vehicleLine(listVehicles()[0]))
        print(vehiclePersonNumber(listVehicles()[0]))
        print(vehicleVia(listVehicles()[0]))
        print(vehicleSpeedWithoutTraCI(listVehicles()[0]))
        print(vehicleIsRouteValid(listVehicles()[0]))
        print(vehicleLateralLanePosition(listVehicles()[0]))
        print(vehicleMaxSpeedLat(listVehicles()[0]))
        print(vehicleMinGapLat(listVehicles()[0]))
        print(vehicleLateralAlignment(listVehicles()[0]))
        print(vehicleActionStepLength(listVehicles()[0]))
        print(vehicleLastActionTime(listVehicles()[0]))
        print(vehicleTaxiFleet(2))
        print(vehicleParameter(listVehicles()[0],"buffer_stop"))

    step += 1

traci.close()
