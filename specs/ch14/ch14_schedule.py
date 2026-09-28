from formkit import *
f = form('CH14_SCHEDULE', 'CareWell Clinic')
main(f, 'Appointments', 520, 300)

# named visual attributes
cur = VisualAttribute(f, 'VA_CURRENT');   cur.setBackColor('r88g88b100')
can = VisualAttribute(f, 'VA_CANCELLED'); can.setForegroundColor('gray52'); can.setFontStyle(T.FOST_ITALIC_CTID)
nos = VisualAttribute(f, 'VA_NO_SHOW');   nos.setForegroundColor('r75g0b0')

# a property class for items that show a value the user may not change
pc = PropertyClass(f, 'PC_READONLY')
pc.setBooleanProperty(T.INSERT_ALLOWED_PTID, False)
pc.setBooleanProperty(T.UPDATE_ALLOWED_PTID, False)
pc.setBooleanProperty(T.KEYBOARD_NAVIGABLE_PTID, False)
pc.setStringProperty(T.BACK_COLOR_PTID, 'r88g88b88')

c = block(f, 'CTL')
item(c, 'BANNER', None, 0, 0, 520, 22, kind='display', length=60, fontSize=1200)

a = block(f, 'APPOINTMENTS', table='APPOINTMENTS', records=12, where="doctor_id = 1003 and appt_start >= date '2026-09-01'",
          order='appt_start', scroll=True)
a.setRecordVisualAttributeGroupName('VA_CURRENT')

item(a, 'PATIENT_ID', dt='number', cnv=None)
st = item(a, 'APPT_START', 'Start', 12, 44, 100, dt='datetime', formatMask='DD-MON-YYYY HH24:MI')
st.setSubclassParent(pc)
pn = item(a, 'PATIENT_NAME', 'Patient', 114, 44, 120, kind='display', length=61, db=False)
item(a, 'STATUS', 'Status', 236, 44, 76, length=10)
item(a, 'REASON', 'Reason', 314, 44, 180, length=100)
a.setScrollbarXPosition(496); a.setScrollbarYPosition(44); a.setScrollbarLength(192); a.setScrollbarWidth(10)
trigger(a, 'POST-QUERY', file='ch14/appointments-post-query.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch14/banner.pls')
save(f)
