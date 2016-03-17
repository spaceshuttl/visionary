#!/usr/bin/python2

from getpass import getpass
import pyscrypt
import json

def banner():
    return """
                      _     _                              
               /\   /(_)___(_) ___  _ __   __ _ _ __ _   _ 
               \ \ / / / __| |/ _ \| '_ \ / _` | '__| | | |
                \ V /| \__ \ | (_) | | | | (_| | |  | |_| |
                 \_/ |_|___/_|\___/|_| |_|\__,_|_|   \__, |
                                     Password Manager|___/ """

   
def generate(master_password, keyword, cost=2048, oLen=32):
    hashed = pyscrypt.hash (
        password = master_password, 
        salt = keyword, 
        N = cost,
        r = 1,
        p = 1,
        dkLen = 32
    )
    generated = hashed.encode('hex')[0:oLen]

def get_keyword():
    try:
        return raw_input('Keyword: ')
    except EOFError:
        print 'Keyword unusable.\n'
        return get_keyword()
    except KeyboardInterrupt:
        print '\nKeyboard Interrupt.'
        print '\nExiting...'
        raise SystemExit

def init_defaults():
    cost = raw_input('CPU/memory cost parameter (default=2048): ')
    if cost:
        if cost > 0 and not (num & (num - 1)):
            if cost <= 16384:
                pass
            else:
                print 'Cost must be below ' #TODO
    else:
        cost = 2048

def setup():
    try:
        with open('visionarypm.conf') as f:
            config = json.loads(f.read())
        return {
            cost : config['cost'],
            oLen : config['oLen']
        }
    except IOError:
        f = open('visionarypm.conf', 'a+')
        

def main(first_run=False):
    if first_run == True:
        print '%s\n' % (banner())
    #parameters = setup() # Not enabled for now.
    master_password = getpass('Master password: ')
    if len(master_password) >= 8:
        print '' #line break for formatting
        while True:
            keyword = get_keyword()
            if keyword:
                print 'Your password: %s\n' % (generate(master_password, keyword))
            else:
                print '\nExiting...'
                raise SystemExit
    else:
        print 'Password must be at least 8 characters.\n'
        main() 
 
if __name__ == "__main__":
    try:
        main(True)
    except KeyboardInterrupt:
        print '\nKeyboard Interrupt.'
        print '\nExiting...'
