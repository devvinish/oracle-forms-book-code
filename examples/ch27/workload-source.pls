-- @where Block WORKLOAD: Query Data Source Name (Query Data Source Type: FROM clause query)
(select d.doctor_id,
        d.first_name || ' ' || d.last_name as doctor,
        dp.dept_name,
        count(a.appt_id) as appts,
        nvl(sum(a.duration_min), 0) as minutes,
        rank() over (order by count(a.appt_id) desc) as busiest
 from   doctors d
        join departments dp on dp.dept_id = d.dept_id
        left join appointments a
          on  a.doctor_id = d.doctor_id
          and a.status = 'BOOKED'
          and a.appt_start >= date '2026-11-01' and a.appt_start < date '2026-12-01'
 group  by d.doctor_id, d.first_name, d.last_name, dp.dept_name)
