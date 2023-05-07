# KIOS BaSP API - Python Library
# University of Cyprus, KIOS Research Center of Excellence

import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class KiosBasp:

    def __init__(self, url=None, key=None):
        """
        Initialize the library

        Parameters:
        url (string): The url for the API. Leave empty to use the default
        key (string): The API Key. Leave empty to not use an API Key

        Returns:
        int: Description of return value

        """

        if url is None:
            self.baseURL = "http://localhost:8000/api/"
        else:
            self.baseURL = url

        self.headers = {"Authorization": 'Api-Key {}'.format(key)}

    def change_baseURL(self, url):
        """
        Change the base URL of the API

        Parameters:
        url (string): The base URL to use (with "http://")

        """

        self.baseURL = url

    def post(self, url, data, headers=None):
        """
        Perform a post request

        Parameters:
        url (string): The endpoint url
        data: the data to be send to the server
        header: The header for the request

        Returns:
        response: Returns the response from the server

        """

        if headers is None:
            headers = self.headers
        res = requests.post(self.baseURL + url, data=data, headers=headers)
        status="HTTP "+ str(res.status_code)+ " "+ str(res.reason)
        try:
            return status, res.json()
        except:
            return status, None

    def put(self, url, data, headers=None):
        """
        Perform a post request

        Parameters:
        url (string): The endpoint url
        data: the data to be send to the server
        header: The header for the request

        Returns:
        response: Returns the response from the server

        """

        if headers is None:
            headers = self.headers
        res = requests.put(self.baseURL + url, data=data, headers=headers)
        status="HTTP "+ str(res.status_code)+ " "+ str(res.reason)
        try:
            return status, res.json()
        except:
            return status, None

    def delete(self, url, headers=None):
        """
        Perform a delete request

        Parameters:
        url (string): The endpoint url
        data: the data to be send to the server
        header: The header for the request

        Returns:
        response: Returns the response from the server

        """

        if headers is None:
            headers = self.headers
        res = requests.delete(self.baseURL + url, headers=headers)
        status="HTTP "+ str(res.status_code)+ " "+ str(res.reason)
        try:
            return status, res.json()
        except:
            return status, None

    def water_load_post(self):
        """
        Load EPANET inp file

        Returns:
        response: Returns the response from the server

        """

        url = "water/load/"
        data = {'file': 'ltown'}
        response = self.post(url, data)
        return response

    def water_clear_post(self):
        """
        Use this API endpoint to clear the database from EPANET inp file values. Set Clear field to true for cleaning the database.

        Returns:
        response: Returns the response from the server

        """

        url = "water/clear/"
        data = {'clear': 'true'}
        response = self.post(url, data)
        return response

    def water_start_post(self, startdate, enddate, experimentname, sensors):
        """
        Start an EPANET simulation

        Parameters:
        startdate (YYYY-MM-DD): The start date of the simulation
        enddate (YYYY-MM-DD): The end date of the simulation
        experimentname (string): provide the experiment name
        sensors (string): Provide the name of the file with the sensors

        Returns:
        response: Returns the response from the server

        """

        url = "water/start/"
        file = open(sensors, 'rb')
        sensors_data = file.read()
        file.close()
        fields = {'startdate': startdate,
                  'enddate': enddate,
                  'experimentname': experimentname,
                  'sensors': sensors_data
                  }
        data = MultipartEncoder(
            fields
        )
        headers1 = self.headers.copy()
        headers1['Content-Type'] = data.content_type

        response = self.post(url, data, headers1)
        return response

    def water_output_sensors_post(self, experimentname, sensorid=None):
        """
        Retrieve EPANET simulation sensor readings

        Parameters:
        experimentname (string): provide the experiment name
        sensorid (list): provide a list of sensor ids, or leave empty to receive all of them
        "sensorid_example": [
            "sensor_1",
            "sensor_2"
        ]
        Returns:
        response: Returns the readings from the sensors

        """

        url = "water/output/sensors/"
        if sensorid is None:
            data = {'experimentname': experimentname}
        else:
            data = {'experimentname': experimentname,
                    'sensorid': sensorid.__str__()}

        response = self.post(url, data)
        return response

    def water_output_json_post(self, experimentname):
        """
        Use this API endpoint to retrieve the EPANET JSON file generated from EPANET binary file

        Parameters:
        experimentname (string): provide the experiment name

        Returns:
        json: JSON file generated from EPANET binary file
        response: Returns the response from the server

        """

        url = "water/output/json/"
        data = {'experimentname': experimentname}

        response = self.post(url, data)

        if 'status' not in response:
            file = open("simulationdata.json", 'w')
            json.dump(response, file)
        return response

    def get(self, url):
        """
        Perform a get request

        Parameters:
        url (string): The endpoint url

        Returns:
        response: Returns the response from the server

        """

        full_url = self.baseURL + url
        res = requests.get(full_url, headers=self.headers)
        status="HTTP "+ str(res.status_code)+ " "+ str(res.reason)
        try:
            return status,res.json()
        except:
            return status, None


    def water_input_get(self):
        """
        This endpoint returns a list of all the editable EPANET input file fields

        Returns:
        response: The fields you can edit

        """

        url = 'water/input/'
        response = self.get(url)
        return response

    def water_load_get(self):
        """
        Returns a list of Water Start Features

        """

        url = 'water/load/'
        response = self.get(url)
        return response

    def water_start_get(self):
        """
        Returns a list of Water Start Features

        Returns:
        response: The values in the reserved list are not allowed as experiment names

        """

        url = 'water/start'
        response = self.get(url)
        return response

    def water_output_sensors_get(self):
        """
        Returns a list of Water Start Features

        """

        url = 'water/output/sensors'
        response = self.get(url)
        return response

    def water_input_deletedb_get(self):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        url = 'water/input/deletedb/'
        status, response = self.get(url)
        return status, response

    def water_input_deletedb_post(self, experimentname):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/deletedb/'
        data = {'experimentname': experimentname.__str__()}
        status, response = self.post(url, data)
        return status, response

    def water_input_backdrop_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/backdrop/'+str(id)
        else:
            url = 'water/input/backdrop/'
        status, response = self.get(url)
        return status, response

    def water_input_backdrop_delete(self, id):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/backdrop/'+str(id)
        status, response = self.delete(url)
        return status, response

    #todo
    def water_input_backdrop_update(self, id, value):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/backdrop/'+str(id)+'/'
        data = {'value': value.__str__()}
        status, response = self.put(url, data)
        return status, response

    def water_input_controls_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/controls/'+str(id)+"/"
        else:
            url = 'water/input/controls/'
        status, response = self.get(url)
        return status, response

    def water_input_controls_delete(self, id):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/controls/'+str(id)+'/'
        status, response = self.delete(url)
        return status, response

    #todo
    def water_input_controls_update(self, id, value):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/controls/'+str(id)+'/'
        data = {'value': value.__str__()}
        status, response = self.put(url, data)
        return status, response

    # todo
    def water_input_controls_create(self, id, value):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/controls/' + str(id) + '/'
        data = {'value': value.__str__()}
        status, response = self.post(url, data)
        return status, response


    def water_input_coordinates_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/coordinates/'+str(id)+"/"
        else:
            url = 'water/input/coordinates/'
        status, response = self.get(url)
        return status, response

    def water_input_coordinates_delete(self, id):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/coordinates/'+str(id)+'/'
        status, response = self.delete(url)
        return status, response

    def water_input_coordinates_update(self, id, xcoord, ycoord):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/coordinates/'+str(id)+'/'
        data = {'xcoord': xcoord, 'ycoord':ycoord}
        status, response = self.put(url, data)
        return status, response


    def water_input_curves_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/curves/'+str(id)+"/"
        else:
            url = 'water/input/curves/'
        status, response = self.get(url)
        return status, response


    def water_input_emitters_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/emitters/'+str(id)+"/"
        else:
            url = 'water/input/emitters/'
        status, response = self.get(url)
        return status, response

    def water_input_emitters_delete(self, id):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/emitters/'+str(id)+'/'
        status, response = self.delete(url)
        return status, response

    def water_input_emitters_update(self, id, flow_coefficient):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/emitters/'+str(id)+'/'
        data = {'flow_coefficient': flow_coefficient}
        status, response = self.put(url, data)
        return status, response


    def water_input_energy_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/energy/'+str(id)+"/"
        else:
            url = 'water/input/energy/'
        status, response = self.get(url)
        return status, response

    def water_input_energy_delete(self, id):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/energy/'+str(id)+'/'
        status, response = self.delete(url)
        return status, response

    def water_input_energy_update(self, id, value):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/energy/'+str(id)+'/'
        data = {'value': value}
        status, response = self.put(url, data)
        return status, response


    def water_input_junctions_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/junctions/'+str(id)+"/"
        else:
            url = 'water/input/junctions/'
        status, response = self.get(url)
        return status, response


    def water_input_labels_get(self):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        url = 'water/input/labels/'
        status, response = self.get(url)
        return status, response


    def water_input_mixing_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/mixing/'+str(id)+"/"
        else:
            url = 'water/input/mixing/'
        status, response = self.get(url)
        return status, response


    def water_input_options_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/options/'+str(id)+"/"
        else:
            url = 'water/input/options/'
        status, response = self.get(url)
        return status, response


    def water_input_patterns_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/patterns/'+str(id)+"/"
        else:
            url = 'water/input/patterns/'
        status, response = self.get(url)
        return status, response


    def water_input_pipes_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/pipes/'+str(id)+"/"
        else:
            url = 'water/input/pipes/'
        status, response = self.get(url)
        return status, response


    def water_input_pumps_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/pumps/'+str(id)+"/"
        else:
            url = 'water/input/pumps/'
        status, response = self.get(url)
        return status, response


    def water_input_reactions_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/reactions/'+str(id)+"/"
        else:
            url = 'water/input/reactions/'
        status, response = self.get(url)
        return status, response

    def water_input_reactions_delete(self, id):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/reactions/'+str(id)+'/'
        status, response = self.delete(url)
        return status, response

    def water_input_reactions_update(self, id, value):
        """
        Here you can delete experiments from BaSP

        Parameters:
        experimentname (list): provide the experiment names to be deleted

        Returns:
        response: Returns the response from the server

        """

        url = 'water/input/reactions/'+str(id)+'/'
        data = {'value': value}
        status, response = self.put(url, data)
        return status, response


    def water_input_report_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/report/'+str(id)+"/"
        else:
            url = 'water/input/report/'
        status, response = self.get(url)
        return status, response


    def water_input_reservoirs_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/reservoirs/'+str(id)+"/"
        else:
            url = 'water/input/reservoirs/'
        status, response = self.get(url)
        return status, response


    def water_input_sources_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/sources/'+str(id)+"/"
        else:
            url = 'water/input/sources/'
        status, response = self.get(url)
        return status, response


    def water_input_sources_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/sources/'+str(id)+"/"
        else:
            url = 'water/input/sources/'
        status, response = self.get(url)
        return status, response


    def water_stepexecution_get(self):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        url = 'water/stepexecution/'
        status, response = self.get(url)
        return status, response


    def water_stepexecution_post(self,startdate,timestep,iterations,timestep_size,experiment_name,sensors):
        """
        Load EPANET inp file

        Returns:
        response: Returns the response from the server

        """

        url = "water/stepexecution/"
        file = open(sensors, 'rb')
        sensors_data = file.read()
        file.close()
        data = {'startdate': startdate,'timestep':timestep, 'iterations':iterations,'timestep_size':timestep_size,'experiment_name':experiment_name,'sensors':sensors_data}
        response = self.post(url, data)
        return response


    def water_input_tanks_get(self, id=None):
        """
        Here you can delete experiments from BaSP

        Returns a list of Experiments Names

        """

        if id!=None:
            url = 'water/input/tanks/'+str(id)+"/"
        else:
            url = 'water/input/tanks/'
        status, response = self.get(url)
        return status, response


    def water_input_valves_get(self, id=None):
        """
        Use this endpoint to read all the or a specific valves data from the database

        """

        if id!=None:
            url = 'water/input/valves/'+str(id)+"/"
        else:
            url = 'water/input/valves/'
        status, response = self.get(url)
        return status, response


    def water_input_times_get(self, id=None):
        """
        Use this endpoint to read all the or a specific times data from the database

        """

        if id!=None:
            url = 'water/input/times/'+str(id)+"/"
        else:
            url = 'water/input/times/'
        status, response = self.get(url)
        return status, response


    def water_input_leak_get(self):
        """
        Returns a list of Water Start Features

        """

        url = 'water/input/leak/'
        status, response = self.get(url)
        return status, response


    def water_input_leak_post(self,file):
        """


        """

        url = "water/stepexecution/"
        f = open(file, 'rb')
        file_data = f.read()
        f.close()
        data = {'file':file_data}
        response = self.post(url, data)
        return response


    def TransportationLaneGetLengthViewSet_get(self):
        """


        """

        url = 'transportation/output/lane/getLength/'
        status, response = self.get(url)
        return status, response


    def TransportationLaneGetLengthViewSet_post(self,laneID):
        """
        Get the lane's length in m
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getLength/'

        data = {'laneID':laneID}
        response = self.post(url, data)
        return response

    def TransportationLaneGetMaxSpeedViewSet_get(self):
        """


        """

        url = 'transportation/output/lane/getMaxSpeed/'
        status, response = self.get(url)
        return status, response

    def TransportationLaneGetMaxSpeedViewSet_post(self, laneID):
        """
        Get the lane's maximum allowed speed
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getMaxSpeed/'

        data = {'laneID': laneID}
        response = self.post(url, data)
        return response


    def TransportationLaneGetCO2EmissionViewSet_get(self):
        """
        """

        url = 'transportation/output/lane/getCO2Emission/'
        status, response = self.get(url)
        return status, response

    def TransportationLaneGetCO2EmissionViewSet_post(self, laneID):
        """
        Get the CO2 emission in mg for the last time step on the given lane.
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getCO2Emission/'

        data = {'laneID': laneID}
        response = self.post(url, data)
        return response


    def TransportationLaneGetCOEmissionViewSet_get(self):
        """
        """

        url = 'transportation/output/lane/getCOEmission/'
        status, response = self.get(url)
        return status, response

    def TransportationLaneGetCOEmissionViewSet_post(self, laneID):
        """
        Get the CO emission in mg for the last time step on the given lane.
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getCOEmission/'

        data = {'laneID': laneID}
        response = self.post(url, data)
        return response


    def TransportationLaneGetHCEmissionViewSet_get(self):
        """
        """

        url = 'transportation/output/lane/getHCEmission/'
        status, response = self.get(url)
        return status, response

    def TransportationLaneGetHCEmissionViewSet_post(self, laneID):
        """
        Get the HC emission in mg for the last time step on the given lane.
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getHCEmission/'

        data = {'laneID': laneID}
        response = self.post(url, data)
        return response


    def TransportationLaneGetPMxEmissionViewSet_get(self):
        """
        """

        url = 'transportation/output/lane/getPMxEmission/'
        status, response = self.get(url)
        return status, response

    def TransportationLaneGetPMxEmissionViewSet_post(self, laneID):
        """
        Get the PMx emission in mg for the last time step on the given lane.
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getPMxEmission/'

        data = {'laneID': laneID}
        response = self.post(url, data)
        return response


    def TransportationLaneGetNOxEmissionViewSet_get(self):
        """
        """

        url = 'transportation/output/lane/getNOxEmission/'
        status, response = self.get(url)
        return status, response

    def TransportationLaneGetNOxEmissionViewSet_post(self, laneID):
        """
        Get the NOx emission in mg for the last time step on the given lane.
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getNOxEmission/'

        data = {'laneID': laneID}
        response = self.post(url, data)
        return response


    def TransportationLaneGetFuelConsumptionViewSet_get(self):
        """
        """

        url = 'transportation/output/lane/getFuelConsumption/'
        status, response = self.get(url)
        return status, response

    def TransportationLaneGetFuelConsumptionViewSet_post(self, laneID):
        """
        Get the fuel consumption in ml for the last time step on the given lane.
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getFuelConsumption/'

        data = {'laneID': laneID}
        response = self.post(url, data)
        return response


    def TransportationLaneGetNoiseEmissionViewSet_get(self):
        """
        """

        url = 'transportation/output/lane/getNoiseEmission/'
        status, response = self.get(url)
        return status, response

    def TransportationLaneGetNoiseEmissionViewSet_post(self, laneID):
        """
        Get the noise emission in db for the last time step on the given lane.
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getNoiseEmission/'

        data = {'laneID': laneID}
        response = self.post(url, data)
        return response


    def TransportationLaneGetElectricityConsumptionViewSet_get(self):
        """
        """

        url = 'transportation/output/lane/getElectricityConsumption/'
        status, response = self.get(url)
        return status, response

    def TransportationLaneGetElectricityConsumptionViewSet_post(self, laneID):
        """
        Get the electricity consumption in ml for the last time step on the given lane.
        laneID: provide a lane id

        """

        url = 'transportation/output/lane/getElectricityConsumption/'

        data = {'laneID': laneID}
        response = self.post(url, data)
        return response


    def TransportationLaneGetIDListViewSet_get(self):
        """
        Get a list of all lanes in the network

        """

        url = 'transportation/output/lane/getIDList/'
        status, response = self.get(url)
        return status, response


    def TransportationLaneGetIDCountViewSet_get(self):
        """
        Get the number of all lanes in the network

        """

        url = 'transportation/output/lane/getIDCount/'
        status, response = self.get(url)
        return status, response


    def TransportationTrafficlightGetIDListViewSet_get(self):
        """
        Get a list of all lanes in the network

        """

        url = 'transportation/output/trafficlight/getIDList/'
        status, response = self.get(url)
        return status, response


    def TransportationTrafficlightGetIDCountViewSet_get(self):
        """
        Get the number of all lanes in the network

        """

        url = 'transportation/output/trafficlight/getIDCount/'
        status, response = self.get(url)
        return status, response


    def TransportationTrafficlightGetRedYellowGreenStateViewSet_get(self):
        """
        """

        url = 'transportation/output/trafficlight/getRedYellowGreenState/'
        status, response = self.get(url)
        return status, response

    def TransportationTrafficlightGetRedYellowGreenStateViewSet_post(self, tlsID):
        """
        Get the traffic light state.

        Return: the named tl's state as a tuple of light definitions from
        rugGyYoO, for red, yed-yellow, green, yellow, off, where lower case letters mean that the stream
        has to decelerate.

        tlsID: Provide a traffic light id

        """

        url = 'transportation/output/trafficlight/getRedYellowGreenState/'

        data = {'tlsID': tlsID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetIDCountViewSet_get(self):
        """
        Get the number of vehicles currently running within the scenario

        """

        url = 'transportation/output/vehicle/getIDCount/'
        status, response = self.get(url)
        return status, response


    def TransportationVehicleGetIDListViewSet_get(self):
        """
        Get a list of ids of all vehicles currently running within the scenario

        """

        url = 'transportation/output/vehicle/getIDList/'
        status, response = self.get(url)
        return status, response


    def TransportationTrafficlightGetPhaseDurationViewSet_get(self):
        """
        """

        url = 'transportation/output/trafficlight/getPhaseDuration/'
        status, response = self.get(url)
        return status, response

    def TransportationTrafficlightGetPhaseDurationViewSet_post(self, tlsID):
        """
        Get the total duration of the current phase (in seconds). This value
        is not affected by the elapsed or remaining duration of the current phase.

        tlsID: Provide a traffic light id

        """

        url = 'transportation/output/trafficlight/getPhaseDuration/'

        data = {'tlsID': tlsID}
        response = self.post(url, data)
        return response


    def TransportationTrafficlightGetPhaseViewSet_get(self):
        """
        """

        url = 'transportation/output/trafficlight/getPhase/'
        status, response = self.get(url)
        return status, response

    def TransportationTrafficlightGetPhaseViewSet_post(self, tlsID):
        """
        Get the total duration of the current phase (in seconds). This value
        is not affected by the elapsed or remaining duration of the current phase.

        tlsID: Provide a traffic light id

        """

        url = 'transportation/output/trafficlight/getPhase/'

        data = {'tlsID': tlsID}
        response = self.post(url, data)
        return response


    def TransportationTrafficlightSetRedYellowGreenStateViewSet_get(self):
        """
        """

        url = 'transportation/input/trafficlight/setRedYellowGreenState/'
        status, response = self.get(url)
        return status, response

    def TransportationTrafficlightSetRedYellowGreenStateViewSet_post(self, tlsID, state):
        """
        Set the named tl's state as a tuple of light definitions.

        tlsID: Provide a traffic light id
        state: A tuple of light definitions from rugGyYuoO, for red, red-yellow, green, yellow, off, where lower case letters mean that the stream has to decelerate.

        """

        url = 'transportation/input/trafficlight/setRedYellowGreenState/'

        data = {'tlsID': tlsID, 'state': state}
        response = self.post(url, data)
        return response


    def TransportationTrafficlightSetLinkStateViewSet_get(self):
        """
        """

        url = 'transportation/input/trafficlight/setLinkState/'
        status, response = self.get(url)
        return status, response

    def TransportationTrafficlightSetLinkStateViewSet_post(self, tlsID, state):
        """
        Set the state for the given tls and link index.

        tlsID: Provide a traffic light id
        state: A tuple of light definitions from rugGyYuoO, for red, red-yellow, green, yellow, off, where lower case letters mean that the stream has to decelerate.
        tlsLinkIndex: The link index is shown in the GUI when setting the appropriate junction visualization option.

        """

        url = 'transportation/input/trafficlight/setLinkState/'

        data = {'tlsID': tlsID, 'state': state}
        response = self.post(url, data)
        return response


    def TransportationTrafficlightSetPhase_post(self, tlsID, index):
        """
        Switch to the phase with the given index in the list of all phases for
        the current program.

        tlsID: Provide a traffic light id

        """

        url = 'transportation/input/trafficlight/setPhase/'

        data = {'tlsID': tlsID, 'index': index}
        response = self.post(url, data)
        return response


    def TransportationTrafficlightSetPhaseDuration_post(self, tlsID, phaseDuration):
        """
        Set the remaining phase duration of the current phase in seconds. This value has no effect on subsquent repetitions of this phase.

        tlsID: Provide a traffic light id
        phaseDuration: Provide phase duration of the current phase in seconds.

        """

        url = 'transportation/input/trafficlight/setPhaseDuration/'

        data = {'tlsID': tlsID, 'phaseDuration': phaseDuration}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetSpeed_post(self, vehID):
        """
        Get the speed of the named vehicle within the last step [m/s]

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getSpeed/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetAcceleration_post(self, vehID):
        """
        Get the acceleration in m/s^2 of the named vehicle within the last step.

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getAcceleration/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetPosition_post(self, vehID):
        """
        Get the position(two doubles) of the named vehicle (center of the front bumper) within the last step [m,m]

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getPosition/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetCO2Emission_post(self, vehID):
        """
        Get Vehicle's CO2 emissions in mg/s during this time step, to get the value for one step multiply with the step length

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getCO2Emission/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetCOEmission_post(self, vehID):
        """
        Get Vehicle's CO emissions in mg/s during this time step, to get the value for one step multiply with the step length

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getCOEmission/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetHCEmission_post(self, vehID):
        """
        Get Vehicle's HC emissions in mg/s during this time step, to get the value for one step multiply with the step length

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getHCEmission/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetPMxEmission_post(self, vehID):
        """
        Get Vehicle's PMx emissions in mg/s during this time step, to get the value for one step multiply with the step length

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getPMxEmission/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetNOxEmission_post(self, vehID):
        """
        Get Vehicle's NOx emissions in mg/s during this time step, to get the value for one step multiply with the step length

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getNOxEmission/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response

    def TransportationVehicleGetFuelConsumption_post(self, vehID):
        """
        Get Vehicle's fuel consumption in ml/s during this time step, to get the value for one step multiply with the step length

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getFuelConsumption/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetNoiseEmission_post(self, vehID):
        """
        Get Vehicle's noise emission in db for the last time step

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getNoiseEmission/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleGetElectricityConsumption_post(self, vehID):
        """
        Get Vehicle's electricity consumption in Wh/s during this time step, to get the value for one step multiply with the step length

        vehID: Provide a vehicle id

        """

        url = 'transportation/output/vehicle/getElectricityConsumption/'

        data = {'vehID': vehID}
        response = self.post(url, data)
        return response


    def TransportationVehicleStateSetStop_post(self, vehID, edgeID, pos,laneIndex,duration,startPos,until,flags=None):
        """
        Lets the vehicle stop at the given edge, at the given position and lane.
        The vehicle will stop for the given duration. Re-issuing a stop command with the same lane and position allows changing the duration.
        Setting the duration to 0 cancels an existing stop.

        vehID: Provide a vehicle id
        edgeID: Provide an edge id
        pos: Provide a position
        laneIndex:Provide the lane Index
        duration:How long the vehicle will stop
        flags:
        startPos:Provide the start position in seconds
        until:in seconds

        """

        url = 'transportation/input/vehicle/setStop/'

        data = {'vehID': vehID,
                'edgeID': edgeID,
                'pos' : pos,
                'laneIndex': laneIndex,
                'duration': duration,
                'flags': flags,
                'startPos': startPos,
                'until': until
                }
        response = self.post(url, data)
        return response


    def TransportationVehicleStateChangeLane_post(self, vehID,laneIndex,duration):
        """
        Forces a lane change to the lane with the given index; if successful,the lane will be chosen for the given amount of time (in s).

        vehID: Provide a vehicle id
        laneIndex:Provide the lane Index
        duration:the lane will be chosen for the given amount of time (in s)

        """

        url = 'transportation/input/vehicle/changeLane/'

        data = {'vehID': vehID,
                'laneIndex': laneIndex,
                'duration': duration,
                }
        response = self.post(url, data)
        return response


    def TransportationVehicleStateChangeSubLane_post(self, vehID,latDist):
        """
        Forces a lateral change by the given amount (negative values indicate changing to the right, positive to the left).
        This will override any other lane change motivations but conform to safety-constraints as configured by laneChangeMode.

        vehID: Provide a vehicle id
        latDist:

        """

        url = 'transportation/input/vehicle/changeSubLane/'

        data = {'vehID': vehID,
                'latDist': latDist,
                }
        response = self.post(url, data)
        return response


    def TransportationVehicleStateSlowDown_post(self, vehID,speed,duration):
        """
        Changes the speed smoothly to the given value over the given amount of time in seconds (can also be used to increase speed).

        vehID: Provide a vehicle id
        speed: Provide the value of the speed
        duration':Provide the duration in seconds

        """

        url = 'transportation/input/vehicle/slowDown/'

        data = {'vehID': vehID,
                'speed': speed,
                'duration': duration
                }
        response = self.post(url, data)
        return response


    def TransportationVehicleStateSetSpeed_post(self, vehID,speed):
        """
        Sets the vehicle speed to the given value. The speed will be followed according to the current speed mode.
        By default the vehicle may drive slower than the set speed according to the safety rules of the car-follow model.
        When sending a value of -1 the vehicle will revert to its original behavior (using the maxSpeed of its vehicle type and following all safety rules).

        vehID: Provide a vehicle id
        speed: Provide the value of the speed

        """

        url = 'transportation/input/vehicle/setSpeed/'

        data = {'vehID': vehID,
                'speed': speed,
                }
        response = self.post(url, data)
        return response

    def TransportationVehicleStateMoveTo_post(self, vehID,speed,laneID, pos, reason):
        """
        Moves the vehicle to a new position along the current route

        vehID: Provide a vehicle id
        speed: Provide the value of the speed
        laneID: Provide a lane id
        pos: Provide a position
        reason: Provide a reason

        """

        url = 'transportation/input/vehicle/MoveTo/'

        data = {'vehID': vehID,
                'speed': speed,
                'laneID': laneID,
                'pos': pos,
                'reason': reason
                }
        response = self.post(url, data)
        return response


    def TransportationVehicleStateSetSpeedMode_post(self, vehID,sm):
        """
        Sets the vehicle's speed mode as a bitset.

        vehID: Provide a vehicle id
        sm: Provide the speed mode

        """

        url = 'transportation/input/vehicle/setSpeedMode/'

        data = {'vehID': vehID,
                'sm': sm
                }
        response = self.post(url, data)
        return response


    def TransportationVehicleStateSetMaxSpeed_post(self, vehID,speed):
        """
        Sets the maximum speed in m/s for this vehicle.

        vehID: Provide a vehicle id
        speed: Provide the value of the speed

        """

        url = 'transportation/input/vehicle/setMaxSpeed/'

        data = {'vehID': vehID,
                'speed': speed
                }
        response = self.post(url, data)
        return response


    def TransportationVehicleStateRemove_post(self, vehID,reason):
        """
        Remove vehicle with the given ID for the give reason. Reasons are defined in module constants and start with REMOVE_

        vehID: Provide a vehicle id
        reason: Provide the reason

        """

        url = 'transportation/input/vehicle/Remove/'

        data = {'vehID': vehID,
                'reason': reason
                }
        response = self.post(url, data)
        return response


    def TransportationRouteGetIDList_get(self):
        """
        Get a list of all routes in the network

        """

        url = 'transportation/output/route/getIDList/'

        response = self.get(url)
        return response


    def TransportationRouteGetIDCount_get(self):
        """
        Get a list of all routes in the network

        """

        url = 'transportation/output/route/getIDCount/'

        response = self.get(url)
        return response


    def TransportationRouteGetEdges_post(self, routeID):
        """
        Returns a list of all edges in the route.

        routeID: Provide a route id

        """

        url = 'transportation/output/route/getEdges/'

        data = {
                'routeID': routeID

                }
        response = self.post(url, data)
        return response


    def TransportationRouteAdd_post(self, routeID, edges):
        """
        Adds a new route with the given id consisting of the given list of edge IDs.

        routeID: Provide a route id
        edges: provide a list of edge IDs.
        edges_example: ('edge_1', 'edge_2')

        """

        url = 'transportation/input/route/add/'

        data = {
                'routeID': routeID,
                'edges': edges

                }
        response = self.post(url, data)
        return response


    def TransportationLaneSetAllowed_post(self, laneID, allowedClasses):
        """
        Sets a list of allowed vehicle classes.

        laneID: provide the lane id
        allowedClasses: provide a list of allowed vehicle classes, or leave empty which means means all vehicles are allowed
        allowedClasses_example: ["class_1", "class_2"]

        """

        url = 'transportation/input/lane/setAllowed/'

        data = {
                'laneID': laneID,
                'allowedClasses': allowedClasses

                }
        response = self.post(url, data)
        return response


    def TransportationLaneSetDisallowed_post(self, laneID, disallowedClasses):
        """
        Sets a list of disallowed vehicle classes.

        laneID: provide the lane id
        disallowedClasses: provide a list of disallowed vehicle classes, or leave empty which means means all vehicles are not allowed
        disallowedClasses_example: ['class_1', 'class_2']

        """

        url = 'transportation/input/lane/setDisallowed/'

        data = {
                'laneID': laneID,
                'disallowedClasses': disallowedClasses

                }
        response = self.post(url, data)
        return response


    def TransportationLaneSetLength_post(self, laneID, length):
        """
        Sets the length of the lane in m.

        laneID: provide the lane id
        length: provide the lane length

        """

        url = 'transportation/input/lane/setLength/'

        data = {
                'laneID': laneID,
                'length': length

                }
        response = self.post(url, data)
        return response


    def TransportationLaneSetMaxSpeed_post(self, laneID, speed):
        """
        Sets a new maximum allowed speed on the lane in m/s.

        laneID: provide the lane id
        speed: provide a maximum allowed speed on the lane in m/s

        """

        url = 'transportation/input/lane/setMaxSpeed/'

        data = {
                'laneID': laneID,
                'speed': speed

                }
        response = self.post(url, data)
        return response


    def TransportationStart_post(self):
        """
        Start Sumo simulation

        """

        url = 'transportation/start/'

        data = {
                }
        response = self.post(url, data)
        return response


    def TransportationSteps_post(self, steps):
        """
        Move simulation time

        steps: Provide the number of steps

        """

        url = 'transportation/input/steps/'

        data = {
                'steps': steps
                }
        response = self.post(url, data)
        return response
