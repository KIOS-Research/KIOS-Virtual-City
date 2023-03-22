import math
import random

from . import models

def sensorsValue(sensor_id, sensor_value):
    try:
        sensor=models.SensorsProfile.objects.get(sensor_unique_id=sensor_id)

        resolution = sensor.sensor_resolution
        uncertainty = sensor.sensor_uncertainty
        uncertaintydist = sensor.sensor_uncertainty_dist
        minval = sensor.sensor_min
        maxval = sensor.sensor_max

        # Sensor Resolution
        t001 = str(resolution).split('.')
        flformat = "{:." + str(len(t001[1])) + "f}"
        if (float(sensor_value) / float(resolution)).is_integer():
            resultwithrest = sensor_value
        else:
            resultwithrest = float(sensor_value) - math.fmod(float(sensor_value), float(resolution))
            resultwithrest = flformat.format(resultwithrest)
        # Sensor Uncertainty
        if uncertainty > 0:
            unc_value = (float(resultwithrest) * float(uncertainty)) / float(100)
            randval = 0
            # Sensor Uncertainty Distribution
            if uncertaintydist == "uniform":
                randval = random.uniform(-unc_value, unc_value)
            resultwithrest = float(resultwithrest) + float(randval)
            resultwithrest = flformat.format(resultwithrest)
        if float(resultwithrest) > float(maxval):
            resultwithrest = maxval
        elif float(resultwithrest) < float(minval):
            resultwithrest = minval
        return resultwithrest
    except:
        return "error"


