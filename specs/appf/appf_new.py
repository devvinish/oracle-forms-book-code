# APPF_NEW: a tour of the item styles and block properties new in Forms 14.1.2 (Appendix F)
from formkit import *
f = form('APPF_NEW', 'CareWell Clinic')
f.setAppname('CAREWELL')
main(f, "What's New in 14.1.2", 600, 390)
c = block(f, 'CTL')
# typing: placeholder text, and a character counter
frame(f, 'FR_TYPE', 'Typing', 8, 6, 290, 128)
item(c, 'LAST_NAME', 'Last Name', 80, 24, 190, 20, length=30, edge='start',
     placeholderText='as on the patient card', persistentPlaceholder=True)
item(c, 'PHONE', 'Phone', 80, 52, 120, 20, length=20, edge='start', placeholderText='98xxx xxxxx')
item(c, 'NOTE', 'Note', 80, 78, 190, 34, length=120, edge='start', multiLine=True, wrapStyle=T.WRST_WORD_CTID, characterCounter=True)
# choosing: check boxes as switches and toggle buttons, a combo box that completes
frame(f, 'FR_CHOOSE', 'Choosing', 306, 6, 286, 128)
for name, text, x, y, w, h, style in [('ACTIVE', 'Active', 320, 24, 90, 18, T.UIST_SWITCH_CTID),
                                      ('NOTIFY', 'Send reminders', 420, 22, 160, 22, T.UIST_SWITCH_LARGE_CTID),
                                      ('URGENT', 'Urgent', 320, 52, 80, 22, T.UIST_TOGGLE_CTID)]:
    cb = item(c, name, text, x, y, w, h, kind='check', length=1, uiStyle=style)
    cb.setCheckedValue('Y'); cb.setUncheckedValue('N'); cb.setInitializeValue('Y' if name != 'URGENT' else 'N')
sp = item(c, 'SPECIALTY', 'Specialty', 380, 90, 190, kind='list', length=40, edge='start',
          listStyle=T.LSST_COMBO_CTID, autoComplete=True)
sp.insertElement(1, 'General Physician', 'General Physician')
# showing: numbers as a progress bar, a gauge, and a half gauge
frame(f, 'FR_SHOW', 'Appointments by status, in percent', 8, 140, 584, 96)
for name, text, x, y, w, h, style in [('COMPLETED', 'Completed', 30, 176, 200, 22, T.DUST_PROGRESS_CTID),
                                      ('BOOKED', 'Booked', 300, 160, 66, 66, T.DUST_GAUGE_CTID),
                                      ('NO_SHOW', 'No-shows', 440, 166, 100, 56, T.DUST_HALFGAUGE_CTID)]:
    item(c, name, text, x, y, w, h, dt='number', kind='display', db=False,
         displayUiStyle=style, uiMinval=0, uiMaxval=100, animated=True)
# an autosized block, sorted on the Forms server
d = block(f, 'DOCTORS', table='DOCTORS', order='doctor_id',
          where="specialty = nvl(:ctl.specialty, specialty)")
d.setAutoSizeBlock(True); d.setMaximumRecordsDisplay(8)
item(d, 'LAST_NAME', 'Doctor', 14, 256, 100, length=30)
item(d, 'FIRST_NAME', None, 116, 256, 90, length=30)
item(d, 'SPECIALTY', 'Specialty', 208, 256, 130, length=40)
item(d, 'CONSULT_FEE', 'Fee', 340, 256, 50, dt='number')
b = block(f, 'BTN')
for name, text, y, code in [('QUERY', 'Query', 256, "go_block('DOCTORS');\nexecute_query;"),
                            ('SORT_NAME', 'Sort by Name', 284, None), ('SORT_FEE', 'Sort by Fee', 312, None)]:
    bt = item(b, name, text, 460, y, 110, 22, kind='button', roundSide=T.ROUND_SIDE_BOTH_CTID,
              rolloverSwap=True, mouseNavigate=False, keyboardNavigable=False)
    trigger(bt, 'WHEN-BUTTON-PRESSED', code, file=None if code else 'appf/%s.pls' % name.lower().replace('_', '-'))
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='appf/new-form.pls')
save(f)
