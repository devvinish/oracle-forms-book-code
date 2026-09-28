from formkit import *
f = form('CH11_PHOTO', 'CareWell Clinic')
main(f, 'Patient Photo', 420, 250)
# the buttons: a toolbar of iconic buttons that don't take the cursor out of the patient's record
t = block(f, 'TOOLS')
def tool(name, icon, text, x, code, width=60):
    b = item(t, name, text, x, 8, width, 22, kind='button', iconic=True, iconFilename=icon,
             labelWithIcon=T.LAIC_END_CTID, tooltip=text, mouseNavigate=False, keyboardNavigable=False)
    trigger(b, 'WHEN-BUTTON-PRESSED', code)
    return b
tool('FIND', 'find', 'Find', 12, "go_block('PATIENTS');\nexecute_query;")
tool('LOAD_PHOTO', 'photo', 'Load Photo', 76, 'x', width=86)
tool('SAVE', 'save', 'Save', 166, 'commit_form;')
Trigger.find(Item.find(t, 'LOAD_PHOTO'), 'WHEN-BUTTON-PRESSED').setTriggerText(code_of('ch11/load-photo.pls'))

p = block(f, 'PATIENTS', table='PATIENTS', order='last_name, first_name')
item(p, 'MRN', 'MRN', 70, 48, 70, length=10, edge='start', updateAllowed=False)
item(p, 'FIRST_NAME', 'Name', 70, 68, 90, length=30, edge='start')
item(p, 'LAST_NAME', None, 164, 68, 100, length=30)
item(p, 'CITY', 'City', 70, 88, 110, length=30, edge='start')
item(p, 'PHOTO', None, 280, 48, 110, 134, kind='image', imageFormat=T.IMFM_NATIVE_CTID,
     sizingStyle=T.SIST_ADJUST_CTID)
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('PATIENTS');\nexecute_query;")
save(f)
