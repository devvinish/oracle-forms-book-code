-- @where Trigger: WHEN-TIMER-EXPIRED (form CH31_JS)
-- The WJSI server starts in a background thread of the client: check, act, and try again
if get_application_property(timer_name) = 'WJSI_JOIN' then
  if get_custom_property('CTL.WJSI', 1, 'WSJSI_IS_SERVER_UP') = 'FALSE' then
    set_custom_property('CTL.WJSI', 1, 'WSJSI_START_SERVER', '9002');    -- on localhost
  elsif get_custom_property('CTL.WJSI', 1, 'WSJSI_IS_SESSION') = 'FALSE' then
    set_custom_property('CTL.WJSI', 1, 'WSJSI_SET_SESSION_ID', 'cw-board');
    set_custom_property('CTL.WJSI', 1, 'WSJSI_BEGIN_SESSION', '9002');   -- the form joins
  else
    :ctl.session := get_custom_property('CTL.WJSI', 1, 'WSJSI_GET_SESSION_ID');
    delete_timer('WJSI_JOIN');
  end if;
end if;
