-- @where Trigger: WHEN-NEW-FORM-INSTANCE (form CH31_BEAN)
declare
  v_data varchar2(2000);
begin
  for d in (select * from (select substr(d.first_name, 1, 1) || '. ' || d.last_name name,
                                   count(a.appt_id) n
                              from doctors d, appointments a
                             where a.doctor_id = d.doctor_id
                               and a.status = 'BOOKED'
                               and a.appt_start >= date '2026-11-01'
                               and a.appt_start < date '2026-12-01'
                             group by d.doctor_id, d.first_name, d.last_name
                             order by n desc)
             where rownum <= 8) loop                 -- no FETCH FIRST in Forms PL/SQL
    v_data := v_data || d.name || '=' || d.n || ';';           -- 'M. Wilson=15;...'
  end loop;
  set_custom_property('CTL.CHART', 1, 'TITLE', 'Bookings in November 2026');
  set_custom_property('CTL.CHART', 1, 'DATA', rtrim(v_data, ';'));
end;
