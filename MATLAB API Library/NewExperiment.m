function [Expname,fromD,toD]=NewExperiment(ReservedNames)
f = figure('Name', 'Experiment Name and Simulation Period');
set(f, 'MenuBar', 'none');
set(f, 'ToolBar', 'none');
handles.Counter=0;
Info = uicontrol(f, 'Style', 'Text','FontSize',14, ...
'String', 'Experiment Input Data', ...
'Horizontalalignment', 'center', ...
'Position', [190 380 200 20]);

Info2=uicontrol(f,'Style','popupmenu', ...
'String', 'Show Reserved Names', ...
'Horizontalalignment', 'center', ...
'Position', [275 150 200 20],'String',ReservedNames);

% StartdateTextHandle = uicontrol(f, 'Style', 'Text', ...
% 'String', 'StartDate:', ...
% 'Horizontalalignment', 'left', ...
% 'Position', [80 300 50 20]);
% 
% EnddateTextHandle = uicontrol(f, 'Style', 'Text', ...
% 'String', 'EndDate:', ...
% 'Horizontalalignment', 'left', ...
% 'Position', [80 200 50 20]);

StartdateEditBoxHandle = uicontrol(f, 'Style', 'Edit', ...  
'Position', [140 300 100 20], ...  
'BackgroundColor', 'w');

EnddateEditBoxHandle = uicontrol(f, 'Style', 'Edit', ...  
'Position', [140 250 100 20], ...  
'BackgroundColor', 'w');

ExpNameEditBoxHandle = uicontrol(f, 'Style', 'Edit', ...  
'Position', [140 150 100 20], ...  
'BackgroundColor', 'w');

StartcalendarButtonHandle = uicontrol(f, 'Style', 'PushButton', ...  
'String', 'Select start date', ...  
'Position', [275 300 200 20], ...  
'callback', @startpushbutton_cb);

EndcalendarButtonHandle = uicontrol(f, 'Style', 'PushButton', ...  
'String', 'Select end date', ...  
'Position', [275 250 200 20], ...  
'callback', @endpushbutton_cb);

ExpNameButtonHandle = uicontrol(f, 'Style', 'Text', ...  
'String', 'Experiment Name', ...  
'Position', [140 175 100 20]);

ResNameButtonHandle = uicontrol(f, 'Style', 'Text', ...  
'String', 'Reserved Names', ...  
'Position', [275 175 200 20]);


SubmitButton = uicontrol(f, 'Style', 'PushButton', ...  
'String', 'Submit', ...  
'Position', [175 100 200 20], ...  
'callback', @submitpushbutton_cb);


function startpushbutton_cb(hcbo, eventStruct)  
% Create a UICALENDAR with the following properties:  
% 1) Highlight weekend dates.  
% 2) Only allow a single date to be selected at a time.  
% 3) Send the selected date to the edit box uicontrol.  
uicalendar('Weekend', [1 0 0 0 0 0 1], ...  
'SelectionType', 1, ...  
'DestinationUI', StartdateEditBoxHandle);


end  

function endpushbutton_cb(hcbo, eventStruct)  
% Create a UICALENDAR with the following properties:  
% 1) Highlight weekend dates.  
% 2) Only allow a single date to be selected at a time.  
% 3) Send the selected date to the edit box uicontrol.  
uicalendar('Weekend', [1 0 0 0 0 0 1], ...  
'SelectionType', 1, ...  
'DestinationUI', EnddateEditBoxHandle);

end 


function submitpushbutton_cb(hcbo, eventStruct,c,ReservedNames)  

fromD = get(StartdateEditBoxHandle,'String');
toD = get(EnddateEditBoxHandle,'String');
ReservedNames=get(Info2,'String');
Expname=get(ExpNameEditBoxHandle,'String');
match=find(contains(ReservedNames,Expname));

while isempty(fromD) || isempty(toD) || isempty(Expname)

    ff = msgbox('Please fill all data','WaterAnalytics','help','modal');
    posin = get(ff, 'Position');
    set(ff, 'Position', posin+[0 0 40 0]) 
         return
end

fromD=datetime(fromD,'TimeZone', 'local','Format','d-MMM-y HH:mm:ss');
toD=datetime(toD,'TimeZone', 'local','Format','d-MMM-y HH:mm:ss');

if toD>fromD
     
 else
   ff = msgbox('Please select correct dates','WaterAnalytics','help','modal');
    posin = get(ff, 'Position');
    set(ff, 'Position', posin+[0 0 40 0]) 
         return
end


 if length(match)>0
     
    ff = msgbox('Please select different experiment name','WaterAnalytics','help','modal');
    posin = get(ff, 'Position');
    set(ff, 'Position', posin+[0 0 40 0]) 
         return
end

handles.Counter = 1;

  
 return
end 





while(handles.Counter ~=1)
    try 
        x = get(StartdateEditBoxHandle,'String');
        y = get(EnddateEditBoxHandle,'String');
        t= get(ExpNameEditBoxHandle,'String');
    catch
        clear fromD;clear toD;
     return
    end
    pause(1);
end


fromD = get(StartdateEditBoxHandle,'String');
toD = get(EnddateEditBoxHandle,'String');
Expname=get(ExpNameEditBoxHandle,'String');
fromD=datetime(fromD,'TimeZone', 'local','Format','d-MMM-y HH:mm:ss');
toD=datetime(toD,'TimeZone', 'local','Format','d-MMM-y HH:mm:ss');
close(f)
     
end

