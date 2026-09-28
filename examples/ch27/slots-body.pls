-- @where Program unit: SLOTS (Package Body), form CH27_SLOTS
package body slots is
  g_doctor number;
  g_next   date;                                  -- the next slot to return
  g_end    date;                                  -- the end of the day

  procedure open_day(p_doctor_id number, p_day date) is
  begin
    g_doctor := p_doctor_id;
    g_next   := trunc(p_day) + 9 / 24;            -- 09:00
    g_end    := trunc(p_day) + 17 / 24;           -- 17:00
  end open_day;

  function next_slot(p_start out date, p_patient out varchar2) return boolean is
  begin
    if g_next is null or g_next >= g_end then
      return false;
    end if;
    p_start := g_next;
    select min(p.first_name || ' ' || p.last_name) into p_patient
      from appointments a, patients p              -- no ANSI join in Forms PL/SQL
     where p.patient_id = a.patient_id
       and a.doctor_id = g_doctor
       and a.status <> 'CANCELLED'
       and a.appt_start < g_next + 30 / 1440
       and a.appt_start + a.duration_min / 1440 > g_next;
    g_next := g_next + 30 / 1440;
    return true;
  end next_slot;
end slots;
