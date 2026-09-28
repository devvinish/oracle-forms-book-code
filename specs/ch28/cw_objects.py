# CW_OBJECTS: the object library of CareWell Clinic. The objects are made in a scratch form,
# then added to the library's tab, as Forms Builder does when you drag them onto it.
from formkit import *
f = form('CW_OBJECTS_SRC', 'CareWell Clinic')
for name, style, buttons in [('CW_NOTE', 'note', ('OK',)), ('CW_CAUTION', 'caution', ('Yes', 'No')),
                             ('CW_STOP', 'stop', ('OK',))]:
    alert(f, name, 'CareWell Clinic', 'Message', style, buttons)
va = VisualAttribute(f, 'CW_CURRENT_RECORD'); va.setBackColor('r88g88b100')
d = PropertyClass(f, 'CW_DATE')
d.setStringProperty(T.FORMAT_MASK_PTID, 'DD-MON-YYYY'); d.setIntegerProperty(T.WIDTH_PTID, 76)
m = PropertyClass(f, 'CW_MONEY')
m.setStringProperty(T.FORMAT_MASK_PTID, '999,990.00'); m.setIntegerProperty(T.WIDTH_PTID, 64)
r = PropertyClass(f, 'CW_READONLY')
r.setBooleanProperty(T.INSERT_ALLOWED_PTID, False); r.setBooleanProperty(T.UPDATE_ALLOWED_PTID, False)
r.setBooleanProperty(T.KEYBOARD_NAVIGABLE_PTID, False); r.setStringProperty(T.BACK_COLOR_PTID, 'r88g88b88')
olb = ObjectLibrary('CW_OBJECTS')
tab = ObjectLibraryTab(olb, 'CAREWELL'); tab.setLabel('CareWell')
# items to use as SmartClasses: offered on the SmartClasses menu of items
blk = block(f, 'CW_ITEMS', cnv=None)
di = item(blk, 'CW_DATE_ITEM', None, 0, 0, 76, dt='date', cnv=None, formatMask='DD-MON-YYYY')
mi = item(blk, 'CW_MONEY_ITEM', None, 0, 0, 64, dt='number', cnv=None, formatMask='999,990.00')
# (an object group added with the JDAPI made the library unreadable, so groups live in forms)
for obj in [Alert.find(f, 'CW_NOTE'), Alert.find(f, 'CW_CAUTION'), Alert.find(f, 'CW_STOP'), va, d, m, r, di, mi]:
    olb.addObject(tab, obj, True)
desc = {'CW_NOTE': 'Note alert, one button. Used by CW_MSG.INFORM (CW_LIB).',
        'CW_CAUTION': 'Caution alert, two buttons. Used by CW_MSG.ASK (CW_LIB).',
        'CW_STOP': 'Stop alert, one button. Used by CW_MSG.FAIL (CW_LIB).',
        'CW_CURRENT_RECORD': 'Current record highlight: set it as a block\'s Current Record Visual Attribute Group.',
        'CW_DATE': 'Date items: DD-MON-YYYY, 76 points wide.',
        'CW_MONEY': 'Amounts: 999,990.00, 64 points wide.',
        'CW_READONLY': 'Items the user may see but not change or enter.',
        'CW_DATE_ITEM': 'A date text item: DD-MON-YYYY. SmartClass.',
        'CW_MONEY_ITEM': 'An amount text item: 999,990.00. SmartClass.'}
for o in olb.getObjectLibraryObjects():
    olb.setDescription(o, desc[o.getName()])
for name in ['CW_DATE_ITEM', 'CW_MONEY_ITEM']:        # SmartClasses
    for o in olb.getObjectLibraryObjects():
        if o.getName() == name: olb.setSmartClass(o, True)
for o in olb.getObjectLibraryObjects():
    print('%s %s smart=%s' % (o.getClassName(), o.getName(), olb.isSmartClass(o)))
save(olb, '/work/forms/cw_objects.olb')
