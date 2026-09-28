-- @ APPF_NEW: WHEN-NEW-FORM-INSTANCE
-- the share of all appointments in each status, for the gauges
declare
  v_rg recordgroup;
  v_n  number;
begin
  select round(100 * count(case when status = 'COMPLETED' then 1 end) / count(*)),
         round(100 * count(case when status = 'BOOKED' then 1 end) / count(*)),
         round(100 * count(case when status = 'NO_SHOW' then 1 end) / count(*))
    into :ctl.completed, :ctl.booked, :ctl.no_show
    from appointments;
  -- the combo box lists the specialties of the clinic's doctors
  v_rg := create_group_from_query('RG_SPECIALTIES',
            'select distinct specialty, specialty from doctors order by 1');
  v_n := populate_group(v_rg);
  populate_list('CTL.SPECIALTY', v_rg);
  go_block('DOCTORS');
  execute_query;
end;
