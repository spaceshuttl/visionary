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

   
def generate(master_password, keyword, N=2048, r=1, p=1, dkLen=32):
    hashed = pyscrypt.hash(password = master_password, 
                           salt = keyword, 
                           N = N,
                           r = r,
                           p = p,
                           dkLen = dkLen)
    return hashed.encode('hex')[0:32]

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

def main(first_run=False):
    if first_run == True:
        print '%s\n' % (banner())
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
