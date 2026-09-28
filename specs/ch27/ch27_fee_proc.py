# CH27_FEE_PROC: the block that the Data Block Wizard built on CW_FEE_API's procedures
# (ch27_fee_proc_wizard.fmb, made in Forms Builder), laid out and completed here
from formkit import *
start()
f = FormModule.open('/work/forms/ch27_fee_proc_wizard.fmb')
f.setName('CH27_FEE_PROC')
main(f, 'Consultation Fees (procedures)', 400, 150)
AttachedLibrary(f, 'cw_lib')
pm = ModuleParameter(f, 'P_DEPT_ID')
pm.setParameterDataType(T.PADA_NUMBER_CTID); pm.setParameterInitializeValue('101')
b = Block.find(f, 'FEES')
b.setRecordsDisplayCount(4); b.setInsertAllowed(False); b.setDeleteAllowed(False)
for i, (name, prompt, x, w) in enumerate([('DOCTOR_ID', 'ID', 12, 44), ('FIRST_NAME', 'First Name', 58, 110),
                                          ('LAST_NAME', 'Last Name', 170, 110), ('CONSULT_FEE', 'Fee', 282, 60)]):
    it = Item.find(b, name)
    it.setCanvasName('MAIN_CNV'); it.setXPosition(x); it.setYPosition(30); it.setWidth(w); it.setHeight(16)
    it.setPrompt(prompt); it.setPromptAttachmentEdge(T.PRAT_TOP_CTID)
    if name != 'CONSULT_FEE':
        it.setUpdateAllowed(False)
    else:
        it.setFormatMask('990.00')
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "go_block('FEES');\nexecute_query;")
trigger(f, 'ON-ERROR', file='ch27/fee-proc-on-error.pls')
save(f, '/work/forms/ch27_fee_proc.fmb')
