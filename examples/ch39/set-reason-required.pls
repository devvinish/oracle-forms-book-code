-- @where Program unit: procedure SET_REASON_REQUIRED (form CH39_BOOKING)
-- a cancelled appointment needs a reason: Required for this record only
procedure set_reason_required is
begin
  set_item_instance_property('APPOINTMENTS.REASON', to_number(:system.trigger_record), REQUIRED,
    case :appointments.status when 'CANCELLED' then PROPERTY_TRUE else PROPERTY_FALSE end);
end;
