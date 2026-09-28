from formkit import *
from oracle.forms.jdapi import MenuModule, Menu, MenuItem, JdapiTypes as T
start()
m = MenuModule('STEP0_MENU')
main_menu = Menu(m, 'MAIN_MENU')
m.setMainMenu('MAIN_MENU')
def entry(menu, name, label, code=None, sub=None):
    mi = MenuItem(menu, name)
    mi.setLabel(label)
    if sub:
        mi.setCommandType(T.COTY_MENU_CTID); mi.setSubMenuName(sub)
    else:
        mi.setCommandType(T.COTY_PLSQL_CTID); mi.setMenuItemCode(code)
    return mi
file_m = Menu(m, 'FILE_MENU')
entry(file_m, 'SAVE', '&Save', 'do_key(\'commit_form\');')
entry(file_m, 'EXIT', 'E&xit', 'do_key(\'exit_form\');')
doc_m = Menu(m, 'DOCTORS_MENU')
entry(doc_m, 'FETCH', '&Fetch Doctor 7', "copy('7', 'ctrl.doctor_id');\ngo_item('ctrl.fetch');\nexecute_trigger('WHEN-BUTTON-PRESSED');")
entry(main_menu, 'FILE', '&File', sub='FILE_MENU')
entry(main_menu, 'DOCTORS', '&Doctors', sub='DOCTORS_MENU')
m.save('/work/forms/step0_menu.mmb'); print('saved menu')
f = FormModule.open('/work/forms/step0_rest.fmb')
f.setMenuModule('step0_menu')   # the file name: Linux file names are case-sensitive
f.save('/work/forms/step0_menuform.fmb'); print('saved /work/forms/step0_menuform.fmb')
