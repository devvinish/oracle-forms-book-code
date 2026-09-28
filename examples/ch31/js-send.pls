-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.SEND (form CH31_JS)
declare
  v_js varchar2(4000);
begin
  for d in (select * from (select substr(d.first_name, 1, 1) || '. ' || d.last_name name,
                                   count(a.appt_id) n
                              from doctors d, appointments a
                             where a.doctor_id = d.doctor_id and a.status = 'BOOKED'
                               and a.appt_start >= date '2026-11-01'
                               and a.appt_start < date '2026-12-01'
                             group by d.doctor_id, d.first_name, d.last_name
                             order by n desc)
             where rownum <= 8) loop
    v_js := v_js || '{"doctor":"' || d.name || '","booked":' || d.n || '},';
  end loop;
  set_custom_property('CTL.WJSI', 1, 'WSJSI_JS_EVAL_EXPR',
                      'showBookings([' || rtrim(v_js, ',') || '])');   -- runs in the page
end;
