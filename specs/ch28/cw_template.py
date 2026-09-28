# CW_TEMPLATE: the form every CareWell form starts from (File > New > Form Using Template)
from formkit import *
f = form('CW_TEMPLATE', 'CareWell Clinic')
main(f, 'CareWell Clinic', 520, 280)
f.setMenuModule('cw_menu')
AttachedLibrary(f, 'cw_lib')
olb = ObjectLibrary.open('/work/forms/cw_objects.olb')
lib = dict([(o.getName(), o) for o in olb.getObjectLibraryObjects()])
for name in ['CW_NOTE', 'CW_CAUTION', 'CW_STOP']:
    Alert(f, name).setSubclassParent(lib[name])
VisualAttribute(f, 'CW_CURRENT_RECORD').setSubclassParent(lib['CW_CURRENT_RECORD'])
g = ObjectGroup(f, 'CW_STANDARD')
for child in ['CW_NOTE', 'CW_CAUTION', 'CW_STOP', 'CW_CURRENT_RECORD']:
    ObjectGroupChild(g, child)
pm = ModuleParameter(f, 'P_USER'); pm.setParameterInitializeValue('RECEPTION1')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "cw_sec.login(:parameter.p_user);\ncw_sec.apply_menu;")
save(f, '/work/forms/cw_template.fmb')
