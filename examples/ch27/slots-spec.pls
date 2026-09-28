-- @where Program unit: SLOTS (Package Spec), form CH27_SLOTS
package slots is
  -- the half-hour slots of a doctor's day, for a block on transactional triggers
  procedure open_day(p_doctor_id number, p_day date);
  function next_slot(p_start out date, p_patient out varchar2) return boolean;
end slots;
