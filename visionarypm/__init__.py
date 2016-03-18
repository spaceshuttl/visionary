#!/usr/bin/python2

from getpass import getpass
import pyscrypt
import json
import sys

def banner():
    return """
               _     _                              
        /\   /(_)___(_) ___  _ __   __ _ _ __ _   _ 
        \ \ / / / __| |/ _ \| '_ \ / _` | '__| | | |
         \ V /| \__ \ | (_) | | | | (_| | |  | |_| |
          \_/ |_|___/_|\___/|_| |_|\__,_|_|   \__, |
                              Password Manager|___/ 
    """
   
def generate(master_password, keyword, cost=2048, oLen=32):
    hashed = pyscrypt.hash (
        password = master_password, 
        salt = keyword, 
        N = cost,
        r = 1,
        p = 1,
        dkLen = 32
    )
    return hashed.encode('hex')[0:oLen]

def safe_input(string):
    try:
        return raw_input(string)
    except EOFError:
        print 'Input unusable.\n'
        return safe_input(string)
    except KeyboardInterrupt:
        print '\nKeyboard Interrupt.\n\nExiting...'
        raise SystemExit

def get_defaults():
    print 'Enter your preferred settings: (leave blank to accept defaults)\n'
    cost = safe_input('CPU/memory cost parameter [default=2048]: ')
    if cost:
        if cost.isdigit():
            cost = int(cost)
            if (cost & (cost - 1)) or (cost > 16384 or cost < 1024):
                print 'Input must be a positive power of 2 between 1024 and 16384.\n'
                return get_defaults()
        else:
            print 'Input must be a positive power of 2 between 1024 and 16384.\n'
            return get_defaults()
    else:
        cost = 2048
    oLen = safe_input('Length of generated passwords [default=32]: ')
    if oLen:
        if oLen.isdigit():
            oLen = int(oLen)
            if oLen > 64 or oLen < 16:
                print 'Input must be a positive integer between 16 and 64.\n'
                return get_defaults()
        else:
            print 'Input must be a positive integer between 16 and 64.\n'
            return get_defaults()
    else:
        oLen = 32
    print '' #line break for formatting
    return {"cost" : cost, "oLen" : oLen}

def getConfig():    
    try:
        with open(sys.path[0] + '/visionarypm.conf') as f:
            config = json.loads(f.read())
        return config
    except IOError:
        config = get_defaults()
        print 'In order to save these settings, place %s' % json.dumps(config)
        print 'in %s\n' % (sys.path[0] + '/visionarypm.conf')
        return config

def main(first_run=True):
    if first_run == True:
        print '%s\n' % (banner())
    params = getConfig()
    try: # Sometimes the installed version doesn't exit properly.
        master_password = getpass('Master password: ')
    except KeyboardInterrupt:
        print '\nKeyboard Interrupt.\n\nExiting...'
        raise SystemExit
    if len(master_password) >= 8:
        print '' #line break for formatting
        while True:
            keyword = safe_input('Keyword: ')
            if keyword:
                print 'Your password: %s\n' % (generate(master_password, keyword, params['cost'], params['oLen']))
            else:
                print '\nExiting...'
                raise SystemExit
    else:
        print 'Password must be at least 8 characters.\n'
        main(False) 
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print '\nKeyboard Interrupt.\n\nExiting...'
