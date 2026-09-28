from formkit import *
f = form('CH08_INVOICES', 'CareWell Clinic')
main(f, 'Invoices', 520, 330)
inv = block(f, 'INVOICES', table='INVOICES', order='invoice_id')
item(inv, 'INVOICE_ID', 'Invoice', 70, 12, 56, dt='number', edge='start')
item(inv, 'INVOICE_DATE', 'Date', 190, 12, 70, dt='date', edge='start')
item(inv, 'STATUS', 'Status', 320, 12, 60, length=8, edge='start')
item(inv, 'PATIENT_ID', 'Patient', 70, 32, 56, dt='number', edge='start')
item(inv, 'VISIT_ID', 'Visit', 190, 32, 56, dt='number', edge='start')

ln = block(f, 'INVOICE_LINES', table='INVOICE_LINES', records=5, order='line_no', scroll=True)
item(ln, 'INVOICE_ID', dt='number', cnv=None)
item(ln, 'LINE_NO', 'Line', 16, 76, 30, dt='number', insertAllowed=False, updateAllowed=False,
     keyboardNavigable=False)
item(ln, 'DESCRIPTION', 'Description', 48, 76, 200, length=60)
item(ln, 'QUANTITY', 'Qty', 250, 76, 36, dt='number')
item(ln, 'UNIT_PRICE', 'Unit Price', 288, 76, 70, dt='number')
ln.setScrollbarXPosition(360); ln.setScrollbarYPosition(76); ln.setScrollbarLength(80); ln.setScrollbarWidth(10)

pay = block(f, 'PAYMENTS', table='PAYMENTS', records=3, order='paid_on', scroll=True)
item(pay, 'INVOICE_ID', dt='number', cnv=None)
item(pay, 'PAYMENT_ID', 'Payment', 16, 196, 50, dt='number')
item(pay, 'PAID_ON', 'Paid On', 68, 196, 70, dt='date')
item(pay, 'AMOUNT', 'Amount', 140, 196, 70, dt='number')
item(pay, 'METHOD', 'Method', 212, 196, 70, length=10)
pay.setScrollbarXPosition(284); pay.setScrollbarYPosition(196); pay.setScrollbarLength(48); pay.setScrollbarWidth(10)

relations(f, inv, [
    dict(name='INVOICES_LINES', block='INVOICE_LINES', table='INVOICE_LINES',
         join=[('INVOICE_ID', 'INVOICE_ID')], delete='cascading'),
    dict(name='INVOICES_PAYMENTS', block='PAYMENTS', table='PAYMENTS',
         join=[('INVOICE_ID', 'INVOICE_ID')], delete='non-isolated')])
trigger(ln, 'PRE-INSERT', file='ch08/invoice-lines-pre-insert.pls')
save(f)
