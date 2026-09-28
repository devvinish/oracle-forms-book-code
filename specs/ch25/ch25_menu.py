from formkit import *
import os
m = MenuModule('CW_MENU')
cw = Menu(m, 'CW_MAIN')
m.setMainMenu('CW_MAIN')

def entry(menu, name, label=None, code=None, sub=None, icon=None, kind='plain', magic=None):
    mi = MenuItem(menu, name)
    if kind == 'separator':
        mi.setMenuItemType(T.MNIT_SEPARATOR_CTID); return mi
    mi.setLabel(label)
    mi.setName(name)                           # setting the label renames the item after it
    if magic is not None:                      # a magic item that Forms fills: its command type is Null
        mi.setMenuItemType(T.MNIT_MAGIC_CTID); mi.setMagicItem(magic); mi.setCommandType(T.COTY_NULL_CTID)
    if sub:
        mi.setCommandType(T.COTY_MENU_CTID); mi.setSubMenuName(sub)
    elif code:
        mi.setCommandType(T.COTY_PLSQL_CTID); mi.setMenuItemCode(code)
    if icon:                                   # also a button of the menu's toolbar
        mi.setIconFilename(icon); mi.setVisibleInHorizontalMenuToolbar(True)
    return mi

def open_or_go(form):
    return ("if id_null(find_form('%s')) then\n  open_form('%s');\nelse\n  go_form('%s');\nend if;"
            % (form.upper(), form, form.upper()))

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
entry(c, 'PATIENTS', '&Patients', open_or_go('ch25_patients'))
entry(c, 'INVOICES', '&Invoices', open_or_go('ch21_invoices'))
entry(c, 'FEES', 'Doctors\' &Fees', code_of('ch25/menu-open-fees.pls'))
h = Menu(m, 'HELP')
entry(h, 'ABOUT', '&About CareWell', code_of('ch25/menu-about.pls'))
entry(cw, 'FILE', '&File', sub='FILE')
entry(cw, 'RECORDS', '&Records', sub='RECORDS')
entry(cw, 'CLINIC', '&Clinic', sub='CLINIC')
entry(cw, 'WINDOW', '&Window', magic=T.MAIT_WINDOW_CTID)
entry(cw, 'HELP', '&Help', sub='HELP')
if os.environ.get('CW_MENU_SECURITY'):         # the variant with database-role security
    m.setUseSecurity(True)
    m.addRole(0, 'CW_USER_ROLE'); m.addRole(1, 'CW_FEES_ROLE')
    for menu in m.getMenus():                  # with security, an item without roles is for no one
        for mi in menu.getMenuItems():
            if mi.getName() == 'FEES':
                mi.addRole(0, 'CW_FEES_ROLE'); mi.setDisplayNoPriv(True)   # shown, but disabled
            else:
                mi.addRole(0, 'CW_USER_ROLE')
save(m)
