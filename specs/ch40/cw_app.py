# CW_APP: the menu of the CareWell application (Chapter 40), built like CW_MENU of Chapter 25
from formkit import *
m = MenuModule('CW_APP')
AttachedLibrary(m, 'cw_lib')
main_ = Menu(m, 'CW_MAIN'); m.setMainMenu('CW_MAIN')

def entry(menu, name, label=None, code=None, sub=None, kind='plain', magic=None, icon=None):
    mi = MenuItem(menu, name)
    if kind == 'separator':
        mi.setMenuItemType(T.MNIT_SEPARATOR_CTID); return mi
    mi.setLabel(label); mi.setName(name)
    if magic is not None:
        mi.setMenuItemType(T.MNIT_MAGIC_CTID); mi.setMagicItem(magic); mi.setCommandType(T.COTY_NULL_CTID)
    elif sub:
        mi.setCommandType(T.COTY_MENU_CTID); mi.setSubMenuName(sub)
    else:
        mi.setCommandType(T.COTY_PLSQL_CTID); mi.setMenuItemCode(code)
    if icon:
        mi.setIconFilename(icon); mi.setVisibleInHorizontalMenuToolbar(True)
    return mi

f_ = Menu(m, 'FILE')
entry(f_, 'SAVE', '&Save', "do_key('commit_form');", icon='save')
entry(f_, 'CLEAR', '&Clear', "do_key('clear_form');")
entry(f_, 'SEP1', kind='separator')
entry(f_, 'EXIT', 'E&xit', "do_key('exit_form');")
r = Menu(m, 'RECORDS')
entry(r, 'QUERY', '&Enter Query', "do_key('enter_query');")
entry(r, 'EXECUTE', 'E&xecute Query', "do_key('execute_query');", icon='find')
entry(r, 'SEP1', kind='separator')
entry(r, 'INSERT', '&Insert', "do_key('create_record');")
entry(r, 'DELETE', '&Delete', "do_key('delete_record');")
c = Menu(m, 'CLINIC')
entry(c, 'HOME', '&Home', "cw_nav.open_module('cw_main');")
entry(c, 'PATIENTS', '&Patients', "cw_nav.open_module('cw_patients');")
entry(c, 'APPOINTMENTS', '&Appointments', "cw_nav.open_module('cw_appointments');")
entry(c, 'INVOICES', '&Invoices', "cw_nav.open_module('cw_billing');")
h = Menu(m, 'HELP')
entry(h, 'ABOUT', '&About CareWell', "message('CareWell Clinic, signed in as ' || cw_sec.full_name || '.');")
entry(main_, 'FILE', '&File', sub='FILE')
entry(main_, 'RECORDS', '&Records', sub='RECORDS')
entry(main_, 'CLINIC', '&Clinic', sub='CLINIC')
entry(main_, 'WINDOW', '&Window', magic=T.MAIT_WINDOW_CTID)
entry(main_, 'HELP', '&Help', sub='HELP')
save(m)
