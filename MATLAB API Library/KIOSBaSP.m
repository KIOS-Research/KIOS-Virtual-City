% KIOS BaSP API - MATLAB Library
% University of Cyprus, KIOS Research Center of Excellence
classdef KIOSBaSP
    properties
        baseURL = "http://localhost:8000/api/";
        key;
    end

    methods

        function obj = KIOSBaSP(key,url)

           if exist('key')
               obj.key = key;
           end
           if exist('url')
               obj.baseURL = url;
           end
        end

        function [status,response] = WaterGet(obj,URL)
            call=strcat(obj.baseURL,URL);
            apikey = ['Api-Key' ' ' obj.key];
            header = matlab.net.http.field.ContentTypeField( 'application/json' );
            request = matlab.net.http.RequestMessage('GET',header);
            resp = send(request,call);
            sc = resp.StatusCode;
            status = strcat('HTTP', {' '},string(sc),{' '},getReasonPhrase(sc));
            %disp(strcat('HTTP', {' '},string(sc),{' '},getReasonPhrase(sc)));
            response = resp.Body.Data;
        end
        
        function [status,response] = post(obj,url,data)
             full_url = strcat(obj.baseURL,url);
             apikey = ['Api-Key' ' ' obj.key];
             header = matlab.net.http.field.ContentTypeField( 'application/json' );
             body = matlab.net.http.MessageBody(data);
             request = matlab.net.http.RequestMessage('POST',header,body);
             options = matlab.net.http.HTTPOptions('ConnectTimeout',500);
             resp = send(request,full_url,options);
             sc = resp.StatusCode;
             status = strcat('HTTP', {' '},string(sc),{' '},getReasonPhrase(sc));
             %disp(strcat('HTTP', {' '},string(sc),{' '},getReasonPhrase(sc)));
             response = resp.Body.Data;
        end
        
        function [status,response] = delete(obj,URL)
            call=strcat(obj.baseURL,URL);
            apikey = ['Api-Key' ' ' obj.key];
            header = matlab.net.http.field.ContentTypeField( 'application/json' );
            request = matlab.net.http.RequestMessage('DELETE',header);
            resp = send(request,call);
            sc = resp.StatusCode;
            status = strcat('HTTP', {' '},string(sc),{' '},getReasonPhrase(sc));
            %disp(strcat('HTTP', {' '},string(sc),{' '},getReasonPhrase(sc)));
            response = resp.Body.Data;
        end
        
        function [status,response] = put(obj,url,data)
             full_url = strcat(obj.baseURL,url);
             apikey = ['Api-Key' ' ' obj.key];
             header = matlab.net.http.field.ContentTypeField( 'application/json' );
             body = matlab.net.http.MessageBody(data);
             request = matlab.net.http.RequestMessage('PUT',header,body);
             show(request)
             resp = send(request,full_url);
             sc = resp.StatusCode;
             status = strcat('HTTP', {' '},string(sc),{' '},getReasonPhrase(sc));
             %disp(strcat('HTTP', {' '},string(sc),{' '},getReasonPhrase(sc)));
             response = resp.Body.Data;
        end
        
        %WaterView
        function [status,response] = WaterInputGet(obj)
            %returns a list of all the editable EPANET input file fields
            url="water/input/";
            [status,response] = WaterGet(obj,url);
        end
        
        %WaterDeleteDb
        function [status,response] = WaterDeleteDbGet(obj)
            %Returns a list of all the experiments available for deleting
            url = "water/input/deletedb/";
            [status,response] = WaterGet(obj,url);
        end
        
        function [status,response] = WaterDeleteDbPost(obj,experimentname)
            %Use this function to delete experiments
            %Experimentname: Provide the expreriment name
            %"experimentname example": '[
            %    "experiment_1",
            %    "experiment_2"
            % ]'
            url = "water/input/deletedb/";
            data = struct('experimentname',experimentname);
            [status,response] = post(obj,url,data);
        end

        %WaterBackdropViewSet
        function [status,response] = WaterBackdropGet(obj,id)
            %Use this function to read a specific backdrop entry using its id
            %id: Backdrop id
            %id example : 'DIMENSIONS'
            if exist('id')
                url = ['water/input/backdrop/',id,'/'];
            else
                url = "water/input/backdrop/";
            end
            [status,response] = WaterGet(obj,url);
        end
        
        function [status,response] = WaterBackdropDelete(obj,id)
            %Use this endpoint to remove a backdrop from the database using its id
            %id: Backdrop id
            %id example : 'DIMENSIONS'
            if exist('id')
                url = ['water/input/backdrop/',id,'/'];
            else
                url = "water/input/backdrop/";
            end
            [status,response] = delete(obj,url);
        end
        
        function [status,response] = WaterBackdropUpdate(obj,id,val)
            %Use this function to update a backdrop using its id
            %id: Backdrop id
            %id example : 'DIMENSIONS'
            %val: backdrop new value
            if exist('id')
                url = ['water/input/backdrop/',id,'/'];
            else
                url = "water/input/backdrop/";
            end
            data = struct ('value',val);
            [status,response] = put(obj,url,data);
        end
        
        %WaterControlsViewSet
        function [status,response] = WaterControlsGet(obj,id)
            if exist('id')
                url = ['water/input/controls/',id,'/'];
            else
                url = "water/input/controls/";
            end
            [status,response] = WaterGet(obj,url); 
        end
        
        function [status,response] = WaterControlsDelete(obj,id)
            %Use this function to remove a control from the database using its id
            if exist('id')
                url = ['water/input/controls/',id,'/'];
            else
                url = "water/input/controls/";
            end
            [status,response] = delete(obj,url);
        end
        
        %WaterCoordinatesViewSet
        function [status,response] = WaterCoordinatesViewSetGet(obj,id)
            %Use this endpoint to read all the coordinates or a specific coordinate data from the database
            if exist('id')
                url = ['water/input/coordinates/',id,'/'];
            else
                url = "water/input/coordinates/";
            end
            [status,response] = WaterGet(obj,url);
            response = jsonencode(response);
        end
        
        function [status,response] = WaterCoordinatesViewSetUpdate(obj,id,xcoord,ycoord)
            %Use this function to update a coordinate using its id
            if exist('id')
                url = ['water/input/coordinates/',id,'/'];
            else
                url = "water/input/coordinates/";
            end
            data = struct('xcoord',xcoord,'ycoord',ycoord);
            [status,response] = put(obj,url,data);
        end
        
        function [status,response] = WaterCoordinatesViewSetDelete(obj,id)
            %Use this endpoint to remove a coordinate from the database using its id
            if exist('id')
                url = ['water/input/coordinates/',id,'/'];
            else
                url = "water/input/coordinates/";
            end
            [status,response] = delete(obj,url);
        end
        
        %WaterCurvesViewSet
        function [status,response] = WaterCurvesViewSetGet(obj,id)
            %Use this endpoint to read all the curves data from the database
            if exist('id')
                url = ['water/input/curves/',id,'/'];
            else
                url = "water/input/curves/";
            end
            [status,response] = WaterGet(obj,url);
            response = jsonencode(response);
        end
        
        %WaterEmittersViewSet
        function [status,response] = WaterEmittersViewSetGet(obj,id)
           %Use this endpoint to read all the/a specific emitters data from the database 
           if exist('id')
                url = ['water/input/emitters/',id,'/'];
            else
                url = "water/input/emitters/";
            end
            [status,response] = WaterGet(obj,url);
            response = jsonencode(response);
        end
        
        function [status,response] = WaterEmittersViewSetUpdate(obj,id,flow_coefficient)
           %Use this function to update an emitter using its id 
           if exist('id')
                url = ['water/input/emitters/',id,'/'];
            else
                url = "water/input/emitters/";
           end
            data = struct('flow_coefficient',flow_coefficient);
            [status,response] = put(obj,url,data);
        end
        
         function [status,response] = WaterEmittersViewSetDelete(obj,id)
            %Use this function to remove an emitter from the database using its id 
            if exist('id')
                url = ['water/input/emitters/',id,'/'];
            else
                url = "water/input/emitters/";
            end
            [status,response] = delete(obj,url);
         end
         
         %WaterEnergyViewSet
         function [status,response] = WaterEnergyViewSetGet(obj,id)
            %Use this endpoint to read all the/a specific energy data from the database 
            if exist('id')
                url = ['water/input/energy/',id,'/'];
            else
                url = "water/input/energy/";
            end
            [status,response] = WaterGet(obj,url);
         end
        
         function [status,response] = WaterEnergyViewSetUpdate(obj,id,value)
            %Use this function to update an energy using its id 
            if exist('id')
                url = ['water/input/energy/',id,'/'];
            else
                url = "water/input/energy/";
            end
            data = struct('value',value);
            [status,response] = put(obj,url,data);
         end
        
         function [status,response] = WaterEnergyViewSetDelete(obj,id)
            %Use this endpoint to read all the/a specific energy data from the database 
            if exist('id')
                url = ['water/input/energy/',id,'/'];
            else
                url = "water/input/energy/";
            end
            [status,response] = delete(obj,url);
         end
         
         %WaterJunctionsViewSet
         function [status,response] = WaterJunctionsViewSetGet(obj,id)
            %Use this endpoint to read all the/a specific junction data from the database 
            if exist('id')
                url = ['water/input/junctions/',id,'/'];
            else
                url = "water/input/junctions/";
            end
            [status,response] = WaterGet(obj,url);
            %response = jsonencode(response);
         end
         
         %WaterLabelsViewSet
         function [status,response] = WaterLabelsViewSetGet(obj)
            %Use this endpoint to read all the labels data from the database 
            url="water/input/labels/";
            [status,response] = WaterGet(obj,url);
         end
         
         %WaterMixingViewSet
         function [status,response] = WaterMixingViewSetGet(obj,id)
            %Use this function to read all the/a specific mixing data from the database 
            if exist('id')
                url = ['water/input/mixing/',id,'/'];
            else
                url = "water/input/mixing/";
            end
            [status,response] = WaterGet(obj,url);
         end
        
         %WaterOptionsViewSet
         function [status,response] = WaterOptionsViewSetGet(obj,id)
            %Use this endpoint to read all the/a specific options data from the database
            if exist('id')
                url = ['water/input/options/',id,'/'];
            else
                url = "water/input/options/";
            end
            [status,response] = WaterGet(obj,url);
         end
         
         %WaterPatternsViewSet
         function [status,response] = WaterPatternsViewSetGet(obj,id)
            %Use this endpoint to read all the/a specific patterns data from the database 
            if exist('id')
                url = ['water/input/patterns/',id,'/'];
            else
                url = "water/input/patterns/";
            end
            [status,response] = WaterGet(obj,url);
         end
         
         %WaterPipesViewSet
         function [status,response] = WaterPipesViewSetGet(obj,id)
            %Use this endpoint to read all the/a pipes data from the database 
            if exist('id')
                url = ['water/input/pipes/',id,'/'];
            else
                url = "water/input/pipes/";
            end
            [status,response] = WaterGet(obj,url);
         end
         
         %WaterPumpsViewSet
         function [status,response] = WaterPumpsViewSetGet(obj,id)
            %Use this endpoint to read all the/a pumps data from the database 
            if exist('id')
                url = ['water/input/pumps/',id,'/'];
            else
                url = "water/input/pumps/";
            end
            [status,response] = WaterGet(obj,url);
         end
         
         %WaterReactionsViewSet
         function [status,response] = WaterReactionsViewSetGet(obj,id)
            %Use this endpoint to read all the/a specific reactions data from the database 
            if exist('id')
                url = ['water/input/reactions/',id,'/'];
            else
                url = "water/input/reactions/";
            end
            [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = WaterReactionsViewSetUpdate(obj,id,value)
            %Use this endpoint to read all the/a specific reactions data from the database 
            if exist('id')
                url = ['water/input/reactions/',id,'/'];
            else
                url = "water/input/reactions/";
            end
            data = struct('value',value);
            [status,response] = put(obj,url,data);
         end
         
         function [status,response] = WaterReactionsViewSetDelete(obj,id)
            %Use this endpoint to remove a reaction from the database using its id 
            if exist('id')
                url = ['water/input/reactions/',id,'/'];
            else
                url = "water/input/reactions/";
            end
            [status,response] = delete(obj,url);
         end
         
         %WaterReportViewSet
         function [status,response] = WaterReportViewSetGet(obj,id)
            %Use this endpoint to read all the/a specific reports data from the database 
            if exist('id')
                url = ['water/input/report/',id,'/'];
            else
                url = "water/input/report/";
            end
            [status,response] = WaterGet(obj,url);
         end
         
         %WaterReservoirsViewSet
         function [status,response] = WaterReservoirsViewSetGet(obj,id)
            %Use this function to read all the/a specific reservoirs data from the database 
            if exist('id')
                url = ['water/input/reservoirs/',id,'/'];
            else
                url = "water/input/reservoirs/";
            end
            [status,response] = WaterGet(obj,url);
         end
         
         %WaterSourcesViewSet
         function [status,response] = WaterSourcesViewSetGet(obj,id)
            %Use this function to read all the/a specific source data from the database 
            if exist('id')
                url = ['water/input/sources/',id,'/'];
            else
                url = "water/input/sources/";
            end
            [status,response] = WaterGet(obj,url);
         end
         
         %WaterClearDataView
         function [status,response] = WaterClearPost(obj)
            %clear the database from EPANET inp file values.
            url = 'water/clear/';
            data = struct ('clear','true');
            [status,response] = post(obj,url,data);

         end
        
         %WaterJSONFileView
         function [status,response] = WaterOutputJsonPost(obj,experimentname)
            %retrieve the EPANET JSON file generated
            %from EPANET binary file
            %experimentname : provide the experiment name

            url = 'water/output/json/';
            data = struct('experimentname',experimentname);
            [status,response] = post(obj,url,data);
            value = jsonencode(response);
            JSONFILE_name= sprintf('simulationdata.json');
            fid=fopen(JSONFILE_name,'w');
            fprintf(fid, value);
            fclose('all');
         end
        
        %WaterLoadView
        function [status,response] = WaterLoadGet(obj)
            %Returns a list of Water Start Features
            url="water/load/";
            [status,response] = WaterGet(obj,url);
        end
        
        function [status,response] = WaterLoadPost(obj)
            %load an EPANET
            url = 'water/load/';
            data = struct('file','ltown');
            [status,response] = post(obj,url,data);
        end
        
        %WaterStartView
        function [status,response] = WaterStartGet(obj)
            %Returns a list of Water Start Features
            url="water/start/";
            [status,response] = WaterGet(obj,url);
        end
        
        function [status,response] = WaterStartPost(obj,startDate,endDate,expiramentname,sensors)
            %start an EPANET simulation
            %startDate : Format YYYY-MM-DD.
            %endDate: Format YYYY-MM-DD.
            %expiramentname: provide the experiment name
            %sensors: Give the file name - example.json
            url = 'water/start/';
            fid = fopen(sensors, 'r');
            data1 = fileread(sensors);
            data2 = regexprep(data1,'[\n\t]+','');
            fclose(fid);
            data = struct('startdate',startDate,'enddate',endDate,'experimentname',expiramentname, 'sensors', data2);
            [status,response] = post(obj,url,data);
        end

        function [status,response] = WaterStartWNTRPost(obj,startDate,endDate,expiramentname,sensors, leakages)
            %start a WNTR simulation
            %startDate : Format YYYY-MM-DD.
            %endDate: Format YYYY-MM-DD.
            %expiramentname: provide the experiment name
            %sensors: Give the file name - example.json
            %leakages: provide the leakages yaml file
            url = 'water/startwntr/';
            fid = fopen(sensors, 'r');
            data1 = fileread(sensors);
            data2 = regexprep(data1,'[\n\t]+','');
            fclose(fid);
            if exist('leakages')
                fid = fopen(leakages, 'r');
                data3 = fileread(leakages);
                data4 = regexprep(data3,'[\n\t]+','');
                fclose(fid);
                data = struct('startdate',startDate,'enddate',endDate,'experimentname',expiramentname, 'leakages', data4, 'sensors', data2);
            else
                data = struct('startdate',startDate,'enddate',endDate,'experimentname',expiramentname, 'leakages', '', 'sensors', data2);
            end
            [status,response] = post(obj,url,data);
        end
        
        %WaterStepExecution
        
        
        %WaterTanksViewSet
        function [status,response] = WaterTanksViewSetGet(obj,id)
            %Use this endpoint to read all the/a specific tanks data from the database 
            if exist('id')
                url = ['water/input/tanks/',id,'/'];
            else
                url = "water/input/tanks/";
            end
            [status,response] = WaterGet(obj,url);
        end
        
        %WaterValvesViewSet
        function [status,response] = WaterValvesViewSetGet(obj,id)
            %Use this endpoint to read all the/a specific valves data from the database 
            if exist('id')
                url = ['water/input/valves/',id,'/'];
            else
                url = "water/input/valves/";
            end
            [status,response] = WaterGet(obj,url);
        end
        
        %WaterTimesViewSet
        function [status,response] = WaterTimesViewSetGet(obj,id)
            %Use this endpoint to read all the/a specific times data from the database 
            if exist('id')
                url = ['water/input/times/',id,'/'];
            else
                url = "water/input/times/";
            end
            [status,response] = WaterGet(obj,url);
        end
        
        %WaterAddLeakViewSet
        function [status,response] = WaterAddLeakViewSetGet(obj)
            %Use this function to a list of Water Start Features 
            url = "water/input/leak/";
            [status,response] = WaterGet(obj,url);
        end
        
        function [status,response] = WaterAddLeakViewSetPost(obj,file)
            %file: Give the file name - dataset_configuration.yalm
            url = "water/input/leak/";
            fid = fopen(file, 'r');
            data1 = fileread(file);
            %data2 = regexprep(data1,'[\n\t]+','');
            %fclose(fid);
            data = struct('file',data1);
            [status,response] = post(obj,url,data);
        end
        
        %WaterOutputLinksViewSet
        
        
        %WaterOutputSensorsValuesViewSet
        function [status,response] = OutputSensorsGet(obj)
            %Returns a list of Water Start Features
            url="water/output/sensors/";
            [status,response] = WaterGet(obj,url);
        end

        function [status,response] = WaterOutputSensorsPost(obj,experimentname,sensorid)
            %Here you can retrieve EPANET simulation sensor readings
            %experimentname: provide the experiment name
            %"sensorid": "provide a list of sensor ids, or leave empty to receive all of them",
            %"sensorid example": [
            %    "sensor_1",
            %    "sensor_2"
            % ]
            url = 'water/output/sensors/';
            tf = strcmp(sensorid,'');
            if tf
                data = struct('experimentname',experimentname);
            else 
                data = struct('experimentname',experimentname,'sensorid',sensorid);
            end
            [status,response] = post(obj,url,data);
            value = jsonencode(response);
        end
        
        
        %TransportationStartViewSet
        function [status,response] = TransportationStartViewSetGet(obj)
           url = "transportation/start/";
           [status,response] = WaterGet(obj,url);
        end
        
        function [status,response] = TransportationStartViewSetPost(obj)
           url = "transportation/start/";
           data = "";
           [status,response] = post(obj,url,data);
        end
        
        %TransportationStepsViewSet
        function [status,response] = TransportationStepsViewSetGet(obj)
           url = "transportation/input/steps/";
           [status,response] = WaterGet(obj,url);
        end
        
        function [status,response] = TransportationStepsViewSetPost(obj,steps)
            %Move simulation time
           url = "transportation/input/steps/";
           data = struct('steps',steps);
           [status,response] = post(obj,url,data);
        end
        
        %TransportationLaneGetLengthViewSet
        function [status,response] = TransportationLaneGetLengthViewSetGet(obj)
           url = "transportation/output/lane/getLength/";
           [status,response] = WaterGet(obj,url);
        end
        
         function [status,response] = TransportationLaneGetLengthViewSetPost(obj,id)
             %Returns the lane's length in m
             %id: Provide a lane id
           url = "transportation/output/lane/getLength/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
        
         %TransportationLaneGetMaxSpeedViewSet
         function [status,response] = TransportationLaneGetMaxSpeedViewSetGet(obj)
           url = "transportation/output/lane/getMaxSpeed/";
           [status,response] = WaterGet(obj,url);
         end
        
         function [status,response] = TransportationLaneGetMaxSpeedViewSetPost(obj,id)
             %Returns the maximum allowed speed on the lane in m/s.
             %id: Provide a lane id
           url = "transportation/output/lane/getMaxSpeed/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneGetCO2EmissionViewSet
         function [status,response] = TransportationLaneGetCO2EmissionViewSetGet(obj)
           url = "transportation/output/lane/getCO2Emission/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneGetCO2EmissionViewSetPost(obj,id)
             %Returns the CO2 emission in mg for the last time step on the given lane.
             %id: Provide a lane id
           url = "transportation/output/lane/getCO2Emission/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
         
        %TransportationLaneGetCOEmissionViewSet
          function [status,response] = TransportationLaneGetCOEmissionViewSetGet(obj)
           url = "transportation/output/lane/getCOEmission/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneGetCOEmissionViewSetPost(obj,id)
             %Returns the CO emission in mg for the last time step on the given lane.
             %id: Provide a lane id
           url = "transportation/output/lane/getCOEmission/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneGetHCEmissionViewSet
         function [status,response] = TransportationLaneGetHCEmissionViewSetGet(obj)
           url = "transportation/output/lane/getHCEmission/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneGetHCEmissionViewSetPost(obj,id)
             %Returns the HC emission in mg for the last time step on the given lane.
             %id: Provide a lane id
           url = "transportation/output/lane/getHCEmission/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneGetPMxEmissionViewSet
         function [status,response] = TransportationLaneGetPMxEmissionViewSetGet(obj)
           url = "transportation/output/lane/getPMxEmission/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneGetPMxEmissionViewSetPost(obj,id)
             %Returns the particular matter emission in mg for the last time step on the given lane.
             %id: Provide a lane id
           url = "transportation/output/lane/getPMxEmission/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneGetNOxEmissionViewSet
         function [status,response] = TransportationLaneGetNOxEmissionViewSetGet(obj)
           url = "transportation/output/lane/getNOxEmission/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneGetNOxEmissionViewSetPost(obj,id)
             %Returns the N0x emission in mg for the last time step on the given lane.
             %id: Provide a lane id
           url = "transportation/output/lane/getNOxEmission/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneGetFuelConsumptionViewSet
        function [status,response] = TransportationLaneGetFuelConsumptionViewSetGet(obj)
           url = "transportation/output/lane/getFuelConsumption/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneGetFuelConsumptionViewSetPost(obj,id)
             %Returns the fuel consumption in ml for the last time step on the given lane.
             %id: Provide a lane id
           url = "transportation/output/lane/getFuelConsumption/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneGetNoiseEmissionViewSet
         function [status,response] = TransportationLaneGetNoiseEmissionViewSetGet(obj)
           url = "transportation/output/lane/getNoiseEmission/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneGetNoiseEmissionViewSetPost(obj,id)
             %Returns the noise emission in db for the last time step on the given lane.
             %id: Provide a lane id
           url = "transportation/output/lane/getNoiseEmission/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneGetElectricityConsumptionViewSet
         function [status,response] = TransportationLaneGetElectricityConsumptionViewSetGet(obj)
           url = "transportation/output/lane/getElectricityConsumption/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneGetElectricityConsumptionViewSetPost(obj,id)
             %Returns the electricity consumption in ml for the last time step on the given lane.
             %id: Provide a lane id
           url = "transportation/output/lane/getElectricityConsumption/";
           data = struct('laneID',id);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneGetIDListViewSet
         function [status,response] = TransportationLaneGetIDListViewSetGet(obj)
             %Returns a list of all objects in the network
           url = "transportation/output/lane/getIDList/";
           [status,response] = WaterGet(obj,url);
         end
         
         %TransportationLaneGetIDCountViewSet
         function [status,response] = TransportationLaneGetIDCountViewSetGet(obj)
             %Returns the number of all lanes in the network
           url = "transportation/output/lane/getIDCount/";
           [status,response] = WaterGet(obj,url);
         end
         
         %TransportationLaneSetAllowedViewSet
         function [status,response] = TransportationLaneSetAllowedViewSetGet(obj)
           url = "transportation/input/lane/setAllowed/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneSetAllowedViewSetPost(obj,id,allowedClasses)
             %Sets a list of allowed vehicle classes.
             %id: Provide a lane id
             %allowedClasses': 'provide a list of allowed vehicle classes, or leave empty which means means all vehicles are allowed',
             %'allowedClasses_example': "['class_1', 'class_2"']"
           url = "transportation/input/lane/setAllowed/";
           data = struct('laneID',id,'allowedClasses',allowedClasses);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneSetDisallowedViewSet
         function [status,response] = TransportationLaneSetDisallowedViewSetGet(obj)
           url = "transportation/input/lane/setDisallowed/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneSetDisallowedViewSetPost(obj,id,disallowedClasses)
             %Sets a list of disallowed vehicle classes.
             %id: Provide a lane id
             %disallowedClasses': 'provide a list of disallowed vehicle classes, or leave empty which means means all vehicles are allowed',
             %'allowedClasses_example': "['class_1', 'class_2"']"
           url = "transportation/input/lane/setDisallowed/";
           data = struct('laneID',id,'disallowedClasses',disallowedClasses);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneSetLengthViewSet
         function [status,response] = TransportationLaneSetLengthViewSetGet(obj)
           url = "transportation/input/lane/setLength/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneSetLengthViewSetPost(obj,id,length)
             %Sets the length of the lane in m
             %id: Provide a lane id
             %length: 'provide the lane length
           url = "transportation/input/lane/setLength/";
           data = struct('laneID',id,'length',length);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationLaneSetMaxSpeedViewSet
          function [status,response] = TransportationLaneSetMaxSpeedViewSetGet(obj)
           url = "transportation/input/lane/setMaxSpeed/";
           [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationLaneSetMaxSpeedViewSetPost(obj,id,speed)
             %Sets a new maximum allowed speed on the lane in m/s.
             %id: Provide a lane id
             %speed: provide a maximum allowed speed on the lane in m/s
           url = "transportation/input/lane/setMaxSpeed/";
           data = struct('laneID',id,'speed',speed);
           [status,response] = post(obj,url,data);
         end
         
         %TransportationTrafficlightGetIDListViewSet
         function [status,response] = TransportationTrafficlightGetIDListViewSetGet(obj)
            %Returns a list of all objects in the network
            url = "transportation/output/trafficlight/getIDList/";
            [status,response] = WaterGet(obj,url);
         end
         
         %TransportationTrafficlightGetIDCountViewSet
         function [status,response] = TransportationTrafficlightGetIDCountViewSetGet(obj)
            % Returns the number of currently loaded objects
            url = "transportation/output/trafficlight/getIDCount/";
            [status,response] = WaterGet(obj,url);
         end
         
         %TransportationTrafficlightGetRedYellowGreenStateViewSet
         function [status,response] = TransportationTrafficlightGetRedYellowGreenStateViewSetGet(obj)
            %
            url = "transportation/output/trafficlight/getRedYellowGreenState/";
            [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationTrafficlightGetRedYellowGreenStateViewSetPost(obj,tlsID)
            %Returns the named tl's state as a tuple of light definitions from
            %rugGyYoO, for red, yed-yellow, green, yellow, off, where lower case letters mean that the stream
            %has to decelerate.
            url = "transportation/output/trafficlight/getRedYellowGreenState/";
            data = struct('tlsID',tlsID); 
            [status,response] = post(obj,url,data);
         end
         
         %TransportationTrafficlightGetPhaseDurationViewSet
         function [status,response] = TransportationTrafficlightGetPhaseDurationViewSetGet(obj)
            %
            url = "transportation/output/trafficlight/getPhaseDuration/";
            [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationTrafficlightGetPhaseDurationViewSetPost(obj,tlsID)
            %Returns the total duration of the current phase (in seconds). This value
            %is not affected by the elapsed or remaining duration of the current phase
            url = "transportation/output/trafficlight/getPhaseDuration/";
            data = struct('tlsID',tlsID); 
            [status,response] = post(obj,url,data);
         end
         
         %TransportationTrafficlightGetPhaseViewSet
         function [status,response] = TransportationTrafficlightGetPhaseViewSetGet(obj)
            url = "transportation/output/trafficlight/getPhase/";
            [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationTrafficlightGetPhaseViewSetPost(obj,tlsID)
            %Returns the index of the current phase within the list of all phases of the current program
            url = "transportation/output/trafficlight/getPhase/";
            data = struct('tlsID',tlsID); 
            [status,response] = post(obj,url,data);
         end
         
         %TransportationTrafficlightSetRedYellowGreenStateViewSet
         function [status,response] = TransportationTrafficlightSetRedYellowGreenStateViewSetGet(obj)
            url = "transportation/input/trafficlight/setRedYellowGreenState/";
            [status,response] = WaterGet(obj,url);
         end
         
         function [status,response] = TransportationTrafficlightSetRedYellowGreenStateViewSetPost(obj,tlsID,state)
            %Sets the named tl's state as a tuple of light definitions from 
            %rugGyYuoO, for red, red-yellow, green, yellow, off, where lower
            %case letters mean that the stream has to decelerate.
            url = "transportation/input/trafficlight/setRedYellowGreenState/";
            data = struct('tlsID',tlsID,'state',state); 
            [status,response] = post(obj,url,data);
         end
         
         %TransportationTrafficlightSetLinkStateViewSet
          function [status,response] = TransportationTrafficlightSetLinkStateViewSetGet(obj)
            url = "transportation/input/trafficlight/setLinkState/";
            [status,response] = WaterGet(obj,url);
          end
         
          function [status,response] = TransportationTrafficlightSetLinkStateViewSetPost(obj,tlsID,tlsLinkIndex,state)
            %Sets the state for the given tls and link index.
            url = "transportation/input/trafficlight/setLinkState/";
            data = struct('tlsID',tlsID,'tlsLinkIndex',tlsLinkIndex,'state',state); 
            [status,response] = post(obj,url,data);
          end
         
          %TransportationTrafficlightSetPhaseViewSet
          function [status,response] = TransportationTrafficlightSetPhaseViewSetGet(obj)
            url = "transportation/input/trafficlight/setPhase/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationTrafficlightSetPhaseViewSetPost(obj,tlsID,index)
            %Switches to the phase with the given index in the list of all phases for the current program.
            url = "transportation/input/trafficlight/setPhase/";
            data = struct('tlsID',tlsID,'index',index); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationTrafficlightSetPhaseDurationViewSet
          function [status,response] = TransportationTrafficlightSetPhaseDurationViewSetGet(obj)
            url = "transportation/input/trafficlight/setPhaseDuration/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationTrafficlightSetPhaseDurationViewSetPost(obj,tlsID,phaseDuration)
            %Set the remaining phase duration of the current phase in seconds.
            %This value has no effect on subsquent repetitions of this phase
            url = "transportation/input/trafficlight/setPhaseDuration/";
            data = struct('tlsID',tlsID,'phaseDuration',phaseDuration); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetIDCountViewSet
          function [status,response] = TransportationVehicleGetIDCountViewSetGet(obj)
              %Returns the number of vehicles currently running within the scenario
            url = "transportation/output/vehicle/getIDCount/";
            [status,response] = WaterGet(obj,url);
          end
          
          %TransportationVehicleGetIDListViewSet
          function [status,response] = TransportationVehicleGetIDListViewSetGet(obj)
              %Returns a list of ids of all vehicles currently running within the scenario
            url = "transportation/output/vehicle/getIDList/";
            [status,response] = WaterGet(obj,url);
          end
          
          %TransportationVehicleGetSpeedViewSet
          function [status,response] = TransportationVehicleGetSpeedViewSetGet(obj)
            url = "transportation/output/vehicle/getSpeed/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetSpeedViewSetPost(obj,vehID)
            %Returns the (longitudinal) speed in m/s of the named vehicle within the last step.
            url = "transportation/output/vehicle/getSpeed/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetAccelerationViewSet
          function [status,response] = TransportationVehicleGetAccelerationViewSetGet(obj)
            url = "transportation/output/vehicle/getAcceleration/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetAccelerationViewSetPost(obj,vehID)
            %Returns the acceleration in m/s^2 of the named vehicle within the last step
            url = "transportation/output/vehicle/getAcceleration/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetPositionViewSet
          function [status,response] = TransportationVehicleGetPositionViewSetGet(obj)
            url = "transportation/output/vehicle/getPosition/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetPositionViewSetPost(obj,vehID)
            %Returns the position of the named vehicle within the last step [m,m].
            url = "transportation/output/vehicle/getPosition/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetCO2EmissionViewSet
          function [status,response] = TransportationVehicleGetCO2EmissionViewSetGet(obj)
            url = "transportation/output/vehicle/getCO2Emission/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetCO2EmissionViewSetPost(obj,vehID)
            %Returns the CO2 emission in mg/s for the last time step.
            %Multiply by the step length to get the value for one step.
            url = "transportation/output/vehicle/getCO2Emission/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetCOEmissionViewSet
          function [status,response] = TransportationVehicleGetCOEmissionViewSetGet(obj)
            url = "transportation/output/vehicle/getCOEmission/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetCOEmissionViewSetPost(obj,vehID)
            %Returns the CO emission in mg/s for the last time step.
            %Multiply by the step length to get the value for one step.
            url = "transportation/output/vehicle/getCOEmission/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetHCEmissionViewSet
          function [status,response] = TransportationVehicleGetHCEmissionViewSetGet(obj)
            url = "transportation/output/vehicle/getHCEmission/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetHCEmissionViewSetPost(obj,vehID)
            %Returns the HC emission in mg/s for the last time step.
            %Multiply by the step length to get the value for one step.
            url = "transportation/output/vehicle/getHCEmission/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetPMxEmissionViewSet
          function [status,response] = TransportationVehicleGetPMxEmissionViewSetGet(obj)
            url = "transportation/output/vehicle/getPMxEmission/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetPMxEmissionViewSetPost(obj,vehID)
            %Returns the PMx emission in mg/s for the last time step.
            %Multiply by the step length to get the value for one step.
            url = "transportation/output/vehicle/getPMxEmission/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetNOxEmissionViewSet
           function [status,response] = TransportationVehicleGetNOxEmissionViewSetGet(obj)
            url = "transportation/output/vehicle/getNOxEmission/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetNOxEmissionViewSetPost(obj,vehID)
            %Returns the NOx emission in mg/s for the last time step.
            %Multiply by the step length to get the value for one step.
            url = "transportation/output/vehicle/getNOxEmission/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetFuelConsumptionViewSet
          function [status,response] = TransportationVehicleGetFuelConsumptionViewSetGet(obj)
            url = "transportation/output/vehicle/getFuelConsumption/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetFuelConsumptionViewSetPost(obj,vehID)
            %Returns the fuel consumption in ml/s for the last time step.
            %Multiply by the step length to get the value for one step.
            url = "transportation/output/vehicle/getFuelConsumption/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetNoiseEmissionViewSet
          function [status,response] = TransportationVehicleGetNoiseEmissionViewSetGet(obj)
            url = "transportation/output/vehicle/getNoiseEmission/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetNoiseEmissionViewSetPost(obj,vehID)
            %Returns the noise emission in db for the last time step.
            url = "transportation/output/vehicle/getNoiseEmission/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleGetElectricityConsumptionViewSet
          function [status,response] = TransportationVehicleGetElectricityConsumptionViewSetGet(obj)
            url = "transportation/output/vehicle/getElectricityConsumption/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleGetElectricityConsumptionViewSetPost(obj,vehID)
            %Returns the electricity consumption in Wh/s for the last time step.
            %Multiply by the step length to get the value for one step
            url = "transportation/output/vehicle/getElectricityConsumption/";
            data = struct('vehID',vehID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleStateSetStopViewSet
          function [status,response] = TransportationVehicleStateSetStopViewSetGet(obj)
            url = "transportation/input/vehicle/setStop/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleStateSetStopViewSetPost(obj,vehID,edgeID,pos,laneIndex,duration,flags,startPos,until)
            %Adds or modifies a stop with the given parameters
            url = "transportation/input/vehicle/setStop/";
            data = struct('vehID',vehID,'edgeID',edgeID,'pos',pos,'laneIndex',laneIndex,'duration',duration,'flags',flags,'startPos',startPos,'until',until); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleStateChangeLaneViewSet
          function [status,response] = TransportationVehicleStateChangeLaneViewSetGet(obj)
            url = "transportation/input/vehicle/changeLane/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleStateChangeLaneViewSetPost(obj,vehID,laneIndex,duration)
            %Forces a lane change to the lane with the given index
            %if successful,the lane will be chosen for the given amount of time (in s)."
            url = "transportation/input/vehicle/changeLane/";
            data = struct('vehID',vehID,'laneIndex',laneIndex,'duration',duration); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleStateChangeSubLaneViewSet
          function [status,response] = TransportationVehicleStateChangeSubLaneViewSetGet(obj)
            url = "transportation/input/vehicle/changeSubLane/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleStateChangeSubLaneViewSetPost(obj,vehID,latDist)
            %a lateral change by the given amount (negative values indicate changing to the right, positive to the left).
            %This will override any other lane change motivations but conform to safety-constraints as configured by laneChangeMode.
            url = "transportation/input/vehicle/changeSubLane/";
            data = struct('vehID',vehID,'latDist',latDist); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleStateSlowDownViewSet
          function [status,response] = TransportationVehicleStateSlowDownViewSetGet(obj)
            url = "transportation/input/vehicle/slowDown/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleStateSlowDownViewSetPost(obj,vehID,speed,duration)
            %Changes the speed smoothly to the given value over the given amount
            %of time in seconds (can also be used to increase speed).
            url = "transportation/input/vehicle/slowDown/";
            data = struct('vehID',vehID,'speed',speed,'duration',duration); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleStateSetSpeedViewSet
          function [status,response] = TransportationVehicleStateSetSpeedViewSetGet(obj)
            url = "transportation/input/vehicle/setSpeed/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleStateSetSpeedViewSetPost(obj,vehID,speed)
            %Sets the speed in m/s for the named vehicle within the last step.
            %Calling with speed=-1 hands the vehicle control back to SUMO.
            url = "transportation/input/vehicle/setSpeed/";
            data = struct('vehID',vehID,'speed',speed); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleStateMoveToViewSet
          function [status,response] = TransportationVehicleStateMoveToViewSetGet(obj)
            url = "transportation/input/vehicle/MoveTo/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleStateMoveToViewSetPost(obj,vehID,laneID,pos,reason)
            %Move a vehicle to a new position along it's current route.
            url = "transportation/input/vehicle/MoveTo/";
            data = struct('vehID',vehID,'laneID',laneID,'pos',pos,'reason',reason); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleStateSetSpeedModeViewSet
          function [status,response] = TransportationVehicleStateSetSpeedModeViewSetGet(obj)
            url = "transportation/input/vehicle/setSpeedMode/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleStateSetSpeedModeViewSetPost(obj,vehID,sm)
            %Sets the vehicle's speed mode as a bitset.
            url = "transportation/input/vehicle/setSpeedMode/";
            data = struct('vehID',vehID,'sm',sm); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleStateSetMaxSpeedViewSet
          function [status,response] = TransportationVehicleStateSetMaxSpeedViewSetGet(obj)
            url = "transportation/input/vehicle/setMaxSpeed/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleStateSetMaxSpeedViewSetPost(obj,vehID,speed)
            %Sets the maximum speed in m/s for this vehicle.
            url = "transportation/input/vehicle/setMaxSpeed/";
            data = struct('vehID',vehID,'speed',speed); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationVehicleStateRemoveViewSet
          function [status,response] = TransportationVehicleStateRemoveViewSetGet(obj)
            url = "transportation/input/vehicle/Remove/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationVehicleStateRemoveViewSetPost(obj,vehID,reason)
            %Remove vehicle with the given ID for the give reason. 
            %Reasons are defined in module constants and start with REMOVE
            url = "transportation/input/vehicle/Remove/";
            data = struct('vehID',vehID,'reason',reason); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationRouteGetIDListViewSet
          function [status,response] = TransportationRouteGetIDListViewSetGet(obj)
            %Returns a list of all routes in the network
            url = "transportation/output/route/getIDList/";
            [status,response] = WaterGet(obj,url);
          end
          
          %TransportationRouteGetIDCountViewSet
          function [status,response] = TransportationRouteGetIDCountViewSetGet(obj)
            %Returns the number of all routes in the network
            url = "transportation/output/route/getIDCount/";
            [status,response] = WaterGet(obj,url);
          end
          
          %TransportationRouteGetEdgesViewSet
          function [status,response] = TransportationRouteGetEdgesViewSetGet(obj)
            url = "transportation/output/route/getEdges/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationRouteGetEdgesViewSetPost(obj,routeID)
            %Returns a list of all edges in the route.
            url = "transportation/output/route/getEdges/";
            data = struct('routeID',routeID); 
            [status,response] = post(obj,url,data);
          end
          
          %TransportationRouteAddViewSet
          function [status,response] = TransportationRouteAddViewSetGet(obj)
            url = "transportation/input/route/add/";
            [status,response] = WaterGet(obj,url);
          end
          
          function [status,response] = TransportationRouteAddViewSetPost(obj,routeID,edges)
            %Adds a new route with the given id consisting of the given list of edge IDs
            url = "transportation/input/route/add/";
            data = struct('routeID',routeID,'edges',edges); 
            [status,response] = post(obj,url,data);
          end
         
    end
end
