# adds the RP2RRO settings to the form that the Forms Migration Assistant converted (Chapter 37)
from formkit import *
from oracle.forms.jdapi import FormModule
start()
f = FormModule.open('/work/forms/ch37_legacy.fmb')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch37/after-new-form.pls')
f.save('/work/forms/ch37_legacy.fmb')
print('saved /work/forms/ch37_legacy.fmb')
