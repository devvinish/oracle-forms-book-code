from formkit import *
f = form('CH10_PATIENT', 'CareWell Clinic')
main(f, 'Patient', 440, 250)
p = block(f, 'PATIENTS', table='PATIENTS', order='last_name, first_name')
item(p, 'MRN', 'MRN', 90, 12, 70, length=10, edge='start', updateAllowed=False)
item(p, 'FIRST_NAME', 'Name', 90, 32, 100, length=30, edge='start')
item(p, 'LAST_NAME', None, 194, 32, 110, length=30)
# a radio group: one radio button for each value of the column
g = item(p, 'GENDER', 'Gender', 90, 56, 230, 18, kind='radio', length=1, edge='start')
for i, (name, text, value) in enumerate([('FEMALE', 'Female', 'F'), ('MALE', 'Male', 'M'), ('OTHER', 'Other', 'X')]):
    rb = RadioButton(g, name)
    rb.setLabel(text); rb.setRadioButtonValue(value)
    rb.setXPosition(90 + i * 72); rb.setYPosition(56); rb.setWidth(70); rb.setHeight(16)
label(f, 'GENDER_LBL', 'Gender', 52, 57, 36)
# a T-list: several values visible at once
bg = item(p, 'BLOOD_GROUP', 'Blood Group', 90, 82, 60, 62, kind='list', length=3, edge='start',
          listStyle=T.LSST_TLIST_CTID)
for i, v in enumerate(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']):
    bg.insertElement(i + 1, v, v)
# a poplist, filled from the database when the form starts
pl = item(p, 'PLAN_ID', 'Insurance', 90, 152, 210, dt='number', kind='list', edge='start',
          listStyle=T.LSST_POPLIST_CTID)
pl.insertElement(1, 'Star Health - Family Floater', '1')
# a combo box: a list of the usual values, and the user can type another one
ct = item(p, 'CITY', 'City', 90, 178, 130, kind='list', length=30, edge='start', listStyle=T.LSST_COMBO_CTID)
for i, c in enumerate(['Bengaluru', 'Chennai', 'Delhi', 'Gurugram', 'Hyderabad', 'Mumbai', 'Noida', 'Pune']):
    ct.insertElement(i + 1, c, c)
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch10/populate-plans.pls')
save(f)
