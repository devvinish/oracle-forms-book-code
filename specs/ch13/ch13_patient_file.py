from formkit import *
f = form('CH13_PATIENT_FILE', 'CareWell Clinic')
w, c = main(f, 'Patient File', 560, 300)
# a horizontal toolbar canvas, shown at the top of the window
tb = canvas(f, 'TOOLBAR', 'MAIN_WIN', 560, 30, kind='htoolbar')
w.setHorizontalToolbarCanvasName('TOOLBAR')
t = block(f, 'TOOLS')
def tool(name, icon, text, x, code, cnv='TOOLBAR', width=64):
    b = item(t, name, text, x, 5, width, 20, kind='button', cnv=cnv, iconic=bool(icon),
             iconFilename=icon or '', labelWithIcon=T.LAIC_END_CTID, mouseNavigate=False,
             keyboardNavigable=False, tooltip=text)
    trigger(b, 'WHEN-BUTTON-PRESSED', code)
    return b
tool('FIND', 'find', 'Find', 8, "go_block('PATIENTS');\nexecute_query;")
tool('SAVE', 'save', 'Save', 76, 'commit_form;')
tool('ALLERGIES', None, 'Allergies...', 144, "go_item('PATIENTS.ALLERGIES');", width=80)
tool('HELP', None, 'Help', 228, 'null;', width=50)
Trigger.find(Item.find(t, 'HELP'), 'WHEN-BUTTON-PRESSED').setTriggerText(code_of('ch13/toggle-help.pls'))

# the tab canvas, on the content canvas, with three pages
tabs = canvas(f, 'TABS', 'MAIN_WIN', 540, 240, kind='tab', x=10, y=40, vw=540, vh=240)
for name, text in [('DETAILS', 'Details'), ('APPTS', 'Appointments'), ('VISITS', 'Visits')]:
    TabPage(tabs, name).setLabel(text)

p = block(f, 'PATIENTS', table='PATIENTS', order='last_name, first_name')
item(p, 'PATIENT_ID', dt='number', cnv=None)
item(p, 'MRN', 'MRN', 60, 12, 70, length=10, edge='start', updateAllowed=False)
item(p, 'FIRST_NAME', 'Name', 190, 12, 90, length=30, edge='start')
item(p, 'LAST_NAME', None, 284, 12, 110, length=30)
def tabitem(name, prompt, x, y, w, **k):
    return item(p, name, prompt, x, y, w, cnv='TABS', tabPageName='DETAILS', edge='start', **k)
tabitem('BIRTH_DATE', 'Birth Date', 90, 20, 76, dt='date')
tabitem('GENDER', 'Gender', 90, 42, 24, length=1)
tabitem('BLOOD_GROUP', 'Blood Group', 90, 64, 36, length=3)
tabitem('PHONE', 'Phone', 90, 86, 120, length=20)
tabitem('CITY', 'City', 90, 108, 120, length=30)
tabitem('ADDRESS', 'Address', 90, 130, 240, length=80)
# the allergies are in the patient's block, but shown in a dialog window of their own
aw = window(f, 'ALLERGY_WIN', 'Allergies', 300, 130, 120, 120, dialog=True, modal=True)
canvas(f, 'ALLERGY_CNV', 'ALLERGY_WIN', 300, 130)
aw.setPrimaryCanvas('ALLERGY_CNV')
item(p, 'ALLERGIES', None, 12, 12, 276, 76, length=200, cnv='ALLERGY_CNV', multiLine=True,
     wrapStyle=T.WRST_WORD_CTID)
tool('CLOSE_ALLERGIES', None, 'Close', 224, "go_item('PATIENTS.MRN');\nhide_window('ALLERGY_WIN');",
     cnv='ALLERGY_CNV', width=64)
Item.find(t, 'CLOSE_ALLERGIES').setYPosition(98)

ap = block(f, 'APPOINTMENTS', table='APPOINTMENTS', records=8, order='appt_start desc', scroll=True)
item(ap, 'PATIENT_ID', dt='number', cnv=None)
def apitem(name, prompt, x, w, **k):
    return item(ap, name, prompt, x, 20, w, cnv='TABS', tabPageName='APPTS', **k)
apitem('APPT_START', 'Start', 12, 110, dt='datetime', formatMask='DD-MON-YYYY HH24:MI')
apitem('DOCTOR_ID', 'Doctor', 124, 44, dt='number')
apitem('STATUS', 'Status', 170, 80, length=10)
apitem('REASON', 'Reason', 252, 250, length=100)
ap.setScrollbarCanvasName('TABS'); ap.setScrollbarTabPageName('APPTS')
ap.setScrollbarXPosition(504); ap.setScrollbarYPosition(20); ap.setScrollbarLength(128); ap.setScrollbarWidth(10)

v = block(f, 'VISITS', table='VISITS', records=8, order='visit_date desc', scroll=True)
item(v, 'PATIENT_ID', dt='number', cnv=None)
def vitem(name, prompt, x, w, **k):
    return item(v, name, prompt, x, 20, w, cnv='TABS', tabPageName='VISITS', **k)
vitem('VISIT_DATE', 'Date', 12, 76, dt='date')
vitem('DOCTOR_ID', 'Doctor', 90, 44, dt='number')
vitem('DIAGNOSIS', 'Diagnosis', 136, 366, length=200)
v.setScrollbarCanvasName('TABS'); v.setScrollbarTabPageName('VISITS')
v.setScrollbarXPosition(504); v.setScrollbarYPosition(20); v.setScrollbarLength(128); v.setScrollbarWidth(10)

relations(f, p, [
    dict(name='PATIENTS_APPTS', block='APPOINTMENTS', table='APPOINTMENTS',
         join=[('PATIENT_ID', 'PATIENT_ID')], deferred=True),
    dict(name='PATIENTS_VISITS', block='VISITS', table='VISITS',
         join=[('PATIENT_ID', 'PATIENT_ID')], deferred=True)])

# a stacked canvas: a help panel over the right of the window, hidden until the Help button shows it
stk = canvas(f, 'HELP_STK', 'MAIN_WIN', 170, 120, kind='stacked', x=380, y=6, vw=170, vh=120)
stk.setVisible(False)
frame(f, 'HELP_FRAME', 'Help', 4, 6, 162, 110, cnv='HELP_STK')
for i, line in enumerate(['Find: query the patients', 'Save: save the changes',
                          'Allergies: open the', '  allergies in a dialog', 'Tabs: details, appointments,',
                          '  and visits of the patient']):
    label(f, 'HELP_L%d' % i, line, 10, 20 + i * 14, 150, 14, cnv='HELP_STK')

trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('PATIENTS');\nexecute_query;")
trigger(f, 'WHEN-TAB-PAGE-CHANGED', file='ch13/tab-page-changed.pls')
trigger(f, 'WHEN-WINDOW-CLOSED', file='ch13/window-closed.pls')
save(f)
