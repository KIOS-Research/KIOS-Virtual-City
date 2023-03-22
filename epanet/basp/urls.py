from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.contrib import admin

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="KIOS Backend Software Platform BaSP",
      default_version='v1',
      description="The is the BaSP RESTful API Documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="isaia.philippos@ucy.ac.cy"),
      license=openapi.License(name="License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

from . import views
router = DefaultRouter()
router.register('water/clear', views.WaterClearDataView, basename='clear')
router.register('water/load', views.WaterLoadView, basename='load')
router.register('water/start', views.WaterStartView, basename='start')
router.register('water/startwntr', views.WaterStartWntrView, basename='startwntr')
router.register('water/stepexecution', views.WaterStepExecution, basename='stepexecution')
router.register('water/input', views.WaterView, basename='input')
router.register('water/input/deletedb', views.WaterDeleteDBViewSet, basename='deletedb')
router.register('water/input/backdrop', views.WaterBackdropViewSet, basename='waterbackdrop')
router.register('water/input/controls', views.WaterControlsViewSet, basename='watercontrols')
router.register('water/input/coordinates', views.WaterCoordinatesViewSet, basename='watercoordinates')
router.register('water/input/curves', views.WaterCurvesViewSet, basename='watercurves')
router.register('water/input/emitters', views.WaterEmittersViewSet, basename='wateremitters')
router.register('water/input/energy', views.WaterEnergyViewSet, basename='waterenergy')
router.register('water/input/junctions', views.WaterJunctionsViewSet, basename='waterjunctions')
router.register('water/input/labels', views.WaterLabelsViewSet, basename='waterlabels')
router.register('water/input/mixing', views.WaterMixingViewSet, basename='watermixing')
router.register('water/input/options', views.WaterOptionsViewSet, basename='wateroptions')
router.register('water/input/patterns', views.WaterPatternsViewSet, basename='waterpatterns')
router.register('water/input/pipes', views.WaterPipesViewSet, basename='waterpipes')
router.register('water/input/pumps', views.WaterPumpsViewSet, basename='waterpumps')
router.register('water/input/reactions', views.WaterReactionsViewSet, basename='waterreactions')
router.register('water/input/report', views.WaterReportViewSet, basename='waterreport')
router.register('water/input/reservoirs', views.WaterReservoirsViewSet, basename='waterreservoirs')
router.register('water/input/sources', views.WaterSourcesViewSet, basename='watersources')
router.register('water/input/tanks', views.WaterTanksViewSet, basename='watertanks')
router.register('water/input/times', views.WaterTimesViewSet, basename='watertimes')
router.register('water/input/valves', views.WaterValvesViewSet, basename='watervalves')
router.register('water/input/leak',views.WaterAddLeakViewSet,basename='leak')
router.register('water/input/earthquake', views.WaterEarthquakeViewSet, basename = 'earthquake')
router.register('water/output/sensors', views.WaterOutputSensorsValuesViewSet, basename='sensors')
router.register('water/output/json', views.WaterJSONFileView, basename='json')

router.register('transportation/output/lane/getLength', views.TransportationLaneGetLengthViewSet, basename='lane/getLength')
router.register('transportation/output/lane/getMaxSpeed', views.TransportationLaneGetMaxSpeedViewSet, basename='lane/getMaxSpeed')
router.register('transportation/output/lane/getIDList', views.TransportationLaneGetIDListViewSet, basename='lane/getIDList')
router.register('transportation/output/lane/getIDCount', views.TransportationLaneGetIDCountViewSet, basename='lane/getIDCount')
router.register('transportation/output/lane/getCO2Emission', views.TransportationLaneGetCO2EmissionViewSet, basename='lane/getCO2Emission')
router.register('transportation/output/lane/getCOEmission', views.TransportationLaneGetCOEmissionViewSet, basename='lane/getCOEmission')
router.register('transportation/output/lane/getHCEmission', views.TransportationLaneGetHCEmissionViewSet, basename='lane/getHCEmission')
router.register('transportation/output/lane/getPMxEmission', views.TransportationLaneGetPMxEmissionViewSet, basename='lane/getPMxEmission')
router.register('transportation/output/lane/getNOxEmission', views.TransportationLaneGetNOxEmissionViewSet, basename='lane/getNOxEmission')
router.register('transportation/output/lane/getFuelConsumption', views.TransportationLaneGetFuelConsumptionViewSet, basename='lane/getFuelConsumption')
router.register('transportation/output/lane/getNoiseEmission', views.TransportationLaneGetNoiseEmissionViewSet, basename='lane/getNoiseEmission')
router.register('transportation/output/lane/getElectricityConsumption', views.TransportationLaneGetElectricityConsumptionViewSet, basename='lane/getElectricityConsumption')
router.register('transportation/input/lane/setAllowed', views.TransportationLaneSetAllowedViewSet, basename='lane/setAllowed')
router.register('transportation/input/lane/setDisallowed', views.TransportationLaneSetDisallowedViewSet, basename='lane/setDisallowed')
router.register('transportation/input/lane/setMaxSpeed', views.TransportationLaneSetMaxSpeedViewSet, basename='lane/setMaxSpeed')
router.register('transportation/input/lane/setLength', views.TransportationLaneSetLengthViewSet, basename='lane/setLength')

router.register('transportation/output/trafficlight/getIDList', views.TransportationTrafficlightGetIDListViewSet, basename='trafficlight/getIDList')
router.register('transportation/output/trafficlight/getRedYellowGreenState', views.TransportationTrafficlightGetRedYellowGreenStateViewSet, basename='trafficlight/getRedYellowGreenState')
router.register('transportation/output/trafficlight/getIDCount', views.TransportationTrafficlightGetIDCountViewSet, basename='trafficlight/getIDCount')
router.register('transportation/output/trafficlight/getPhaseDuration', views.TransportationTrafficlightGetPhaseDurationViewSet, basename='trafficlight/getPhaseDuration')
router.register('transportation/output/trafficlight/getPhase', views.TransportationTrafficlightGetPhaseViewSet, basename='trafficlight/getPhase')
router.register('transportation/input/trafficlight/setRedYellowGreenState', views.TransportationTrafficlightSetRedYellowGreenStateViewSet, basename='trafficlight/setRedYellowGreenState')
router.register('transportation/input/trafficlight/setLinkState', views.TransportationTrafficlightSetLinkStateViewSet, basename='trafficlight/setLinkState')
router.register('transportation/input/trafficlight/setPhase', views.TransportationTrafficlightSetPhaseViewSet, basename='trafficlight/setPhase')
router.register('transportation/input/trafficlight/setPhaseDuration', views.TransportationTrafficlightSetPhaseDurationViewSet, basename='trafficlight/setPhaseDuration')

router.register('transportation/output/vehicle/getIDCount',views.TransportationVehicleGetIDCountViewSet, basename = 'vehiclegetIDCount')
router.register('transportation/output/vehicle/getIDList', views.TransportationVehicleGetIDListViewSet, basename='vehiclegetIDList')
router.register('transportation/output/vehicle/getSpeed', views.TransportationVehicleGetSpeedViewSet, basename='vehicle/getSpeed')
router.register('transportation/output/vehicle/getAcceleration', views.TransportationVehicleGetAccelerationViewSet, basename = 'vehicleGetAcceleration')
router.register('transportation/output/vehicle/getPosition',views.TransportationVehicleGetPositionViewSet, basename = 'vehicleGetPosition')
router.register('transportation/output/vehicle/getCO2Emission',views.TransportationVehicleGetCO2EmissionViewSet,basename = 'vehicleGetCO2Emission')
router.register('transportation/output/vehicle/getCOEmission',views.TransportationVehicleGetCOEmissionViewSet,basename = 'vehicleGetCOEmission')
router.register('transportation/output/vehicle/getHCEmission',views.TransportationVehicleGetHCEmissionViewSet,basename = 'vehicleGetHCEmission')
router.register('transportation/output/vehicle/getPMxEmission',views.TransportationVehicleGetPMxEmissionViewSet,basename = 'vehicleGetPMxEmission')
router.register('transportation/output/vehicle/getNOxEmission',views.TransportationVehicleGetNOxEmissionViewSet,basename = 'vehicleGetNOxEmission')
router.register('transportation/output/vehicle/getFuelConsumption',views.TransportationVehicleGetFuelConsumptionViewSet,basename = 'vehicleGetFuelConsumption')
router.register('transportation/output/vehicle/getNoiseEmission',views.TransportationVehicleGetNoiseEmissionViewSet,basename = 'vehicleGetNoiseEmission')
router.register('transportation/output/vehicle/getElectricityConsumption',views.TransportationVehicleGetElectricityConsumptionViewSet,basename = 'vehicleGetElectricityConsumption')
router.register('transportation/input/vehicle/setStop',views.TransportationVehicleStateSetStopViewSet,basename = 'vehiclesetStop')

router.register('transportation/input/vehicle/setBusStop',views.TransportationVehicleStateSetBusStopViewSet,basename = 'vehiclesetBusStop')
router.register('transportation/input/vehicle/setContainerStop',views.TransportationVehicleStateSetContainerStopViewSet,basename = 'vehiclesetContainerStop')
router.register('transportation/input/vehicle/setChargingStop',views.TransportationVehicleStateSetChargingStopViewSet,basename = 'vehiclesetContainerStop')
router.register('transportation/input/vehicle/setParkingAreaStop',views.TransportationVehicleStateSetParkingAreaStopViewSet,basename = 'vehiclesetParkingAreaStop')
router.register('transportation/input/vehicle/resume',views.TransportationVehicleStateResumeViewSet,basename = 'vehicleresume')
router.register('transportation/input/vehicle/ChangeTarget',views.TransportationVehicleStateChangeTargetViewSet,basename = 'vehicleChangeTarget')
router.register('transportation/input/vehicle/setRouteID',views.TransportationVehicleStateSetRouteIDViewSet,basename = 'vehicleSetRouteID')
router.register('transportation/input/vehicle/setRoute',views.TransportationVehicleStateSetRouteViewSet,basename = 'vehicleSetRoute')
router.register('transportation/input/vehicle/rerouteParkingArea',views.TransportationVehicleRerouteParkingAreaViewSet,basename = 'vehiclererouteParkingArea')

router.register('transportation/input/vehicle/setAdaptedTraveltime',views.TransportationVehicleStateSetAdaptedTraveltimeViewSet,basename = 'vehiclesetAdaptedTraveltime')
router.register('transportation/input/vehicle/setEffort',views.TransportationVehicleStatesetEffortViewSet,basename = 'vehicleSetEffort')
router.register('transportation/input/vehicle/setSignals',views.TransportationVehicleStateSetSignalsViewSet,basename = 'vehiclesetSignals')
router.register('transportation/input/vehicle/setRoutingMode',views.TransportationVehicleStatesetRoutingModeViewSet,basename = 'vehiclesetRoutingMode')
router.register('transportation/input/vehicle/MoveTo',views.TransportationVehicleStateMoveToViewSet,basename = 'vehiclesetMoveTo')
router.register('transportation/input/vehicle/MoveToXY',views.TransportationVehicleStateMoveToXYViewSet,basename = 'vehiclesetMoveToXY')
router.register('transportation/input/vehicle/replaceStop',views.TransportationVehicleStateReplaceStopViewSet,basename = 'replaceStop')
router.register('transportation/input/vehicle/rerouteTraveltime',views.TransportationVehicleStateRerouteTraveltimeViewSet,basename = 'rerouteTraveltime')
router.register('transportation/input/vehicle/rerouteEffort',views.TransportationVehicleStateRerouteEffortViewSet,basename = 'rerouteEffort')
router.register('transportation/input/vehicle/setLaneChangeMode',views.TransportationVehicleStateSetLaneChangeModeViewSet,basename = 'setLaneChangeMode')
router.register('transportation/input/vehicle/updateBestLanes',views.TransportationVehicleStateUpdateBestLanesViewSet,basename = 'updateBestLanes')
router.register('transportation/input/vehicle/add',views.TransportationVehicleAddViewSet,basename = 'addvehicle')
router.register('transportation/input/vehicle/setLength',views.TransportationVehicleSetLengthViewSet,basename = 'setVehicleLength')
router.register('transportation/input/vehicle/setVehicleClass',views.TransportationVehicleSetVehicleClassViewSet,basename = 'setVehicleLength')
router.register('transportation/input/vehicle/setEmmisionClass',views.TransportationVehicleSetEmissionClassViewSet,basename = 'setEmmisionClass')
router.register('transportation/input/vehicle/setWidth',views.TransportationVehicleSetWidthViewSet,basename = 'setWidth')
router.register('transportation/input/vehicle/setHeight',views.TransportationVehicleSetHeightViewSet,basename = 'setHeight')
router.register('transportation/input/vehicle/minGap',views.TransportationVehicleMinGapViewSet,basename = 'minGap')
router.register('transportation/input/vehicle/shapeClass',views.TransportationVehicleSetShapeClassViewSet,basename = 'setHeight')
router.register('transportation/input/vehicle/SetAcceleration',views.TransportationVehicleSetAccelerationViewSet,basename = 'setacceleration')
router.register('transportation/input/vehicle/SetDeceleration ',views.TransportationVehicleSetDecelerationViewSet,basename = 'setdeceleration ')
router.register('transportation/input/vehicle/SetImperfection',views.TransportationVehicleSetImperfectionViewSet,basename = 'setimperfection')
router.register('transportation/input/vehicle/SetTau',views.TransportationVehicleSetTauViewSet,basename = 'settau')
router.register('transportation/input/vehicle/SetType',views.TransportationVehicleSetTypeViewSet,basename = 'setType')
router.register('transportation/input/vehicle/SetVia',views.TransportationVehicleSetViaViewSet,basename = 'setvia')
router.register('transportation/input/vehicle/setMaxSpeedLat',views.TransportationVehicleSetMaxSpeedLatViewSet,basename = 'setMaxSpeedLat')
router.register('transportation/input/vehicle/setMinGapLat',views.TransportationVehicleSetMinGapLatViewSet,basename = 'setMinGapLat')
router.register('transportation/input/vehicle/setLateralAlignment',views.TransportationVehicleSetLateralAlignmentViewSet,basename = 'setLateralAlignment')
router.register('transportation/input/vehicle/setParameter',views.TransportationVehicleSetParameterViewSet,basename = 'setParameter')
router.register('transportation/input/vehicle/setActionStepLength',views.TransportationVehicleSetActionStepLengthViewSet,basename = 'setActionStepLength')



router.register('transportation/input/vehicle/changeLane',views.TransportationVehicleStateChangeLaneViewSet,basename = 'vehiclechangeLane')
router.register('transportation/input/vehicle/changeSubLane',views.TransportationVehicleStateChangeSubLaneViewSet,basename = 'vehiclechangeSubLane')
router.register('transportation/input/vehicle/slowDown',views.TransportationVehicleStateSlowDownViewSet,basename = 'vehicleSlowDown')
router.register('transportation/input/vehicle/setSpeed',views.TransportationVehicleStateSetSpeedViewSet,basename = 'vehicleSetSpeed')
router.register('transportation/input/vehicle/MoveTo',views.TransportationVehicleStateMoveToViewSet,basename = 'vehicleMoveTo')
router.register('transportation/input/vehicle/setSpeedMode',views.TransportationVehicleStateSetSpeedModeViewSet,basename = 'vehicleSetSpeedMode')
router.register('transportation/input/vehicle/setMaxSpeed',views.TransportationVehicleStateSetMaxSpeedViewSet,basename = 'vehicleSetMaxSpeed')
router.register('transportation/input/vehicle/Remove',views.TransportationVehicleStateRemoveViewSet,basename = 'vehicleRemove')
router.register('transportation/input/vehicle/setColor',views.TransportationVehicleStateSetColorViewSet,basename = 'vehicleSetColor')


router.register('transportation/output/route/getIDList', views.TransportationRouteGetIDListViewSet, basename='route/getIDList')
router.register('transportation/output/route/getIDCount', views.TransportationRouteGetIDCountViewSet, basename='route/getIDCount')
router.register('transportation/output/route/getEdges', views.TransportationRouteGetEdgesViewSet, basename='route/getEdges')
router.register('transportation/input/route/add', views.TransportationRouteAddViewSet, basename='route/add')

router.register('transportation/input/person/Add',views.TransportationPersonAddViewSet,basename = 'addPerson')
router.register('transportation/input/person/appendDrivingStage',views.TransportationPersonAppendDrivingStageViewSet,basename = 'appendDrivingStage')
router.register('transportation/input/person/appendWaitingStage',views.TransportationPersonAppendWaitingStageViewSet,basename = 'appendWaitingStage')
router.register('transportation/input/person/appendWalkingStage',views.TransportationPersonAppendWalkingStageViewSet,basename = 'appendWalkingStage')
router.register('transportation/input/person/removeStage',views.TransportationPersonRemoveStageViewSet,basename = 'removeStage')
router.register('transportation/input/person/removeStages',views.TransportationPersonRemoveStagesViewSet,basename = 'removeStages')
router.register('transportation/input/person/rerouteTraveltime',views.TransportationPersonRerouteTraveltimeViewSet,basename = 'rerouteTraveltime')
router.register('transportation/input/person/moveToXY',views.TransportationPersonMoveToXYViewSet,basename = 'personmovetoxy')
router.register('transportation/input/person/setHeight',views.TransportationPersonSetHeightViewSet,basename = 'setHeight')
router.register('transportation/input/person/setLength',views.TransportationPersonSetLengthViewSet,basename = 'setLength')
router.register('transportation/input/person/setMinGap',views.TransportationPersonSetMinGapViewSet,basename = 'setMinGap')
router.register('transportation/input/person/setSpeed',views.TransportationPersonSetSpeedViewSet,basename = 'setSpeed')
router.register('transportation/input/person/setType',views.TransportationPersonSetTypeViewSet,basename = 'setType')
router.register('transportation/input/person/setWidth',views.TransportationPersonSetWidthViewSet,basename = 'setWidth')
router.register('transportation/input/person/setColor',views.TransportationPersonSetColorViewSet,basename = 'setColor')


router.register('transportation/input/vehicleType/setLength',views.TransportationVehicleTypeSetLengthViewSet,basename = 'vehicleTypeSetLength')
router.register('transportation/input/vehicleType/setMaxSpeed',views.TransportationVehicleTypeSetMaxSpeedViewSet,basename = 'vehicleTypeSetMaxSpeed')
router.register('transportation/input/vehicleType/setVehicleClass',views.TransportationVehicleTypeSetVehicleClassViewSet,basename = 'vehicleTypeSetVehicleClass')
router.register('transportation/input/vehicleType/setSpeedFactor',views.TransportationVehicleTypeSetSpeedFactorViewSet,basename = 'vehicleTypeSetSpeedFactor')
router.register('transportation/input/vehicleType/setSpeedDeviation',views.TransportationVehicleTypeSetSpeedDeviationViewSet,basename = 'vehicleTypeSetSpeedDeviation')
router.register('transportation/input/vehicleType/setEmissionClass',views.TransportationVehicleTypeSetEmissionClassViewSet,basename = 'vehicleTypeSetEmissionClass')
router.register('transportation/input/vehicleType/setWidth',views.TransportationVehicleTypeSetWidthViewSet,basename = 'vehicleTypeSetWidth')
router.register('transportation/input/vehicleType/setHeight',views.TransportationVehicleTypeSetHeightViewSet,basename = 'vehicleTypeSetHeight')
router.register('transportation/input/vehicleType/setMinGap',views.TransportationVehicleTypeSetMinGapViewSet,basename = 'vehicleTypeSetMinGap')
router.register('transportation/input/vehicleType/setShapeClass',views.TransportationVehicleTypeSetShapeClassViewSet,basename = 'vehicleTypeSetShapeClass')
router.register('transportation/input/vehicleType/setAcceleration',views.TransportationVehicleTypeSetAccelerationViewSet,basename = 'vehicleTypeSetAcceleration')
router.register('transportation/input/vehicleType/setDeceleration',views.TransportationVehicleTypeSetDecelerationViewSet,basename = 'vehicleTypeSetDeceleration')
router.register('transportation/input/vehicleType/setImperfection',views.TransportationVehicleTypeSetImperfectionViewSet,basename = 'vehicleTypeSetImperfection')
router.register('transportation/input/vehicleType/setTau',views.TransportationVehicleTypeSetTauViewSet,basename = 'vehicleTypeSetTau')
router.register('transportation/input/vehicleType/setMaxSpeedLat',views.TransportationVehicleTypeSetMaxSpeedLatViewSet,basename = 'vehicleTypesetMaxSpeedLat')
router.register('transportation/input/vehicleType/setMinGapLat',views.TransportationVehicleTypeSetMinGapLatViewSet,basename = 'vehicleTypesetMinGapLat')
router.register('transportation/input/vehicleType/setLateralAlignment',views.TransportationVehicleTypeSetLateralAlignmentViewSet,basename = 'vehicleTypeLateralAlignment')
router.register('transportation/input/vehicleType/copy',views.TransportationVehicleTypeCopyViewSet,basename = 'vehicleTypeCopy')
router.register('transportation/input/vehicleType/setActionStepLength',views.TransportationVehicleTypeActionStepLengthViewSet,basename = 'vehicleTypesetActionStepLength')
router.register('transportation/input/vehicleType/dispatchTaxi',views.TransportationVehicleStatedispatchTaxiViewSet,basename = 'vehicledispatchTaxi')
router.register('transportation/input/vehicleType/setColor',views.TransportationVehicleTypeSetColorViewSet,basename = 'vehiclesetcolor')

router.register('transportation/input/PoIState/setType',views.TransportationPoIStateSetTypeViewSet,basename = 'poiStateSetType')
router.register('transportation/input/PoIState/setPosition',views.TransportationPoIStateSetPositionViewSet,basename = 'poiStateSetPosition')
router.register('transportation/input/PoIState/setWidth',views.TransportationPoIStateSetWidthViewSet,basename = 'poiStateSetWidth')
router.register('transportation/input/PoIState/setHeight',views.TransportationPoIStateSetHeightViewSet,basename = 'poiStateSetHeight')
router.register('transportation/input/PoIState/setAngle',views.TransportationPoIStateSetAngleViewSet,basename = 'poiStateSetAngle')
router.register('transportation/input/PoIState/Remove',views.TransportationPoIStateRemoveViewSet,basename = 'poiStateRemove')

router.register('transportation/input/Polygon/setType',views.TransportationPolygonSetTypeViewSet,basename = 'polygonSetType')
router.register('transportation/input/Polygon/setFilled',views.TransportationPolygonSetFilledViewSet,basename = 'polygonSetFilled')
router.register('transportation/input/Polygon/setLineWidth',views.TransportationPolygonSetLineWidthViewSet,basename = 'polygonSetLineWidth')
router.register('transportation/input/Polygon/remove',views.TransportationPolygonRemoveViewSet,basename = 'Polygonremove')
router.register('transportation/input/Polygon/addDynamics',views.TransportationPolygonAddDynamicsViewSet,basename = 'PolygonAddDynamics')

router.register('transportation/input/simulation/clearPending',views.TransportationSimulationClearPendingViewSet,basename = 'SimulationclearPending')
router.register('transportation/input/simulation/saveState',views.TransportationSimulationSaveStateViewSet,basename = 'SimulationsaveState')
router.register('transportation/input/simulation/loadState',views.TransportationSimulationLoadStateViewSet,basename = 'SimulationloadState')

router.register('transportation/input/edge/adaptTraveltime',views.TransportationEdgesAdaptTraveltimeViewSet,basename = 'EdgeadaptTraveltime')
router.register('transportation/input/edge/setEffort',views.TransportationEdgesSetEffortViewSet,basename = 'EdgeSetEffort')
router.register('transportation/input/edge/setMaxSpeed',views.TransportationEdgesSetMaxSpeedViewSet,basename = 'EdgeSetMaxSpeed')

router.register('transportation/start', views.TransportationStartViewSet, basename='transportation/start')
router.register('transportation/input/steps', views.TransportationStepsViewSet, basename='steps')

router.register('power/input', views.PowerViewSet, basename='power')

router.register('CIS/start', views.CISStartViewSet, basename='cisstart')

urlpatterns = [
    #OpenAPI Schema $ Swagger
    url(r'', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^documentation(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^documentation/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
