-- Installs the CareWell Clinic schema: run as CAREWELL from the setup/carewell folder.
--   sqlplus carewell@formspdb @install.sql
whenever sqlerror exit failure
@@schema.sql
@@data.sql
set feedback off heading off
exec dbms_stats.gather_schema_stats(user)
select 'CareWell installed: ' || (select count(*) from patients) || ' patients, '
       || (select count(*) from appointments) || ' appointments' as result from dual;
