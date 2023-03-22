s = KIOSBaSP();
% doc WaterOutputJsonPost
%[status,response] = s.WaterAddLeakViewSetPost('dataset.yalm')
%response = s.WaterStartGet;
%response = s.WaterInputGet;
%response = WaterLoadGet(s);
%response = s.WaterClearPost;
%response1 = s.WaterDeleteDbGet;
%response1 = s.WaterBackdropGet;
%response1 = s.WaterBackdropDelete('UNITS');
%s.WaterLoadPost
%[status,response] = s.WaterControlsDelete('control 1')
%response = s.WaterBackdropUpdate('DIMENSIONS',"['2.1','2.3']");
%s.WaterDeleteDbPost("['test1']")
s.WaterLoadPost;
[status,response] = s.WaterStartWNTRPost('2021-04-01','2021-04-09','testG85','sensors.json','dataset.yaml')

% WaterOutputSensorsPost(s,'testG01','["pressure_1"]')
% WaterOutputJsonPost(s,'testG01')
%
%fid = fopen('dataset.yalm', 'r')
%data1 = fileread('dataset.yalm')

%[status,response] = s.TransportationStartViewSetPost
%s.TransportationStepsViewSetPost(100)
%[status1,response1] = s.TransportationLaneGetLengthViewSetPost('gneE11_0')
%[status1,response1] = s.TransportationLaneGetMaxSpeedViewSetPost('gneE11_0')
%[status1,response1] = s.TransportationLaneGetHCEmissionViewSetPost('gneE11_0')
%[status1,response1] = s.TransportationLaneSetLengthViewSetPost('gneE11_0',15.3)
%[status1,response1] = s.TransportationLaneSetDisallowedViewSetPost(':1212820385_3_0',"['tram', 'rail_urban', 'rail']")
%[status1,response1] = s.TransportationVehicleStateChangeLaneViewSetPost("1000000000", 0, 10)
%[status1,response1] = s.TransportationVehicleStateChangeSubLaneViewSetPost("1000000000",-1)
%[status1,response1] = s.TransportationVehicleStateSlowDownViewSetPost("1000000000",10,10)
%[status1,response1] = s.TransportationVehicleStateSetSpeedViewSetPost("1000000000",10)
%[status1,response1] = s.TransportationVehicleStateMoveToViewSetPost("1000000000",'gneE11_0',1,1)
%[status1,response1] = s.TransportationVehicleStateSetSpeedModeViewSetPost("1000000000",1)
%[status1,response1] = s.TransportationVehicleStateSetSpeedModeViewSetPost("1000000000",100)
%[status1,response1] = s.TransportationVehicleStateRemoveViewSetPost("1000000000",3)
%[status1,response1] = s.TransportationRouteAddViewSetPost('!999', "('24706084#9', '-29121886#4', '-29121886#3', '-29121886#2', '-29121886#1', '-29121886#0', '-166682861#8', '-166682861#7','-166682861#6', '-166682861#5', '-166682861#4', '-166682861#3', '-166682861#2', '426568352', '-426568355', '348513095','543574677')")
%[status1,response1] = s.TransportationVehicleStateSetStopViewSetPost("1000000000","29149366#1", 1.0, 0, -1073741824.0,0, -1073741824.0, -1073741824.0)