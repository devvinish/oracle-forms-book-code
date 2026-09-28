from formkit import *
f = form('CH09_INVOICE', 'CareWell Clinic')
main(f, 'Invoice', 520, 300)
MONEY = '99G990D00'
inv = block(f, 'INVOICES', table='INVOICES', order='invoice_id')
item(inv, 'INVOICE_ID', 'Invoice', 70, 12, 56, dt='number', edge='start')
item(inv, 'INVOICE_DATE', 'Date', 190, 12, 70, dt='date', edge='start', formatMask='DD-MON-YYYY',
     initializeValue='$$DATE$$')
item(inv, 'STATUS', 'Status', 320, 12, 60, length=8, edge='start', caseRestriction=T.CARS_UPPER_CTID,
     initializeValue='OPEN')
item(inv, 'PATIENT_ID', 'Patient', 70, 32, 56, dt='number', edge='start')

ln = block(f, 'INVOICE_LINES', table='INVOICE_LINES', records=5, order='line_no', scroll=True)
ln.setQueryAllRecords(True)
item(ln, 'INVOICE_ID', dt='number', cnv=None)
item(ln, 'LINE_NO', 'Line', 16, 76, 30, dt='number', insertAllowed=False, updateAllowed=False,
     keyboardNavigable=False, justification=T.JUSTIFICATION_RIGHT_CTID)
item(ln, 'DESCRIPTION', 'Description', 48, 76, 190, length=60,
     hint='What was billed: a consultation, a test, a medicine', autoHint=True,
     tooltip='Service or item billed')
item(ln, 'QUANTITY', 'Qty', 240, 76, 36, dt='number', formatMask='990', initializeValue='1',
     lowestAllowedValue='1', justification=T.JUSTIFICATION_RIGHT_CTID)
item(ln, 'UNIT_PRICE', 'Unit Price', 278, 76, 64, dt='number', formatMask=MONEY,
     lowestAllowedValue='0', justification=T.JUSTIFICATION_RIGHT_CTID)
item(ln, 'AMOUNT', 'Amount', 344, 76, 70, dt='number', kind='display', db=False, formatMask=MONEY,
     justification=T.JUSTIFICATION_RIGHT_CTID, calculateMode=T.CAMO_FORMULA_CTID,
     formula=':invoice_lines.quantity * :invoice_lines.unit_price')
ln.setScrollbarXPosition(416); ln.setScrollbarYPosition(76); ln.setScrollbarLength(80); ln.setScrollbarWidth(10)

pay = block(f, 'PAYMENTS', table='PAYMENTS', records=3, order='paid_on', scroll=True)
pay.setQueryAllRecords(True)
item(pay, 'INVOICE_ID', dt='number', cnv=None)
item(pay, 'PAYMENT_ID', 'Payment', 16, 210, 50, dt='number')
item(pay, 'PAID_ON', 'Paid On', 68, 210, 70, dt='date', formatMask='DD-MON-YYYY', initializeValue='$$DATE$$')
item(pay, 'METHOD', 'Method', 140, 210, 70, length=10, caseRestriction=T.CARS_UPPER_CTID)
item(pay, 'AMOUNT', 'Amount', 212, 210, 70, dt='number', formatMask=MONEY, justification=T.JUSTIFICATION_RIGHT_CTID)
pay.setScrollbarXPosition(284); pay.setScrollbarYPosition(210); pay.setScrollbarLength(48); pay.setScrollbarWidth(10)

tot = block(f, 'TOTALS')
tot.setSingleRecord(True)
item(tot, 'LINES_TOTAL', 'Total', 344, 162, 70, dt='number', kind='display', formatMask=MONEY, edge='start',
     justification=T.JUSTIFICATION_RIGHT_CTID, calculateMode=T.CAMO_SUMMARY_CTID,
     summaryFunction=T.SUFU_SUM_CTID, summaryBlockName='INVOICE_LINES', summaryItemName='AMOUNT')
item(tot, 'PAID', 'Paid', 344, 214, 70, dt='number', kind='display', formatMask=MONEY, edge='start',
     justification=T.JUSTIFICATION_RIGHT_CTID, calculateMode=T.CAMO_SUMMARY_CTID,
     summaryFunction=T.SUFU_SUM_CTID, summaryBlockName='PAYMENTS', summaryItemName='AMOUNT')
item(tot, 'BALANCE', 'Balance', 344, 234, 70, dt='number', kind='display', formatMask=MONEY, edge='start',
     justification=T.JUSTIFICATION_RIGHT_CTID, calculateMode=T.CAMO_FORMULA_CTID,
     formula='nvl(:totals.lines_total, 0) - nvl(:totals.paid, 0)')

relations(f, inv, [
    dict(name='INVOICES_LINES', block='INVOICE_LINES', table='INVOICE_LINES',
         join=[('INVOICE_ID', 'INVOICE_ID')], delete='cascading'),
    dict(name='INVOICES_PAYMENTS', block='PAYMENTS', table='PAYMENTS',
         join=[('INVOICE_ID', 'INVOICE_ID')], delete='non-isolated')])
trigger(ln, 'PRE-INSERT', file='ch08/invoice-lines-pre-insert.pls')
save(f)
