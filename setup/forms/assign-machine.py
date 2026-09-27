# Puts the Administration Server of a Forms development domain on the machine of its Forms
# instance (AdminServerMachine). Run it with WLST while the server is stopped:
#   Linux:   $ORACLE_HOME/oracle_common/common/bin/wlst.sh   assign-machine.py <domain_home>
#   Windows: %ORACLE_HOME%\oracle_common\common\bin\wlst.cmd assign-machine.py <domain_home>
import sys
readDomain(sys.argv[1])
cd('/Servers/AdminServer')
set('Machine', 'AdminServerMachine')
updateDomain()
closeDomain()
print('AdminServer is on AdminServerMachine')
