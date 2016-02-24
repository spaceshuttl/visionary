#!/usr/bin/python2

import hashlib
import re
from getpass import getpass
import pyscrypt

def banner():
    return """
                      _     _                              
               /\   /(_)___(_) ___  _ __   __ _ _ __ _   _ 
               \ \ / / / __| |/ _ \| '_ \ / _` | '__| | | |
                \ V /| \__ \ | (_) | | | | (_| | |  | |_| |
                 \_/ |_|___/_|\___/|_| |_|\__,_|_|   \__, |
                                     Password Manager|___/ """

def sha256(s):
    return hashlib.sha256(s).hexdigest()

    
def generate(master_password, keyword):
    hashed = pyscrypt.hash(password = master_password, 
                           salt = keyword, 
                           N = 4096,
                           r = 1,
                           p = 1,
                           dkLen = 32)
    return hashed.encode('hex')[0:32]

def strong(password):
    if len(password) >= 12:
        if re.search(r'\d', password):
            if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
                return True
            else:
                return 'Password must be a mix of uppercase and lowercase characters.'
        else:
            return 'Password must contain digits.'
    else:
        return 'Password must be at least 12 characters long.'

def main(first_run=True):
    if first_run == True:
        print '%s\n' % (banner())
    master_password = getpass('Master password: ')
    if strong(master_password) == True:
        keyword = raw_input('Keyword: ')
        print '\nYour password: %s' % (generate(master_password, keyword))
    else:
        print '%s\n' % (strong(master_password))
        main(False)        
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print '\nKeyboard Interrupt.'
