from django.db import models

# Create your models here.
class WaterBackdrop(models.Model):
    field = models.CharField(max_length=300, blank=True, null=True)
    value = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'water_backdrop'


class WaterControls(models.Model):
    control = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'water_controls'


class WaterCoordinates(models.Model):
    node = models.CharField(max_length=300, blank=True, null=True)
    xcoord = models.FloatField(blank=True, null=True)
    ycoord = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_coordinates'


class WaterCurves(models.Model):
    curveid = models.CharField(max_length=200, blank=True, null=True)
    xvalue = models.FloatField(blank=True, null=True)
    yvalue = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_curves'


class WaterDemands(models.Model):
    junction = models.CharField(max_length=200, blank=True, null=True)
    demand = models.FloatField(blank=True, null=True)
    pattern = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_demands'


class WaterEmitters(models.Model):
    junction = models.CharField(max_length=200, blank=True, null=True)
    coefficient = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_emitters'


class WaterEnergy(models.Model):
    field = models.CharField(max_length=200, blank=True, null=True)
    value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_energy'


class WaterJunctions(models.Model):
    junctionid = models.CharField(max_length=200, blank=True, null=True)
    elev = models.FloatField(blank=True, null=True)
    demand = models.FloatField(blank=True, null=True)
    pattern = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_junctions'


class WaterLabels(models.Model):
    xcoord = models.FloatField(blank=True, null=True)
    ycoord = models.FloatField(blank=True, null=True)
    label = models.CharField(max_length=200, blank=True, null=True)
    anchor = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_labels'


class WaterMixing(models.Model):
    tank = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_mixing'


class WaterOptions(models.Model):
    field = models.CharField(max_length=200, blank=True, null=True)
    value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_options'


class WaterPatterns(models.Model):
    patternid = models.CharField(max_length=200, blank=True, null=True)
    multipliers = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_patterns'


