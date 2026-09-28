-- @where Trigger: POST-QUERY on APPOINTMENTS
declare
  type t_names is table of varchar2(30);
  items t_names := t_names('APPT_START', 'PATIENT_NAME', 'STATUS', 'REASON');
  va    varchar2(30);
  rec   number := to_number(:system.trigger_record);
begin
  select first_name || ' ' || last_name
  into   :appointments.patient_name
  from   patients
  where  patient_id = :appointments.patient_id;

  va := case :appointments.status when 'CANCELLED' then 'VA_CANCELLED'
                                  when 'NO_SHOW'   then 'VA_NO_SHOW' end;
  if va is not null then
    for i in 1 .. items.count loop
      set_item_instance_property('APPOINTMENTS.' || items(i), rec, visual_attribute, va);
    end loop;
  end if;
end;
