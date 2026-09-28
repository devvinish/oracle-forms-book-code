from formkit import *
f = form('CH27_WORKLOAD', 'CareWell Clinic')
main(f, 'Bookings in November 2026', 520, 250)
w = block(f, 'WORKLOAD', table='DOCTORS', records=8, order='busiest, doctor', scroll=True)
w.setQueryDataSourceType(T.QRDA_FRM_CLEAR_QUERY_CTID)       # FROM clause query
w.setQueryDataSourceName(code_of('ch27/workload-source.pls'))
w.setInsertAllowed(False); w.setUpdateAllowed(False); w.setDeleteAllowed(False)
item(w, 'BUSIEST', 'Rank', 12, 30, 34, dt='number')
item(w, 'DOCTOR_ID', 'ID', 48, 30, 40, dt='number', primaryKey=True)   # no ROWID: a key is required
item(w, 'DOCTOR', 'Doctor', 90, 30, 130, length=61)
item(w, 'DEPT_NAME', 'Department', 222, 30, 130, length=40)
item(w, 'APPTS', 'Booked', 354, 30, 50, dt='number')
item(w, 'MINUTES', 'Minutes', 406, 30, 50, dt='number')
c = block(f, 'CTL')
item(c, 'SQL', None, 12, 196, 496, 48, kind='display', length=2000, multiLine=True)
trigger(w, 'POST-SELECT', ":ctl.sql := :system.last_query;")
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('WORKLOAD');\nexecute_query;")
save(f)
