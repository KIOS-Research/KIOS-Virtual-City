from . import models
from rest_framework import serializers


class WaterDeleteDBViewSet(serializers.Serializer):
    """Serializes field and value"""
    experimentname = serializers.CharField(max_length=None, required=True)


class WaterBackdropSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=400, required=False)


class WaterControlsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=400, required=False)
    actions = serializers.CharField(max_length=1000, required=False)
    condition = serializers.CharField(max_length=1000, required=False)


class WaterCoordinatesSerializer(serializers.Serializer):
    node = serializers.CharField(max_length=200, required=False)
    xcoord = serializers.FloatField(required=False)
    ycoord = serializers.FloatField(required=False)


class WaterCurvesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=True)
    curve_type = serializers.ChoiceField(choices=['PUMP', 'EFFICIENCY', 'VOLUME', 'HEADLOSS'])
    xcoord = serializers.FloatField(required=True)
    ycoord = serializers.FloatField(required=True)


class WaterEmittersSerializer(serializers.Serializer):
    flow_coefficient = serializers.FloatField(required=True)


class WaterEnergySerializer(serializers.Serializer):
    value = serializers.CharField(max_length=200, required=True)


class WaterJunctionsSerializer(serializers.Serializer):
    junction_name = serializers.CharField(max_length=200, required=True)
    base_demand = serializers.FloatField(required=False)
    demand_pattern = serializers.CharField(max_length=200, required=False)
    elevation = serializers.FloatField(required=False)


class WaterMixingSerializer(serializers.Serializer):
    mixing_model = serializers.ChoiceField(choices=['MIXED', '2COMP', 'FIFO', 'LIFO'])
    mixing_fraction = serializers.FloatField(required=False)


class WaterOptionsSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=200, required=False)


class WaterPipesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=True)
    start_node_name = serializers.CharField(max_length=200, required=True)
    end_node_name = serializers.CharField(max_length=200, required=True)
    length = serializers.FloatField(required=False)
    diameter = serializers.FloatField(required=False)
    roughness = serializers.FloatField(required=False)
    minor_loss = serializers.FloatField(required=False)
    status = serializers.ChoiceField(choices=['Open', 'Closed'])
    check_valve_flag = serializers.ChoiceField(choices=['True', 'False'])


class WaterPumpsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=True)
    start_node_name = serializers.CharField(max_length=200, required=True)
    end_node_name = serializers.CharField(max_length=200, required=True)
    pump_type = serializers.ChoiceField(choices=['POWER', 'HEAD'])
    pump_parameter = serializers.CharField(max_length=200, required=True)
    speed = serializers.FloatField(required=True)
    pattern = serializers.CharField(max_length=200, required=True)


class WaterReactionsSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=200, required=True)


class WaterReportSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=200, required=True)


class WaterReservoirsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=True)
    base_head = serializers.FloatField(required=False)
    head_pattern = serializers.CharField(max_length=200, required=True)
    xcoord = serializers.FloatField(required=False)
    ycoord = serializers.FloatField(required=False)


class WaterSourcesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=True)
    node_name = serializers.CharField(max_length=200, required=True)
    source_type = serializers.CharField(max_length=200, required=True)
    quality = serializers.FloatField(required=True)
    pattern = serializers.CharField(max_length=200, required=True)


class WaterTanksSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=True)
    elevation = serializers.FloatField(required=True)
    init_level = serializers.FloatField(required=True)
    min_level = serializers.FloatField(required=True)
    max_level = serializers.FloatField(required=True)
    diameter = serializers.FloatField(required=True)
    min_vol = serializers.FloatField(required=True)
    vol_curve = serializers.CharField(max_length=200, required=False)
    overflow = serializers.ChoiceField(choices=['True', 'False'])
    xcoord = serializers.FloatField(required=False)
    ycoord = serializers.FloatField(required=False)


class WaterValvesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=True)
    start_node_name = serializers.CharField(max_length=200, required=True)
    end_node_name = serializers.CharField(max_length=200, required=True)
    diameter = serializers.FloatField(required=False)
    valve_type = serializers.CharField(max_length=200, required=False)
    minor_loss = serializers.FloatField(required=False)
    setting = serializers.CharField(max_length=200, required=False)


class WaterTimesSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=200, required=True)


class WaterSerializer(serializers.Serializer):
    """Serializes field and value"""
    # field = serializers.CharField(max_length=300)
    # value = serializers.CharField(max_length=300)


class WaterLeakSerializer(serializers.Serializer):
    # file = serializers.FileField()
    file = serializers.CharField(max_length=20000000)
    # area = serializers.FloatField()
    # start_time = serializers.FloatField()
    # end_time = serializers.FloatField()

class WaterEarthquakeSerializer(serializers.Serializer):
    epicenterx = serializers.FloatField(required=True)
    epicentery = serializers.FloatField(required=True)
    magnitude = serializers.FloatField(required=True)
    depth = serializers.FloatField(required=True)

class WaterPowerOutageSerializer(serializers.Serializer):
    link = serializers.CharField(max_length = 500)
    start_time = serializers.IntegerField(required = True)
    end_time = serializers.IntegerField(required = True)

class WaterClearDataSerializer(serializers.Serializer):
    """Clears water data"""
    clear = serializers.CharField(max_length=200, required=False)


class WaterLoadSerializer(serializers.Serializer):
    """Serializes field and value"""
    file = serializers.CharField(max_length=200, required=False)
    inp = serializers.FileField(required=False)


class WaterStartSerializer(serializers.Serializer):
    """Serializes field and value"""
    startdate = serializers.DateField()
    enddate = serializers.DateField()
    experimentname = serializers.CharField(max_length=200, required=False)
    sensors = serializers.CharField(max_length=None, required=True)


class WaterStartSerializerWNTR(serializers.Serializer):
    """Serializes field and value"""
    startdate = serializers.DateField()
    enddate = serializers.DateField()
    experimentname = serializers.CharField(max_length=200, required=False)
    leakages = serializers.CharField(max_length=None, required=False, allow_blank=True)
    sensors = serializers.CharField(max_length=None, required=True)


class WaterStepExecutionSerializer(serializers.Serializer):
    """Serializes field and value"""
    startdate = serializers.DateField(required=True)
    timestep = serializers.IntegerField(required=True)
    iterations = serializers.IntegerField(required=True)
    timestep_size = serializers.IntegerField(required=True)
    experiment_name = serializers.CharField(max_length=200, required=True)
    sensors = serializers.CharField(max_length=None, required=True)


class WaterDemandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterDemands
        fields = ['id', 'junction', 'demand', 'pattern', 'category']


class WaterOutputLinksSerializer(serializers.Serializer):
    links = serializers.CharField(max_length=400, required=False)
    fields = serializers.CharField(max_length=400, required=False)
    resolution = serializers.FloatField(max_value=1.0, min_value=0.0, required=False)
    drop = serializers.IntegerField(max_value=100, min_value=0, required=False)

    '''
    class Meta:
        model = models.WaterOutputLinksValues
        fields = ['linkid', 'readingtime', 'linkfriction', 'linkheadloss', 'linkquality', 'linkreactionrate', 'linksetting', 'linkstatus', 'linkvelocity']
    '''


class WaterOutputNodesSerializer(serializers.Serializer):
    nodes = serializers.CharField(max_length=400, required=False)
    fields = serializers.CharField(max_length=400, required=False)
    resolution = serializers.FloatField(max_value=1.0, min_value=0.0, required=False)
    drop = serializers.IntegerField(max_value=100, min_value=0, required=False)
    '''
    class Meta:
        model = models.WaterOutputNodesValues
        fields = ['nodeid', 'readingtime', 'nodedemand', 'nodehead', 'nodepressure', 'nodequality']
    '''


class WaterOutputSensorsValuesSerializer(serializers.Serializer):
    experimentname = serializers.CharField(max_length=400, required=True)
    sensorid = serializers.CharField(max_length=400, required=False)


class WaterOutputJSONSerializer(serializers.Serializer):
    experimentname = serializers.CharField(max_length=400, required=True)


class PowerSubstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PowerSubstations
        fields = ['linkid', 'readingtime', 'linkfriction', 'linkheadloss', 'linkquality', 'linkreactionrate',
                  'linksetting', 'linkstatus', 'linkvelocity']


class PowerTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PowerTimes
        fields = ['nodeid', 'readingtime', 'nodedemand', 'nodehead', 'nodepressure', 'nodequality']


class PowerOutputVoltagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PowerOutputVoltages
        fields = ['nodeid', 'readingtime', 'nodedemand', 'nodehead', 'nodepressure', 'nodequality']


class TransportationLaneGetSerializer(serializers.Serializer):
    """"""
    laneID = serializers.CharField(max_length=200, required=True)


class TransportationTrafficlightGetSerializer(serializers.Serializer):
    """"""
    tlsID = serializers.CharField(max_length=200, required=True)


class TransportationTrafficlightSetRedYellowGreenStateSerializer(serializers.Serializer):
    """"""
    tlsID = serializers.CharField(max_length=200, required=True)
    state = serializers.CharField(max_length=200, required=True)


class TransportationTrafficlightSetLinkStateSerializer(serializers.Serializer):
    """"""
    tlsID = serializers.CharField(max_length=200, required=True)
    tlsLinkIndex = serializers.IntegerField(required=True)
    state = serializers.CharField(max_length=200, required=True)


class TransportationTrafficlightSetPhaseSerializer(serializers.Serializer):
    """"""
    tlsID = serializers.CharField(max_length=200, required=True)
    index = serializers.IntegerField(required=True)


class TransportationTrafficlightSetPhaseDurationSerializer(serializers.Serializer):
    """"""
    tlsID = serializers.CharField(max_length=200, required=True)
    phaseDuration = serializers.FloatField(min_value=0, required=True)


class TransportationVehicleGetIDCountSerializer(serializers.Serializer):
    """"""


class TransportationVehicleGetIDListSerializer(serializers.Serializer):
    """"""


class TransportationVehicleGetSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)


class TransportationVehicleStateSetStopSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    edgeID = serializers.CharField(max_length=200, required=True)
    pos = serializers.FloatField(default=1.0)
    laneIndex = serializers.IntegerField(default=0)
    duration = serializers.FloatField(default=1073741824.0)
    flags = serializers.IntegerField(default=0)
    startPos = serializers.FloatField(default=-1073741824.0)
    until = serializers.FloatField(default=-1073741824.0)

class TransportationVehicleStateSetBusStopSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    stopID = serializers.CharField(max_length=200, required=True)
    duration = serializers.FloatField(default=1073741824.0)
    until = serializers.FloatField(default=-1073741824.0)
    flags = serializers.IntegerField(default=0)

class TransportationVehicleStateSetContainerStopSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    stopID = serializers.CharField(max_length=200, required=True)
    duration = serializers.FloatField(default=1073741824.0)
    until = serializers.FloatField(default=-1073741824.0)
    flags = serializers.IntegerField(default=0)

class TransportationVehicleStateSetChargingStopSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    stopID = serializers.CharField(max_length=200, required=True)
    duration = serializers.FloatField(default=1073741824.0)
    until = serializers.FloatField(default=-1073741824.0)
    flags = serializers.IntegerField(default=0)

class TransportationVehicleStateSetParkingAreaStopSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    stopID = serializers.CharField(max_length=200, required=True)
    duration = serializers.FloatField(default=1073741824.0)
    until = serializers.FloatField(default=-1073741824.0)
    flags = serializers.IntegerField(default=0)

class TransportationVehicleStateChangeTargetSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    edgeID = serializers.CharField(max_length=200, required=True)

class TransportationVehicleStateSetColorSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    color = serializers.CharField(max_length=200, required=True)

class TransportationVehicleStateDispatchTaxiSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    reservations = serializers.CharField(max_length=200, required=True)

class TransportationVehicleStateSetRouteIdSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    routeID = serializers.CharField(max_length=200, required=True)

class TransportationVehicleStateSetRouteSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    route = serializers.CharField(max_length=500, required=True)

class TransportationVehicleRerouteParkingAreaSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    parkingAreaID = serializers.CharField(max_length=500, required=True)

class TransportationVehicleStatesetAdaptedTraveltimeSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    edgeID = serializers.CharField(max_length=200, required=True)
    time = serializers.FloatField(default=None, required = False)
    begTime = serializers.FloatField(default=None, required = False)
    endTime = serializers.FloatField(default=None, required = False)

class TransportationVehicleStateSetEffortSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    edgeID = serializers.CharField(max_length=200, required=True)
    effort = serializers.FloatField(default=None, required = False)
    begTime = serializers.FloatField(default=None, required = False)
    endTime = serializers.FloatField(default=None, required = False)

class TransportationVehicleStatesetSignalsSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    signals = serializers.IntegerField(required = True)

class TransportationVehicleStatesetRoutingModeSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    routingMode = serializers.IntegerField(required = True)

class TransportationVehicleStateMoveToSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)
    laneID = serializers.CharField(max_length=200, required=True)
    pos = serializers.FloatField(required = True)
    reason = serializers.IntegerField(required = False, default = 0)

class TransportationVehicleStateResumeSerializer(serializers.Serializer):
    vehID = serializers.CharField(max_length=200, required=True)


class TransportationVehicleStateChangeLaneSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    laneIndex = serializers.IntegerField()
    duration = serializers.FloatField()


class TransportationVehicleStateChangeSubLaneSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    latDist = serializers.FloatField()


class TransportationVehicleStateSlowDownSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    speed = serializers.FloatField()
    duration = serializers.FloatField()


class TransportationVehicleStateSetSpeedSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    speed = serializers.FloatField()


class TransportationVehicleStateMoveToSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    laneID = serializers.CharField(max_length=200, required=True)
    pos = serializers.FloatField()
    reason = serializers.IntegerField(default=0)

class TransportationVehicleStateMoveToXYSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    edgeID = serializers.CharField(max_length=200, required=True)
    lane = serializers.CharField(max_length=200, required=True)
    x = serializers.FloatField()
    y = serializers.FloatField()
    angle = serializers.FloatField(default=-1073741824.0)
    keepRoute = serializers.IntegerField(default=1)
    matchThreshold = serializers.IntegerField(default=100)

class TransportationVehicleStatereplaceStopSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    nextStopIndex = serializers.IntegerField()
    edgeID = serializers.CharField(max_length=200, required=True)
    laneIndex = serializers.IntegerField(default = 0)
    pos = serializers.FloatField(default = 1.0)
    duration = serializers.FloatField(default = -1073741824.0)
    flags = serializers.IntegerField(default = 0)
    startPos = serializers.FloatField(default = -1073741824.0)
    until = serializers.FloatField(default = -1073741824.0)
    teleport = serializers.IntegerField(default = 0)

class TransportationVehicleStateRerouteTraveltimeSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    currentTravelTimes = serializers.BooleanField(default = True)

class TransportationVehicleStateRerouteEffortSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)

class TransportationVehicleStateSetSpeedModeSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    sm = serializers.IntegerField()


class TransportationVehicleStateSetSpeedFactorSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    factor = serializers.FloatField()


class TransportationVehicleStateSetMaxSpeedSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    speed = serializers.FloatField()


class TransportationVehicleStateRemoveSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    reason = serializers.IntegerField(default=3)

class TransportationVehicleStateSetLaneChangeModeSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    lcm = serializers.IntegerField()

class TransportationVehicleStateUpdateBestLanesSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)

class TransportationVehicleAddSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    routeID = serializers.CharField(max_length=200, required=True)
    typeID = serializers.CharField(max_length=200, default = 'DEFAULT_VEHTYPE' )
    depart = serializers.CharField(max_length=200, default = None)
    departLane = serializers.CharField(max_length=200, default = 'first')
    departPos =  serializers.CharField(max_length=200,  default = 'base')
    departSpeed =  serializers.CharField(max_length=200, default = '0')
    arrivalLane = serializers.CharField(max_length=200, default = 'current')
    arrivalPos = serializers.CharField(max_length=200, default = 'max')
    arrivalSpeed = serializers.CharField(max_length=200, default = 'current')
    fromTaz = serializers.CharField(max_length=200,default = '')
    toTaz = serializers.CharField(max_length=200, default = '')
    line = serializers.CharField(max_length=200, default = '')
    personCapacity = serializers.IntegerField(default = 0)
    personNumber = serializers.IntegerField(default = 0)

class TransportationVehicleSetLengthSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    length = serializers.FloatField()

class TransportationVehicleSetVehicleClassSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    clazz = serializers.CharField(max_length=200, required=True)

class TransportationVehicleSetEmmisionClassSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    clazz = serializers.CharField(max_length=200, required=True)

class TransportationVehicleSetWidthSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    width = serializers.FloatField(required=True)


class TransportationVehicleSetHeightSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    height = serializers.FloatField(required=True)

class TransportationVehicleSetMinGapSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    minGap = serializers.FloatField(required=True)

class TransportationVehicleSetShapeClassSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    clazz = serializers.CharField(max_length=200, required=True)

class TransportationVehicleSetAccelerationSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    accel = serializers.FloatField(required=True)

class TransportationVehicleSetDecelerationSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    decel = serializers.FloatField(required=True)

class TransportationVehicleSetImperfectionSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    imperfection = serializers.FloatField(required=True)

class TransportationVehicleSetTauctionSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    tau = serializers.FloatField(required=True)

class TransportationVehicleSetTypeSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    typeID = serializers.CharField(max_length=200, required=True)

class TransportationVehicleSetViaSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    edgeList = serializers.CharField(max_length=200, required=True)

class TransportationVehicleSetMaxSpeedLatSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    speed = serializers.FloatField()

class TransportationVehicleSetMinGapLatSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    MinGapLat = serializers.FloatField()

class TransportationVehicleSetLateralAlignmentSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    align = serializers.CharField(max_length=200, required=True)

class TransportationVehicleSetParameterSerializer(serializers.Serializer):
    """"""
    objID = serializers.CharField(max_length=200, required=True)
    param = serializers.CharField(max_length=200, required=True)
    value = serializers.CharField(max_length=200, required=True)

class TransportationVehiclesetActionStepLengthSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    actionStepLength = serializers.FloatField()
    resetActionOffset = serializers.BooleanField(default = True)

class TransportationRouteGetSerializer(serializers.Serializer):
    """"""
    routeID = serializers.CharField(max_length=200, required=True)


class TransportationRouteAddSerializer(serializers.Serializer):
    """"""
    routeID = serializers.CharField(max_length=200, required=True)
    edges = serializers.CharField(max_length=400, required=False)


class TransportationStepSerializer(serializers.Serializer):
    """"""
    steps = serializers.IntegerField(default=1)


class TransportationLaneSetAllowedSerializer(serializers.Serializer):
    """"""
    laneID = serializers.CharField(max_length=200, required=True)
    allowedClasses = serializers.CharField(max_length=400, required=False)


class TransportationLaneSetDisallowedSerializer(serializers.Serializer):
    """"""
    laneID = serializers.CharField(max_length=200, required=True)
    disallowedClasses = serializers.CharField(max_length=400, required=False)


class PowerSerializer(serializers.Serializer):
    """"""
    experiment_name = serializers.CharField(max_length=200, required=True)
    timestep = serializers.IntegerField(required=True)
    itterations = serializers.IntegerField(required=True)


class CISStartSerializer(serializers.Serializer):
    """"""
    experiment_name = serializers.CharField(min_length=1, max_length=200, required=True)
    start_date = serializers.DateField(required=True)
    water_timestep_size_seconds = serializers.IntegerField(min_value=1, required=True)
    transportation_timestep_size_seconds = serializers.IntegerField(min_value=1, required=True)
    power_timestep_size_seconds = serializers.IntegerField(min_value=1, required=True)
    itterations = serializers.IntegerField(min_value=1, required=True)
    events = serializers.CharField(max_length=None, required=False, allow_blank=True)
    water_sensors = serializers.CharField(max_length=None, required=True)


class TransportationLaneSetMaxSpeedSerializer(serializers.Serializer):
    """"""
    laneID = serializers.CharField(max_length=200, required=True)
    speed = serializers.FloatField(required=True)


class TransportationLaneSetLengthSerializer(serializers.Serializer):
    """"""
    laneID = serializers.CharField(max_length=200, required=True)
    length = serializers.FloatField(min_value=0, required=True)

class TransportationPersonAddSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    edgeID = serializers.CharField(max_length=200, required=True)
    pos = length = serializers.FloatField()
    depart = length = serializers.FloatField(default = -3)
    typeID = serializers.CharField(max_length=200, default = 'DEFAULT_PEDTYPE')

class TransportationPersonAppendDrivingStageSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    toEdge = serializers.CharField(max_length=200, required=True)
    lines = serializers.CharField(max_length=200, required=True)
    stopID = serializers.CharField(max_length=200)

class TransportationPersonAppendWaitingStageSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    duration = serializers.FloatField()
    description = serializers.CharField(max_length=200, default = 'waiting')
    stopID = serializers.CharField(max_length=200)

class TransportationPersonAppendWalkingStageSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    edges = serializers.CharField(max_length=200, required=True)
    arrivalPos = serializers.FloatField()
    duration = serializers.FloatField(default = -1)
    speed = serializers.FloatField(default = -1)
    stopID = serializers.CharField(max_length=200)

class TransportationPersonRemoveStageSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    nextStageIndex = serializers.IntegerField()

class TransportationPersonRemoveStagesSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)

class TransportationPersonRerouteTraveltimeSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)

class TransportationPersonMoveToXYSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    edgeID = serializers.CharField(max_length=200, required=True)
    x = serializers.FloatField()
    y = serializers.FloatField()
    angle = serializers.FloatField(default = -1073741824.0)
    keepRoute = serializers.IntegerField(default = 1)
    matchThreshold = serializers.FloatField(default = 100)

class TransportationPersonSetHeightSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    height = serializers.FloatField(required = True)

class TransportationPersonSetLengthSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    length = serializers.FloatField(required = True)

class TransportationPersonSetMinGapSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    minGap = serializers.FloatField(required = True)

class TransportationPersonSetSpeedSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    speed = serializers.FloatField(required = True)

class TransportationPersonSetTypeSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    typeID = serializers.CharField(max_length=200, required=True)

class TransportationPersonSetWidthSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    width = serializers.FloatField(required = True)

class TransportationPersonSetColorSerializer(serializers.Serializer):
    """"""
    personID = serializers.CharField(max_length=200, required=True)
    color = serializers.CharField(max_length=200, required=True)

class TransportationVehicleTypeSetLengthSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    length = serializers.FloatField(required = True)

class TransportationVehicleTypeSetMaxSpeedSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    speed = serializers.FloatField(required = True)

class TransportationVehicleTypeSetVehicleClassSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    clazz = serializers.CharField(max_length=200, required=True)

class TransportationVehicleTypeSetSpeedFactorSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    factor = serializers.FloatField(required = True)

class TransportationVehicleTypeSetSpeedDeviationSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    deviation = serializers.FloatField(required = True)

class TransportationVehicleTypeSetEmissionClassSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    clazz = serializers.CharField(max_length=200, required=True)

class TransportationVehicleTypeSetWidthSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    width = serializers.FloatField(required = True)

class TransportationVehicleTypeSetHeightSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    height = serializers.FloatField(required = True)

class TransportationVehicleTypeSetMinGapSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    minGap = serializers.FloatField(required = True)

class TransportationVehicleTypeSetShapeClassSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    clazz = serializers.CharField(max_length=200, required=True)

class TransportationVehicleTypeSetAccelerationSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    accel = serializers.FloatField(required = True)

class TransportationVehicleTypeSetDecelerationSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    decel = serializers.FloatField(required = True)

class TransportationVehicleTypeSetImperfectionSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    imperfection = serializers.FloatField(required = True)

class TransportationVehicleTypeSetTauSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    tau = serializers.FloatField(required = True)

class TransportationVehicleTypeSetMinGapLatSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    minGapLat = serializers.FloatField(required = True)

class TransportationVehicleTypeSetMaxSpeedLatSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    speed = serializers.FloatField(required = True)

class TransportationVehicleTypeSetLateralAlignmentSerializer(serializers.Serializer):
    """"""
    typeID = serializers.CharField(max_length=200, required=True)
    latAlignment = serializers.CharField(max_length=200, required=True)

class TransportationVehicleTypeCopySerializer(serializers.Serializer):
    """"""
    origTypeID = serializers.CharField(max_length=200, required=True)
    newTypeID = serializers.CharField(max_length=200, required=True)

class TransportationVehicleTypeSetActionStepLengthSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    actionStepLength = serializers.FloatField(required = True)
    resetActionOffset = serializers.BooleanField(default = True)

