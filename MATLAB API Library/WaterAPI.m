clear all; close all; clc;

s = KIOSBaSP();
s.WaterLoadGet
s.WaterLoadPost
[status SavedNames]=s.WaterStartGet;
% Names=jsondecode(SavedNames)
ReservedNames=SavedNames.reserved_list;

%% User input data
fileName = 'sensors.json'; % filename in JSON extension
leakagefile='dataset_configuration.yaml';
sensors = fileread(fileName); % dedicated for reading files as text 
data = jsondecode(sensors); %

try
[Type]=LoadOrNew()
 catch
    ff = msgbox('Process Canceled','help','modal');
    posin = get(ff, 'Position');
    set(ff, 'Position', posin+[0 0 40 0]) 
    return
    end
TypeInd=find(contains(Type,'Load'));

if TypeInd==1
    
    try
    [Expname]=LoadExperiment(ReservedNames)
    catch
    ff = msgbox('Process Canceled','help','modal');
    posin = get(ff, 'Position');
    set(ff, 'Position', posin+[0 0 40 0]) 
    return
    end

else
    
    try
    [Expname,fromD,toD]=NewExperiment(ReservedNames)
    catch
    ff = msgbox('Process Canceled','help','modal');
    posin = get(ff, 'Position');
    set(ff, 'Position', posin+[0 0 40 0]) 
    return
    end

startDate=datestr(fromD,'yyyy-mm-dd');
endDate=datestr(toD,'yyyy-mm-dd')';
expiramentname=Expname;

%Add Leakage
% [status,response] = s.WaterAddLeakViewSetPost('dataset_configuration.yalm')

s.WaterStartWNTRPost(startDate,endDate,expiramentname,fileName,leakagefile)
% s.WaterStartPost(startDate, endDate, expiramentname,fileName)
end

expiramentname=Expname;

%% Simulation
[status sensordata]=s.WaterOutputSensorsPost(expiramentname,'');
Datetime={sensordata(1).values.timestamp}';
Datetime=datetime(Datetime, 'InputFormat', 'yyyy-MM-dd''T''HH:mm:ss''Z');
%% Data clustering
SensorID={sensordata.sensorid}';
% SensorType={data.sensors.sensortype};
% ModelID={data.sensors.id};

presInd_TS = find(contains(SensorID,'pressure'));
AMRInd_TS = find(contains(SensorID,'demand'));
FlowInd_TS = find(contains(SensorID,'flow'));
levelInd_TS=find(contains(SensorID,'level'));
reservoirInd_TS=find(contains(SensorID,'reservoir'));



%% Load Sensor Data

%Load Pressure Sensor Data
dim=ceil(sqrt(length(presInd_TS)));
figure;
for i=1:length(presInd_TS)
pressure(:,i)=cell2mat({sensordata(presInd_TS(i)).values.value});
subplot(dim,dim,i)
plot(Datetime,pressure(:,i))
title(['',SensorID{presInd_TS(i)},''], 'Interpreter', 'none')
ylabel('m')
% axis tight
grid on
end
suptitle('Pressure (m)')
drawnow

%Load Flow Sensor Data
dim=ceil(sqrt(length(FlowInd_TS)));
figure;
for i=1:length(FlowInd_TS)
flow(:,i)=cell2mat({sensordata(FlowInd_TS(i)).values.value});
subplot(dim,dim,i)
plot(Datetime,flow(:,i))
title(['',SensorID{FlowInd_TS(i)},''], 'Interpreter', 'none')
ylabel('m3/h')
% axis tight
grid on
end
suptitle('Flow (m3/h)')
drawnow

%Load Demad Sensor Data
dim=ceil(sqrt(length(AMRInd_TS)));
figure;
for i=1:length(AMRInd_TS)
demand(:,i)=cell2mat({sensordata(AMRInd_TS(i)).values.value});
subplot(dim,dim,i)
plot(Datetime,demand(:,i))
title(['',SensorID{AMRInd_TS(i)},''], 'Interpreter', 'none')
ylabel('m3/h')
% axis tight
grid on
end
suptitle('Demand (m3/h)')
drawnow

%Load Reservoir Sensor Data
dim=ceil(sqrt(length(reservoirInd_TS)));
figure;
for i=1:length(reservoirInd_TS)
reservoir(:,i)=cell2mat({sensordata(reservoirInd_TS(i)).values.value});
subplot(dim,dim,i)
plot(Datetime,reservoir(:,i))
title(['',SensorID{reservoirInd_TS(i)},''], 'Interpreter', 'none')
ylabel('m')
% axis tight
grid on
end
suptitle('Reservoir Pressure (m)')
drawnow

%Load Reservoir Sensor Data
dim=ceil(sqrt(length(levelInd_TS)));
figure;
for i=1:length(levelInd_TS)
level(:,i)=cell2mat({sensordata(levelInd_TS(i)).values.value});
subplot(dim,dim,i)
plot(Datetime,level(:,i))
title(['',SensorID{levelInd_TS(i)},''], 'Interpreter', 'none')
ylabel('m')
% axis tight
grid on
end
suptitle('Tank Pressure (m)')
drawnow