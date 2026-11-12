
import os
import getpass


userName = getpass.getuser()
# print userName
user = os.environ.get('USERNAME')
print user, userName
