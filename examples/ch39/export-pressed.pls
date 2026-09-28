-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.EXPORT (form CH39_FIND)
export_block('PATIENTS', '/work/transfer/out/patients_' || to_char(sysdate, 'YYYYMMDD_HH24MI') || '.csv');
