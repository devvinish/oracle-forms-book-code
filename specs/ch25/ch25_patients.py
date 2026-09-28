from formkit import *
f = form('CH25_PATIENTS', 'CareWell Clinic')
main(f, 'Patients of Pune', 470, 220)
f.setMenuModule('cw_menu')                   # the file name, as on disk
AttachedLibrary(f, 'cw_lib')
pm = ModuleParameter(f, 'P_USER')
pm.setParameterInitializeValue('RECEPTION1')
for name, style, buttons in [('CW_NOTE', 'note', ('OK',)), ('CW_CAUTION', 'caution', ('Yes', 'No')), ('CW_STOP', 'stop', ('OK',))]:
    alert(f, name, 'CareWell Clinic', 'Message', style, buttons)

pop = Menu(f, 'POP_PATIENT')                 # a popup menu belongs to the form
mi = MenuItem(pop, 'APPOINTMENTS'); mi.setLabel('Appointments...'); mi.setName('APPOINTMENTS')
mi.setCommandType(T.COTY_PLSQL_CTID); mi.setMenuItemCode(code_of('ch25/popup-appointments.pls'))
mi = MenuItem(pop, 'VISITS'); mi.setLabel('Visits'); mi.setName('VISITS')
mi.setCommandType(T.COTY_PLSQL_CTID)
mi.setMenuItemCode("declare\n  v_list paramlist := create_parameter_list('');\nbegin\n  add_parameter(v_list, 'P_PATIENT_ID', text_parameter, :patients.patient_id);\n  open_form('ch16_visits', activate, no_session, v_list);\nend;")

p = block(f, 'PATIENTS', table='PATIENTS', records=8, where="city = 'Pune'", order='last_name, first_name', scroll=True)
for args in [('PATIENT_ID', 'Id', 12, 30, 44, 'number'), ('MRN', 'MRN', 58, 30, 70, 'char'),
             ('FIRST_NAME', 'First Name', 130, 30, 90, 'char'), ('LAST_NAME', 'Last Name', 222, 30, 90, 'char'),
             ('PHONE', 'Phone', 314, 30, 96, 'char')]:
    it = item(p, args[0], args[1], args[2], args[3], args[4], dt=args[5], length=None if args[5] == 'number' else 30)
    it.setPopupMenuName('POP_PATIENT')
trigger(p, 'PRE-POPUP-MENU', file='ch25/pre-popup-menu.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', file='ch25/patients-new-form.pls')
save(f)
