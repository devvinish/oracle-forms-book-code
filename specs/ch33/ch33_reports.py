from formkit import *
from oracle.forms.jdapi import Report
f = form('CH33_REPORTS', 'CareWell Clinic')
main(f, 'Appointment Schedule', 420, 170)
c = block(f, 'CTL')
item(c, 'P_FROM', 'From', 70, 12, 80, dt='date', formatMask='DD-MON-YYYY', edge='start')
item(c, 'P_TO', 'To', 220, 12, 80, dt='date', formatMask='DD-MON-YYYY', edge='start')
b = item(c, 'RUN', 'Run Report', 70, 40, 100, 20, kind='button')
item(c, 'JOB', 'Job', 70, 76, 200, kind='display', length=100, edge='start')
item(c, 'STATUS', 'Status', 70, 96, 200, kind='display', length=100, edge='start')
item(c, 'URL', 'Output', 70, 116, 330, kind='display', length=400, edge='start')
r = Report(f, 'APPT_SCHEDULE')                     # the report object
r.setFilename('/work/reports/cw_appt_schedule.rdf')
r.setReportObjectType(0)                           # Oracle Reports, not Analytics Publisher
r.setCommMode(T.COMO_SYNCH_CTID)
r.setExecuteMode(T.EXMO_BATCH_CTID)
r.setReportDestinationType(T.RPDE_CACHE_CTID)
r.setReportDestinationFormat('PDF')
r.setReportServer('rep_wls_reports_formslab')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch33/new-form.pls')
trigger(b, 'WHEN-BUTTON-PRESSED', file='ch33/run-report.pls')
save(f)
