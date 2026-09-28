# CW_LOGIN: the first form of the CareWell application (Chapter 40)
from formkit import *
f = form('CW_LOGIN', 'CareWell Clinic')
main(f, 'CareWell Clinic - Sign In', 380, 150)
f.setMenuModule('')                              # no menu before the user signs in
AttachedLibrary(f, 'cw_lib')
c = block(f, 'CTL')
label(f, 'L_HEAD', 'Sign in to CareWell Clinic', 20, 14, 300, 18, size=1200)
item(c, 'USERNAME', 'User', 90, 48, 120, length=30, edge='start', caseRestriction=T.CARS_UPPER_CTID,
     lovName='LOV_USERS', lovButton=True, validateFromList=True, required=True)
item(c, 'FULL_NAME', None, 216, 48, 150, kind='display', length=60)
b = item(c, 'SIGN_IN', 'Sign In', 90, 84, 90, 24, kind='button')
trigger(b, 'WHEN-BUTTON-PRESSED', file='ch40/sign-in.pls')
lov(f, 'LOV_USERS', "select username, full_name, initcap(app_role) as role from app_users "
    "where active = 'Y' order by full_name",
    [('USERNAME', 'User', 90, 'CTL.USERNAME'), ('FULL_NAME', 'Name', 140, 'CTL.FULL_NAME'),
     ('ROLE', 'Role', 70, None)], title='CareWell users', width=320, height=200)
save(f)
