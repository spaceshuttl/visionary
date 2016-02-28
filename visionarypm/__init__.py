#!/usr/bin/python2

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

   
def generate(master_password, keyword):
    hashed = pyscrypt.hash(password = master_password, 
                           salt = keyword, 
                           N = 2048,
                           r = 1,
                           p = 1,
                           dkLen = 32)
    return hashed.encode('hex')[0:32]

def main(first_run=True):
    if first_run == True:
        print '%s\n' % (banner())
    master_password = getpass('Master password: ')
    if len(master_password) >= 8:
        print '' #line break for formatting
        while True:
            keyword = raw_input('Keyword: ')
            if not keyword: #No keyword specified exits program cleanly
                print '\nExiting...'
                break
            print 'Your password: %s\n' % (generate(master_password, keyword))
    else:
        print 'Password must be at least 8 characters.\n'
        main(False)        
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print '\nKeyboard Interrupt.'
