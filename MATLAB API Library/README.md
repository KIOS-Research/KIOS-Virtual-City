# MATLAB API Documentation

## Installation

- In Matlab software go to `MATLAB APILibrary` folder
- In your file create a variable using the `KIOSBaSP` file. e.g `s = KIOSBaSP()`
- Call the functions using the structure `s.WaterLoadGet`
- For more information about KIOSBaSP Library, right click on `KIOSBaSP()` and select `"Help on KIOSBaSP"` or left click on `KIOSBaSP()` and press `F1`.

## Initial Scenario

- Step 1 : Load an EPANET using the function `WaterLoadPost` which load the `ltown`
- Step 2 : Start an EPANET simulation using the function `WaterStartPost(startDate, endDate, expiramentname, sensors)`. Arguments `startDate` and `endDate` must be in format `YYYY-MM-DD`. Argument expiramentname must be a unique name which is not
already reserved. Find all the reserved experiment names using the `WaterStartGet` function. Argument `sensors` must be a json file includes sensors information. In `exampleFiles` folder, `sensors.json` is an example file. 
- Step 3: Information about sensors in a json file can retreive using `WaterOutputJsonPost(experimentname)`. Argument `experimentname` must be a name provided in the `WaterStartPost` function.
- Step 4 : Information about sensors in an array, can retreive using the `WaterOutputSensorsPost(experimentname,sensorid)`. Argument `experimentname` must be a name provided in the `WaterStartPost` function. Argument 
`sensorid` must be a list with sensors name. e.g `WaterOutputSensorsPost('test01','["pressure_1"]')`.