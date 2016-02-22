#!/usr/bin/python2

import hashlib
from getpass import getpass

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

def interactive():
    master_password = getpass('Master password: ')
    reenter_master_password = getpass('Re-enter master password: ')
    if master_password == reenter_master_password:
        keyword = raw_input('Keyword: ')
        print '\nYour password: %s' % (generate(master_password, keyword))
    else:
        print 'Passwords don\'t match!\n'
        interactive()
    
def generate(master_password, keyword):
    password = sha256(sha256(master_password)+sha256(keyword))
    for iteration in range(500000):
        password = sha256(password)
    return password    

def main():
    print '%s\n' % (banner())
    interactive()    
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print '\nKeyboard Interrupt.'
        raise SystemExit
