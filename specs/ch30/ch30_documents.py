# CH30_DOCUMENTS: a patient's documents stored in the database, moved with WebUtil (Chapter 30)
from formkit import *
f = form('CH30_DOCUMENTS', 'CareWell Clinic')
main(f, 'Patient Documents (WebUtil)', 560, 300)
AttachedLibrary(f, 'webutil')
p = block(f, 'PATIENTS', table='PATIENTS', where="city = 'Pune'", order='last_name, first_name')
p.setInsertAllowed(False); p.setUpdateAllowed(False); p.setDeleteAllowed(False)
item(p, 'PATIENT_ID', None, dt='number', cnv=None)
item(p, 'MRN', 'Patient', 60, 12, 70, length=10, edge='start')
item(p, 'FIRST_NAME', None, 134, 12, 90, length=30)
item(p, 'LAST_NAME', None, 228, 12, 100, length=30)
d = block(f, 'DOCS', table='PATIENT_DOCUMENTS', records=6, order='uploaded_on, doc_id')
d.setUpdateAllowed(False)
item(d, 'DOC_ID', None, dt='number', cnv=None)
item(d, 'PATIENT_ID', None, dt='number', cnv=None)
item(d, 'FILE_NAME', 'Document', 12, 56, 200, length=200, insertAllowed=False)
item(d, 'DOC_TYPE', 'Type', 214, 56, 70, length=10, insertAllowed=False)
item(d, 'FILE_SIZE', 'Bytes', 286, 56, 60, dt='number', insertAllowed=False)
item(d, 'UPLOADED_ON', 'Uploaded', 348, 56, 76, dt='date', formatMask='DD-MON-YYYY', insertAllowed=False)
item(d, 'UPLOADED_BY', 'By', 426, 56, 90, length=30, insertAllowed=False)
relations(f, p, [dict(name='PATIENTS_DOCS', block='DOCS', table='PATIENT_DOCUMENTS',
                      join=[('PATIENT_ID', 'PATIENT_ID')])])
c = block(f, 'CTL')
t = item(c, 'DOC_TYPE', 'New document is a', 110, 176, 100, kind='list', length=10, edge='start',
         listStyle=T.LSST_POPLIST_CTID, initializeValue='REPORT')
for i, v in enumerate(['REPORT', 'SCAN', 'REFERRAL', 'CONSENT', 'OTHER']):
    t.insertElement(i + 1, v.title(), v)
for name, text, x, y, w in [('ADD_DOC', 'Add Document...', 220, 174, 110), ('SAVE_DOC', 'Save As...', 12, 210, 90),
                            ('OPEN_DOC', 'Open', 106, 210, 70), ('DETAILS', 'Details', 180, 210, 70),
                            ('EXPORT', 'Export List...', 254, 210, 100)]:
    b = item(c, name, text, x, y, w, 22, kind='button', mouseNavigate=False, keyboardNavigable=False)
    trigger(b, 'WHEN-BUTTON-PRESSED', file='ch30/docs-%s.pls' % name.lower().replace('_doc', '').replace('add', 'add').replace('save', 'save').replace('open', 'open'))
unit(f, 'EXPORT_BLOCK', file='ch39/export-block.pls')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', ":ctl.doc_type := 'REPORT';\ngo_block('PATIENTS');\nexecute_query;")
olb = ObjectLibrary.open('/u01/oracle/fmw/forms/webutil.olb')
lib = dict([(o.getName(), o) for o in olb.getObjectLibraryObjects()])
ObjectGroup(f, 'WEBUTIL_NO_OLE').setSubclassParent(lib['WEBUTIL_NO_OLE'])
for name in ['PATIENTS', 'DOCS', 'CTL']:
    Block.find(f, name).move(Block.find(f, 'WEBUTIL'))        # WebUtil's block stays the last
save(f)
