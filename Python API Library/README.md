# Python API

## Initialization

- In python file import the API and initialize it using the following code:
```
import KIOSBaSP

basp=KIOSBaSP.KiosBasp()
```
- Call the API functions using `basp.function()`
- For more information about the available functions read the API documentation. 
  Access the documentation writing  `pydoc -w KIOSBaSP` in the terminal to extract it as an HTML file.

## Simple Scenario

Load the initial EPANET file `ltown` using the function `basp.water_load_post()`

Start an EPANET simulation using the function `water_start_post(startdate, enddate, experimentname, sensors)`.
- Arguments `startDate`, `endDate` must be in the format `YYYY-MM-DD`.
- `experimentname` must be a unique name. To 
find all reserved `experimentnames` use the function `water_start_get()`.
- Argument `sensors` must be the name of a JSON file which contains sensors information. See the [example](../exampleFiles/) provided. 
- As soon as the experiment is executed, a Grafana dashboard URL will be given.

Use the function `water_output_json_post(experimentname)` to retrieve a JSON file with the results from the EPANET simulation. 
- The `experimentname` must be a valid name that have been already used to run an EPANET simulation.

Retrieve the sensors readings using the function `water_output_sensors_post(experimentname, sensorid)`
- The `experimentname` must be a valid name that have been already used to run an EPANET simulation.
- `sensorid` must be a list of sensors ids or empty to receive the results from all sensors. A `sensorid` example: 
`["sensor_1", "sensor_2"]`
 
