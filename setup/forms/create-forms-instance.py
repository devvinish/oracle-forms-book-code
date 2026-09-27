# Creates the Forms instance "forms1" of a domain made from the "Oracle Forms Development" template,
# which the Configuration Wizard leaves out (the Forms servlet then fails with FRM-93500 or FRM-93131).
# Run it with WLST, which every Forms installation has, while the domain's server is stopped:
#   Linux:   $ORACLE_HOME/oracle_common/common/bin/wlst.sh   create-forms-instance.py <domain_home>
#   Windows: %ORACLE_HOME%\oracle_common\common\bin\wlst.cmd create-forms-instance.py <domain_home>
# It copies every file of Oracle's provisioning document (forms/provision/forms-instance-config.xml)
# from the Oracle home to the instance directory, filling in its macros, and adds the templates that
# the Forms servlet reads from <instance>/server.
import os, sys, shutil
from xml.dom import minidom

DOMAIN = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.environ.get('DOMAIN_HOME', '/u01/oracle/domains/forms_dev'))
OH = os.environ.get('ORACLE_HOME') or os.path.abspath(os.path.join(os.path.dirname(sys.executable or '.'), '..'))
if not os.path.exists(os.path.join(OH, 'forms', 'provision', 'forms-instance-config.xml')):
    OH = '/u01/oracle/fmw'
JAVA_HOME = os.environ.get('JAVA_HOME', '')
NAME = 'forms1'
INST = os.path.join(DOMAIN, 'config', 'fmwconfig', 'components', 'FORMS', 'instances', NAME)
macros = {'%ORACLE_HOME%': OH, '%FORMS_INSTANCE%': INST, '%DOMAIN_HOME%': DOMAIN, '%FORMS_INSTANCE_NAME%': NAME,
          '%CT_JAVA_HOME%': JAVA_HOME, '%JAVA_HOME%': JAVA_HOME,
          '%TNS_ADMIN%': os.path.join(DOMAIN, 'config', 'fmwconfig')}

def mkdirs(d):
    if not os.path.isdir(d): os.makedirs(d)

def copy(src, dst, text=True):
    mkdirs(os.path.dirname(dst))
    if not text:
        shutil.copyfile(src, dst); return
    f = open(src, 'rb'); s = f.read(); f.close()
    for k in macros: s = s.replace(k, macros[k])
    f = open(dst, 'wb'); f.write(s); f.close()

doc = minidom.parse(os.path.join(OH, 'forms', 'provision', 'forms-instance-config.xml'))
copied = 0
for d in doc.getElementsByTagName('Directory'):
    mkdirs(os.path.join(INST, d.getAttribute('path')))
for c in doc.getElementsByTagName('ConfigDocument'):
    src = os.path.normpath(os.path.join(OH, 'forms', c.getAttribute('source')))
    dst = os.path.join(INST, c.getAttribute('destination'))
    if os.path.exists(src):
        binary = c.getAttribute('type') == 'resFile' or src.endswith('.res')
        copy(src, dst, not binary)
        if c.getAttribute('type') == 'script': os.chmod(dst, 0755)
        copied += 1
# the templates and configuration files that the Forms servlet reads from <instance>/server
for name in ['base.htm', 'base.jnlp', 'basejpi.htm', 'basejpi_jnlp.htm', 'basesaa.txt', 'ftrace.cfg',
             'webutil.cfg', 'webutil.jnlp', 'webutilbase.htm', 'webutiljpi.htm', 'webutilsaa.txt']:
    src = os.path.join(OH, 'forms', 'templates', 'config', name)
    if os.path.exists(src) and not os.path.exists(os.path.join(INST, 'server', name)):
        copy(src, os.path.join(INST, 'server', name)); copied += 1
print('Forms instance created: %s (%d files)' % (INST, copied))
