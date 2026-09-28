from formkit import *
f = form('CH16_VISITS', 'CareWell Clinic')
main(f, 'Visits', 540, 260)
p = ModuleParameter(f, 'P_PATIENT_ID')
p.setParameterDataType(T.PADA_NUMBER_CTID)
p.setParameterInitializeValue('10012')

ed = Editor(f, 'ED_NOTES')
ed.setTitle('Visit Notes'); ed.setBottomTitle('OK saves the text in the item')
ed.setWidth(320); ed.setHeight(150); ed.setXPosition(120); ed.setYPosition(30)
ed.setWrapStyle(T.WRST_WORD_CTID); ed.setShowVerticalScrollbar(True)

alert(f, 'AL_CANNOT_DELETE', 'Delete Visit', 'This visit can''t be deleted.', style='stop', buttons=('OK',))
alert(f, 'AL_CONFIRM_DELETE', 'Delete Visit', 'Delete this visit?', style='caution', buttons=('Delete', 'Cancel'))
alert(f, 'AL_CLEAR_NOTES', 'Clear Notes', 'Clear the notes of this visit?', style='caution', buttons=('Yes', 'No'))
alert(f, 'AL_NO_NOTES', 'Clear Notes', 'This visit has no notes.', style='note', buttons=('OK',))

c = block(f, 'CTL')
item(c, 'PATIENT', 'Patient', 60, 10, 300, kind='display', length=80, edge='start')
b = item(c, 'CLEAR_NOTES', 'Clear Notes', 430, 8, 90, 20, kind='button', mouseNavigate=False,
         keyboardNavigable=False)
trigger(b, 'WHEN-BUTTON-PRESSED', file='ch16/clear-notes.pls')

v = block(f, 'VISITS', table='VISITS', records=6, where='patient_id = :parameter.p_patient_id',
          order='visit_date desc', scroll=True)
item(v, 'VISIT_ID', 'Visit', 12, 50, 44, dt='number', updateAllowed=False)
item(v, 'VISIT_DATE', 'Date', 58, 50, 70, dt='date', formatMask='DD-MON-YYYY')
item(v, 'DOCTOR_ID', 'Doctor', 130, 50, 40, dt='number')
item(v, 'DIAGNOSIS', 'Diagnosis', 172, 50, 170, length=200)
item(v, 'NOTES', 'Notes', 344, 50, 170, length=2000, editObject=ed,
     hint='Press Ctrl+E to read or edit the notes')
v.setScrollbarXPosition(516); v.setScrollbarYPosition(50); v.setScrollbarLength(96); v.setScrollbarWidth(10)
v.setInsertAllowed(False)
trigger(v, 'KEY-DELREC', file='ch16/visits-key-delrec.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch16/visits-new-form.pls')
save(f)
