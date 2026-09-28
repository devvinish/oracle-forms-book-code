-- @where Trigger: WHEN-NEW-FORM-INSTANCE on the form
declare
  rg     recordgroup;
  c_min  groupcolumn;
  c_desc groupcolumn;
  type t_mins is table of number;
  mins   t_mins := t_mins(10, 15, 20, 30, 45, 60);
begin
  rg     := create_group('RG_DURATIONS_RT');
  c_min  := add_group_column(rg, 'MINUTES', number_column);
  c_desc := add_group_column(rg, 'DESCRIPTION', char_column, 30);
  for i in 1 .. mins.count loop
    add_group_row(rg, end_of_group);
    set_group_number_cell(c_min, i, mins(i));
    set_group_char_cell(c_desc, i,
      case when mins(i) <= 15 then 'Follow-up' when mins(i) <= 30 then 'Consultation'
           else 'Procedure' end);
  end loop;
  set_lov_property('LOV_DURATIONS', group_name, 'RG_DURATIONS_RT');
  go_item('APPOINTMENTS.PATIENT_NAME');
end;