class WaterPipes(models.Model):
    pipeid = models.CharField(max_length=200, blank=True, null=True)
    node1 = models.CharField(max_length=200, blank=True, null=True)
    node2 = models.CharField(max_length=200, blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    diameter = models.FloatField(blank=True, null=True)
    roughness = models.FloatField(blank=True, null=True)
    minorloss = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_pipes'


class WaterPumps(models.Model):
    pumpid = models.CharField(max_length=200, blank=True, null=True)
    node1 = models.CharField(max_length=200, blank=True, null=True)
    node2 = models.CharField(max_length=200, blank=True, null=True)
    parameters = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_pumps'


class WaterQuality(models.Model):
    node = models.CharField(max_length=200, blank=True, null=True)
    initqual = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_quality'


class WaterReactions(models.Model):
    type = models.CharField(max_length=200, blank=True, null=True)
    coefficient = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_reactions'


class WaterReport(models.Model):
    field = models.CharField(max_length=200, blank=True, null=True)
    value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_report'


class WaterReservoirs(models.Model):
    reservoirid = models.CharField(max_length=200, blank=True, null=True)
    head = models.FloatField(blank=True, null=True)
    pattern = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_reservoirs'


class WaterRules(models.Model):
    ruleid = models.CharField(max_length=200, blank=True, null=True)
    rule = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_rules'


class WaterSources(models.Model):
    node = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    quality = models.FloatField(blank=True, null=True)
    pattern = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_sources'


class WaterStatus(models.Model):
    statusid = models.CharField(max_length=200, blank=True, null=True)
    statussetting = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_status'


class WaterTags(models.Model):
    object = models.CharField(max_length=200, blank=True, null=True)
    tagid = models.CharField(max_length=200, blank=True, null=True)
    tag = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_tags'


class WaterTanks(models.Model):
    tankid = models.CharField(max_length=200, blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    initlevel = models.FloatField(blank=True, null=True)
    minlevel = models.FloatField(blank=True, null=True)
    maxlevel = models.FloatField(blank=True, null=True)
    diameter = models.FloatField(blank=True, null=True)
    minvol = models.FloatField(blank=True, null=True)
    volcurve = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_tanks'


class WaterTimes(models.Model):
    field = models.CharField(max_length=200, blank=True, null=True)
    value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:

        db_table = 'water_times'


class WaterValves(models.Model):
    valveid = models.CharField(max_length=200, blank=True, null=True)
    node1 = models.CharField(max_length=200, blank=True, null=True)
    node2 = models.CharField(max_length=200, blank=True, null=True)
    diameter = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    setting = models.FloatField(blank=True, null=True)
    minorloss = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_valves'


class WaterVertices(models.Model):
    link = models.CharField(max_length=200, blank=True, null=True)
    xcoord = models.FloatField(blank=True, null=True)
    ycoord = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_vertices'


#Need to be changed and only the last value should be added
#TODO
class WaterOutputNodes(models.Model):
    nodeid = models.CharField(max_length=200, blank=True, null=True)
    nodetype = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_output_nodes'


class WaterOutputNodesValues(models.Model):
    nodeid = models.CharField(max_length=200, blank=True, null=True)
    readingtime = models.DateTimeField()
    nodedemand = models.FloatField(blank=True, null=True)
    nodehead = models.FloatField(blank=True, null=True)
    nodepressure = models.FloatField(blank=True, null=True)
    nodequality = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_output_nodes_values'


class WaterOutputLinks(models.Model):
    linkid = models.CharField(max_length=200, blank=True, null=True)
    linktype = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'water_output_links'


class WaterOutputLinksValues(models.Model):
    linkid = models.CharField(max_length=200, blank=True, null=True)
    readingtime = models.DateTimeField()
    linkfriction = models.FloatField(blank=True, null=True)
    linkheadloss = models.FloatField(blank=True, null=True)
    linkquality = models.FloatField(blank=True, null=True)
    linkreactionrate = models.FloatField(blank=True, null=True)
    linksetting = models.FloatField(blank=True, null=True)
    linkstatus = models.CharField(max_length=200, blank=True, null=True)
    linkvelocity = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_output_links_values'


#TODO
'''
class WaterOutputScadaSensors(models.Model):
    re_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    sensorid = models.CharField(max_length=200, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_output_scada_sensors'


class WaterOutputScadaSensorDetails(models.Model):
    s_id = models.AutoField(primary_key=True)
    sensorid = models.CharField(max_length=200, blank=True, null=True)
    node_link_id = models.CharField(max_length=200, blank=True, null=True)
    sensortype = models.CharField(max_length=200, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'water_output_scada_sensor_details'
'''


class ExperimentNames(models.Model):
    ex_name_id = models.AutoField(primary_key=True)
    ex_name = models.CharField(max_length=200, blank=True, null=True)
    ex_sensor_filename = models.CharField(max_length=400, blank=True, null=True)
    ex_events_filename = models.CharField(max_length=400, blank=True, null=True)
    ex_time_filename = models.CharField(max_length=400, blank=True, null=True)
    ex_parameters_filename = models.CharField(max_length=400, blank=True, null=True)
    ex_sensor_events_filename = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        db_table = 'experiment_names'


class PowerSubstations(models.Model):
    subid = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'power_substation'


class PowerTimes(models.Model):
    timeid = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'power_times'


class PowerOutputVoltages(models.Model):
    outid = models.CharField(max_length=200, blank=True, null=True)
    voltage = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'power_output_voltages'

class SensorsProfile(models.Model):
    pk_id = models.AutoField(primary_key=True)
    sensor_type = models.CharField(max_length = 200, blank = True, null = True)
    sensor_brand = models.CharField(max_length = 200, blank = True, null = True)
    sensor_model = models.CharField(max_length = 200, blank = True, null = True)
    sensor_unique_id = models.CharField(max_length = 200, blank = True, null = True)
    sensor_min = models.FloatField(blank = True, null = True)
    sensor_max = models.FloatField(blank = True, null = True)
    sensor_si = models.CharField(max_length = 200, blank = True, null = True)
    sensor_resolution = models.FloatField(blank = True, null = True)
    sensor_uncertainty = models.FloatField(blank = True, null = True)
    sensor_uncertainty_dist = models.CharField(max_length = 200, blank = True, null = True)

    class Meta:
        db_table = 'sensors_profile'