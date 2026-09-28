# CH32_REST_PACKAGES: CH32_CLAIMS with the packages that the REST Package Designer generated
# (saved from Forms Builder as ch32_rest_packages.fmb), and a button that uses them
from formkit import *
start()
f = FormModule.open('/work/forms/ch32_rest_packages.fmb')
f.setName('CH32_REST_PACKAGES')
c = Block.find(f, 'CTL')
if 'COVERAGE2' in [i.getName() for i in c.getItems()]:
    Item.find(c, 'COVERAGE2').setLabel('By Package')
else:
    b = item(c, 'COVERAGE2', 'By Package', 430, 124, 104, 20, kind='button',
             mouseNavigate=False, keyboardNavigable=False)
    trigger(b, 'WHEN-BUTTON-PRESSED', file='ch32/coverage-generated.pls')
tk = Item.find(c, 'TOKEN'); tk.setXPosition(330); tk.setYPosition(126)
save(f, '/work/forms/ch32_rest_packages.fmb')
