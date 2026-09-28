from formkit import *
f = form('CH10_DOCTOR', 'CareWell Clinic')
main(f, 'Doctor', 400, 170)
d = block(f, 'DOCTORS', table='DOCTORS', order='doctor_id')
item(d, 'DOCTOR_ID', 'ID', 80, 12, 50, dt='number', edge='start', updateAllowed=False)
item(d, 'FIRST_NAME', 'Name', 80, 32, 100, length=30, edge='start')
item(d, 'LAST_NAME', None, 184, 32, 110, length=30)
# a spin list: the arrows step through the departments
dp = item(d, 'DEPT_ID', 'Department', 80, 56, 150, dt='number', kind='list', edge='start',
          listStyle=T.LSST_SPINLIST_CTID)
for i, (v, lbl) in enumerate([(100, 'General Medicine'), (101, 'Cardiology'), (102, 'Pediatrics'),
                              (103, 'Orthopedics'), (104, 'Dermatology'), (105, 'ENT'),
                              (106, 'Gynecology'), (107, 'Diagnostics')]):
    dp.insertElement(i + 1, lbl, str(v))
# a slider: whole numbers between a minimum and a maximum
fee = item(d, 'CONSULT_FEE', 'Fee', 80, 82, 200, 20, dt='number', kind='list', edge='start',
           listStyle=T.LSST_SLIDER_CTID, uiMinval=0, uiMaxval=200, uiIncrement=5)
item(d, 'FEE_SHOWN', None, 286, 84, 40, dt='number', kind='display', db=False,
     calculateMode=T.CAMO_FORMULA_CTID, formula=':doctors.consult_fee')
# a check box: Y when checked, N when not
ac = item(d, 'ACTIVE', 'Active', 80, 112, 80, kind='check', length=1)
ac.setCheckedValue('Y'); ac.setUncheckedValue('N')
ac.setCheckBoxOtherValues(T.CHECKBOX_ILLEGAL_CTID)
ac.setInitializeValue('Y')
trigger(ac, 'WHEN-CHECKBOX-CHANGED', file='ch10/active-changed.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('DOCTORS');\nexecute_query;")
save(f)
