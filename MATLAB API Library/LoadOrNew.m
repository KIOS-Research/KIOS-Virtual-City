function [Type]=LoadOrNew(ReservedNames)
f = figure('Name', 'Load or Start New Experiment');
set(f, 'MenuBar', 'none');
set(f, 'ToolBar', 'none');
handles.Counter=0;

Info = uicontrol(f, 'Style', 'Text','FontSize',14, ...
'String', 'Load or Start New Experiment', ...
'Horizontalalignment', 'center', ...
'Position', [190 380 200 20]);

Info2=uicontrol(f,'Style','popupmenu', ...
'String', 'List of Experiments', ...
'Horizontalalignment', 'center', ...
'Position', [270 250 100 20],'String',{'Load Experiment', 'Start New Experiment'},'callback', @selection);

ExpNameEditBoxHandle = uicontrol(f, 'Style', 'Edit', ...  
'Position', [140 250 100 20], ...  
'BackgroundColor', 'w');

SubmitButton = uicontrol(f, 'Style', 'PushButton', ...  
'String', 'Submit', ...  
'Position', [175 100 200 20], ...  
'callback', @submitpushbutton_cb);

function [Type]=selection(src,event)
        val = Info2.Value;
        str = Info2.String;
        Type=str{val};
        
 set(ExpNameEditBoxHandle,'string',Type);
        
end

function submitpushbutton_cb(hcbo, eventStruct,c)  

Type=get(ExpNameEditBoxHandle,'String');
 

handles.Counter = 1;

 end 





while(handles.Counter ~=1)
    try 
      x = get(ExpNameEditBoxHandle,'String');  
       
    catch
        
     return
    end
    pause(1);
end


Type=get(ExpNameEditBoxHandle,'String');
close(f)
     
end

