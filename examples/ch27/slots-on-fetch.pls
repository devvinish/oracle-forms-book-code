-- @where Trigger: ON-FETCH on block SLOTS
declare
  v_start   date;
  v_patient varchar2(61);
begin
  for i in 1 .. get_block_property('SLOTS', records_to_fetch) loop   -- rows Forms asks for
    exit when not slots.next_slot(v_start, v_patient);
    create_queried_record;                          -- a new record, status QUERY
    :slots.slot_start := v_start;
    :slots.booked_for := nvl(v_patient, 'Free');
  end loop;
end;
