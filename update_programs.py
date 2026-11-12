import urllib
from globaldata import *

program = urllib.URLopener()

try:
    url = 'http://10.5.0.1:8000/'
    print url
    for program_name in GLOBALDATA_PROGRAMS:
        print 'updating %s' % program_name
        program.retrieve(url + program_name, PROGRAM_DIR + program_name)
except:
    if COMPUTER in ['TITAN', 'TITAN III', 'OTHER']:
        try:
            url = 'http://10.5.0.102:8000/'
            print url
            for program_name in GLOBALDATA_PROGRAMS:
                print 'updating %s' % program_name
                program.retrieve(url + program_name, PROGRAM_DIR + program_name)
        except:
            if COMPUTER in ['TITAN', 'OTHER']:
                try:
                    url = 'http://10.5.0.103:8000/'
                    print url
                    for program_name in GLOBALDATA_PROGRAMS:
                        print 'updating %s' % program_name
                        program.retrieve(url + program_name, PROGRAM_DIR + program_name)
                except:
                    print 'Cannot find server with updated programs'
    else:
        try:
            url = 'http://10.5.0.103:8000/'
            print url
            for program_name in GLOBALDATA_PROGRAMS:
                print 'updating %s' % program_name
                program.retrieve(url + program_name, PROGRAM_DIR + program_name)
        except:
            print 'Cannot find server with updated programs'
print '%s updated' % program_name