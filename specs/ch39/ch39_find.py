# CH39_FIND: a search panel (dynamic WHERE with bind references), headings that sort, a record counter,
# and a generic CSV export of a block (Chapter 39, recipes 1-3 and 11)
from formkit import *
f = form('CH39_FIND', 'CareWell Clinic')
main(f, 'Find Patients', 560, 350)
c = block(f, 'CTL')
frame(f, 'FR_FIND', 'Find patients whose', 8, 6, 544, 78)
item(c, 'NAME', 'Name contains', 90, 22, 150, length=40, edge='start')
item(c, 'CITY', 'City', 300, 22, 110, length=30, edge='start')
item(c, 'BORN_FROM', 'Born from', 90, 50, 80, dt='date', formatMask='DD-MON-YYYY', edge='start')
item(c, 'BORN_TO', 'to', 196, 50, 80, dt='date', formatMask='DD-MON-YYYY', edge='start')
for name, text, x, code in [('FIND', 'Find', 300, 'find_patients;'),
                            ('CLEAR', 'Clear', 364, ":ctl.name := null;\n:ctl.city := null;\n:ctl.born_from := null;\n:ctl.born_to := null;\nfind_patients;"),
                            ('EXPORT', 'Export', 428, None)]:
    b = item(c, name, text, x, 48, 60, 22, kind='button', mouseNavigate=False, keyboardNavigable=False)
    trigger(b, 'WHEN-BUTTON-PRESSED', code, file=None if code else 'ch39/export-pressed.pls')
item(c, 'COUNTER', None, 12, 318, 200, kind='display', length=40)
item(c, 'TOTAL', None, dt='number', cnv=None)
for n in ('SORT_COLUMN', 'SORT_DIR', 'SORT_HEADING', 'SORT_LABEL'):
    item(c, n, None, length=60, cnv=None)
# the headings are buttons: a click sorts by the column below
h = block(f, 'HEAD')
for name, text, x, w, col in [('H_MRN', 'MRN', 12, 70, 'mrn'), ('H_NAME', 'Name', 84, 192, 'last_name, first_name'),
                              ('H_CITY', 'City', 278, 90, 'city'), ('H_BORN', 'Born', 370, 80, 'birth_date')]:
    b = item(h, name, text, x, 96, w, 18, kind='button', mouseNavigate=False, keyboardNavigable=False)
    if name == 'H_NAME':
        trigger(b, 'WHEN-BUTTON-PRESSED', file='ch39/heading-name.pls')
    else:
        trigger(b, 'WHEN-BUTTON-PRESSED', "sort_by('%s', 'HEAD.%s', '%s');" % (col, name, text))
label(f, 'L_PHONE', 'Phone', 456, 99, 60)
p = block(f, 'PATIENTS', table='PATIENTS', records=10, order='last_name, first_name', scroll=True)
p.setInsertAllowed(False); p.setUpdateAllowed(False); p.setDeleteAllowed(False)
item(p, 'PATIENT_ID', None, dt='number', cnv=None)
item(p, 'MRN', None, 12, 116, 70, length=10)
item(p, 'LAST_NAME', None, 84, 116, 100, length=30)
item(p, 'FIRST_NAME', None, 186, 116, 90, length=30)
item(p, 'CITY', None, 278, 116, 90, length=30)
item(p, 'BIRTH_DATE', None, 370, 116, 80, dt='date', formatMask='DD-MON-YYYY')
item(p, 'PHONE', None, 452, 116, 90, length=20)
p.setScrollbarXPosition(544); p.setScrollbarYPosition(116); p.setScrollbarLength(196); p.setScrollbarWidth(10)
trigger(p, 'WHEN-NEW-RECORD-INSTANCE', file='ch39/counter.pls')
unit(f, 'FIND_PATIENTS', file='ch39/find-patients.pls')
unit(f, 'SORT_BY', file='ch39/sort-by.pls')
unit(f, 'EXPORT_BLOCK', file='ch39/export-block.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "find_patients;")
save(f)