class TransportationVehicleTypeSetColorSerializer(serializers.Serializer):
    """"""
    vehID = serializers.CharField(max_length=200, required=True)
    color = serializers.CharField (max_length = 200, required = True)


class TransportationRouteAddSerializer(serializers.Serializer):
    """"""
    routeID = serializers.CharField (max_length = 200, required = True)
    edges = serializers.CharField (max_length = 200, required = True)

class TransportationPoIStateSetTypeSerializer(serializers.Serializer):
    """"""
    poiID = serializers.CharField (max_length = 200, required = True)
    poiType = serializers.CharField (max_length = 200, required = True)

class TransportationPoIStateSetPositionSerializer(serializers.Serializer):
    """"""
    poiID = serializers.CharField (max_length = 200, required = True)
    x = serializers.FloatField(required = True)
    y = serializers.FloatField(required = True)

class TransportationPoIStateSetWidthSerializer(serializers.Serializer):
    """"""
    poiID = serializers.CharField (max_length = 200, required = True)
    width = serializers.FloatField(required = True)

class TransportationPoIStateSetHeightSerializer(serializers.Serializer):
    """"""
    poiID = serializers.CharField (max_length = 200, required = True)
    height = serializers.FloatField(required = True)

class TransportationPoIStateSetAngleSerializer(serializers.Serializer):
    """"""
    poiID = serializers.CharField (max_length = 200, required = True)
    angle = serializers.FloatField(required = True)

class TransportationPoIStateRemoveSerializer(serializers.Serializer):
    """"""
    poiID = serializers.CharField (max_length = 200, required = True)
    layer = serializers.IntegerField(default = 0)

class TransportationPolygonSetTypeSerializer(serializers.Serializer):
    """"""
    polygonID = serializers.CharField (max_length = 200, required = True)
    polygonType = serializers.CharField (max_length = 200, required = True)

class TransportationPolygonSetFilledSerializer(serializers.Serializer):
    """"""
    polygonID = serializers.CharField (max_length = 200, required = True)
    filled = serializers.BooleanField(required = True)

class TransportationPolygonSetLineWidthSerializer(serializers.Serializer):
    """"""
    polygonID = serializers.CharField (max_length = 200, required = True)
    lineWidth = serializers.FloatField(required = True)

class TransportationPolygonRemoveSerializer(serializers.Serializer):
    """"""
    polygonID = serializers.CharField (max_length = 200, required = True)
    layer = serializers.IntegerField(default = 0)

class TransportationPolygonAddDynamicsSerializer(serializers.Serializer):
    """"""
    polygonID = serializers.CharField (max_length = 200, required = True)
    trackedObjectID = serializers.CharField (max_length = 200, required = True)
    timeSpan = serializers.CharField (max_length = 200, required = True)
    alphaSpan = serializers.CharField (max_length = 200, required = True)
    looped = serializers.BooleanField(default = False)
    rotate = serializers.BooleanField(default = True)

class TransportationEdgesAdaptTraveltimeSerializer(serializers.Serializer):
    """"""
    edgeID = serializers.CharField (max_length = 200, required = True)
    time = serializers.FloatField(required = True)
    begin = serializers.FloatField(required = False)
    end = serializers.FloatField (required = False)

class TransportationEdgesSetEffortSerializer(serializers.Serializer):
    """"""
    edgeID = serializers.CharField (max_length = 200, required = True)
    effort = serializers.FloatField(required = True)
    begin = serializers.FloatField(required = False)
    end = serializers.FloatField (required = False)

class TransportationEdgesSetMaxSpeedSerializer(serializers.Serializer):
    """"""
    edgeID = serializers.CharField (max_length = 200, required = True)
    speed = serializers.FloatField(required = True)

class TransportationSimulationClearPendingSerializer(serializers.Serializer):
    """"""
    routeID = serializers.CharField (max_length = 200, required = True)

class TransportationSimulationSaveStateSerializer(serializers.Serializer):
    """"""
    fileName = serializers.CharField (max_length = 200, required = True)

class TransportationSimulationLoadStateSerializer(serializers.Serializer):
    """"""
    fileName = serializers.CharField (max_length = 200, required = True)