from formkit import *
f = form('CH31_FBEAN', 'CareWell Clinic')
main(f, 'Nightly Import (FBEAN)', 400, 120)
c = block(f, 'CTL')
item(c, 'PROGRESS', None, 12, 12, 370, 22, kind='bean')      # no Implementation Class
st = item(c, 'STEP', 'Next Step', 12, 44, 80, 20, kind='button')
item(c, 'DONE', 'Done', 150, 46, 30, dt='number', kind='display', edge='start')
item(c, 'INFO', None, 12, 80, 370, kind='display', length=100)
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch31/fbean-new-form.pls')
trigger(st, 'WHEN-BUTTON-PRESSED', file='ch31/fbean-step.pls')
save(f)
