# CH39_VISIT: a visit with its prescription, and a button that repeats the prescription of the previous
# visit (Chapter 39, recipe 8)
from formkit import *
f = form('CH39_VISIT', 'CareWell Clinic')
main(f, 'Visit', 560, 300)
pp = ModuleParameter(f, 'P_PATIENT_ID')
pp.setParameterDataType(T.PADA_NUMBER_CTID); pp.setParameterInitializeValue('10145')
v = block(f, 'VISITS', table='VISITS', where='patient_id = :parameter.p_patient_id', order='visit_date desc')
item(v, 'VISIT_ID', None, dt='number', cnv=None)
item(v, 'PATIENT_ID', None, dt='number', cnv=None, initializeValue=':PARAMETER.P_PATIENT_ID')
item(v, 'PATIENT_NAME', 'Patient', 70, 10, 150, length=61, db=False, insertAllowed=False, updateAllowed=False,
     keyboardNavigable=False, edge='start')
item(v, 'VISIT_DATE', 'Visit date', 70, 34, 80, dt='date', formatMask='DD-MON-YYYY', initializeValue='$$DATE$$',
     required=True, edge='start')
item(v, 'DOCTOR_ID', 'Doctor ID', 300, 34, 44, dt='number', required=True, edge='start')
item(v, 'DIAGNOSIS', 'Diagnosis', 70, 58, 274, length=200, edge='start')
trigger(v, 'POST-QUERY', "select first_name || ' ' || last_name into :visits.patient_name\n"
        "  from patients where patient_id = :visits.patient_id;")
trigger(v, 'PRE-INSERT', ':visits.visit_id := visits_seq.nextval;')
trigger(v, 'WHEN-CREATE-RECORD', "select first_name || ' ' || last_name into :visits.patient_name\n"
        "  from patients where patient_id = :parameter.p_patient_id;")
c = block(f, 'CTL')
b = item(c, 'REPEAT', 'Repeat Last Prescription', 360, 56, 170, 22, kind='button', mouseNavigate=False,
         keyboardNavigable=False)
trigger(b, 'WHEN-BUTTON-PRESSED', file='ch39/repeat-prescription.pls')
r = block(f, 'PRESCRIPTIONS', table='PRESCRIPTIONS', records=6, order='rx_id')
item(r, 'RX_ID', None, dt='number', cnv=None)
item(r, 'VISIT_ID', None, dt='number', cnv=None)
item(r, 'MEDICINE_ID', 'Med.', 12, 110, 40, dt='number', required=True)
item(r, 'MEDICINE_NAME', 'Medicine', 54, 110, 140, length=40, db=False, insertAllowed=False, updateAllowed=False,
     keyboardNavigable=False)
item(r, 'DOSAGE', 'Dosage', 196, 110, 90, length=30, required=True)
item(r, 'FREQUENCY', 'Frequency', 288, 110, 110, length=20, required=True)
item(r, 'DAYS', 'Days', 400, 110, 36, dt='number', required=True)
item(r, 'QUANTITY', 'Qty', 438, 110, 36, dt='number', required=True)
trigger(r, 'POST-QUERY', "select medicine_name into :prescriptions.medicine_name\n"
        "  from medicines where medicine_id = :prescriptions.medicine_id;")
trigger(r, 'PRE-INSERT', ':prescriptions.rx_id := prescriptions_seq.nextval;')
relations(f, v, [dict(name='VISITS_PRESCRIPTIONS', block='PRESCRIPTIONS', table='PRESCRIPTIONS',
                     join=[('VISIT_ID', 'VISIT_ID')], delete='cascading')])
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('VISITS');\nexecute_query;")
save(f)
