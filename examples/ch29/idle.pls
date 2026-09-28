-- @where Trigger: WHEN-EVENT-RAISED on event IDLE
:ctl.info := 'No activity since ' || to_char(sysdate - 20 / 86400, 'HH24:MI:SS');
