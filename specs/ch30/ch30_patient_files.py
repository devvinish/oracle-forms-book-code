from formkit import *
f = form('CH30_PATIENT_FILES', 'CareWell Clinic')
main(f, 'Patient Files (WebUtil)', 470, 230)
AttachedLibrary(f, 'webutil')
t = block(f, 'TOOLS')
def tool(name, text, x, width, file):
    b = item(t, name, text, x, 8, width, 22, kind='button', mouseNavigate=False, keyboardNavigable=False)
    trigger(b, 'WHEN-BUTTON-PRESSED', file=file)
tool('LOAD_PHOTO', 'Load Photo...', 12, 90, 'ch30/load-photo.pls')
tool('EXPORT', 'Export List...', 106, 90, 'ch30/export-list.pls')
tool('UPLOAD', 'Send File...', 200, 90, 'ch30/upload.pls')
tool('INFO', 'Client', 294, 60, 'ch30/client-info.pls')
p = block(f, 'PATIENTS', table='PATIENTS', where="city = 'Pune'", order='last_name, first_name')
item(p, 'MRN', 'MRN', 70, 48, 70, length=10, edge='start', updateAllowed=False)
item(p, 'FIRST_NAME', 'Name', 70, 68, 90, length=30, edge='start')
item(p, 'LAST_NAME', None, 164, 68, 100, length=30)
item(p, 'PHONE', 'Phone', 70, 88, 110, length=20, edge='start')
item(p, 'PHOTO', None, 330, 48, 110, 134, kind='image', imageFormat=T.IMFM_NATIVE_CTID,
     sizingStyle=T.SIST_ADJUST_CTID)
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('PATIENTS');\nexecute_query;")
# WebUtil's objects: the group without OLE (no jacob.jar), and its block last in the form
olb = ObjectLibrary.open('/u01/oracle/fmw/forms/webutil.olb')
lib = dict([(o.getName(), o) for o in olb.getObjectLibraryObjects()])
ObjectGroup(f, 'WEBUTIL_NO_OLE').setSubclassParent(lib['WEBUTIL_NO_OLE'])
for name in ['TOOLS', 'PATIENTS']:
    Block.find(f, name).move(Block.find(f, 'WEBUTIL'))        # move() puts a block before another
save(f)
