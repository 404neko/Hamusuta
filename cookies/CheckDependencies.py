import os

#check depends needed by pipeline
COMMANDS = ['gifsicle --help', 'gifdiff --help']

for a_command in COMMANDS:
    v_return=os.system(a_command)
    if v_return==0:
        print a_command+' ............ [OK]'
    else:
        print '\n\n\n'+a_command+' ............ [FAIL]'
        break