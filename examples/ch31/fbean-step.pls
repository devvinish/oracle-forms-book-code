-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.STEP
:ctl.done := least(nvl(:ctl.done, 0) + 25, 100);
fbean.invoke('CTL.PROGRESS', 1, 'setValue', :ctl.done);
:ctl.info := 'getValue returned ' || fbean.invoke_num('CTL.PROGRESS', 1, 'getValue');
