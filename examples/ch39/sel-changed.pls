-- @where Trigger: WHEN-CHECKBOX-CHANGED on APPOINTMENTS.SEL (form CH39_DAY)
-- the count of selected rows, kept as the user checks and unchecks
:ctl.selected := nvl(:ctl.selected, 0) + case :appointments.sel when 'Y' then 1 else -1 end;
