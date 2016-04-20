#!/usr/bin/python2

from colorama import init, Fore, Style
from getpass import getpass
import pyscrypt
import json
import os


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


def err(text):
    return '%s%s%s' % (Fore.RED, text, Fore.RESET)


def settings(text):
    return '%s%s%s' % (Fore.YELLOW, text, Fore.RESET)


def password(text):
    return '%s%s%s' % (Fore.CYAN, text, Fore.RESET)


def safe_input(string):
    try:
        return raw_input(string)
    except EOFError:
        print err('Input unusable.\n')
        return safe_input(string)


def get_defaults():
    print 'Enter your preferred settings: (leave blank to accept defaults)\n'
    cost = safe_input('CPU/memory cost parameter [default=2048]: ')
    if cost:
        if cost.isdigit():
            cost = int(cost)
            if (cost & (cost - 1)) or (cost > 16384 or cost < 1024):
                print err('Input must be a positive power of 2 between 1024 and 16384.\n')
                return get_defaults()
        else:
            print err('Input must be a positive power of 2 between 1024 and 16384.\n')
            return get_defaults()
    else:
        cost = 2048
    oLen = safe_input('Length of generated passwords [default=32]: ')
    if oLen:
        if oLen.isdigit():
            oLen = int(oLen)
            if oLen > 64 or oLen < 16:
                print err('Input must be a positive integer between 16 and 64.\n')
                return get_defaults()
        else:
            print err('Input must be a positive integer between 16 and 64.\n')
            return get_defaults()
    else:
        oLen = 32
    print #line break for formatting
    return {"cost" : cost, "oLen" : oLen}


def getPath():
    try:
        return '%s/visionarypm.conf' % os.path.dirname(os.path.abspath(__file__))
    except:
        print err('\nCannot get path. Are you sure you\'re not running Visionary from IDLE?')
        raise SystemExit


def getConfig():
    try:
        with open(path) as f:
            config = json.loads(f.read().strip())
        return config, 0
    except IOError:
        config = get_defaults()
        print 'In order to save these settings, place %s' % settings(json.dumps(config))
        print 'in %s\n' % (settings(path))
        return config, 1


# Global parameters
params = {}
path = getPath()


# Initialise colours for multi-platform support.
init()


def interactive(first_run=True):
    if first_run == True:
        print """%s%s
                        _     _
                 /\   /(_)___(_) ___  _ __   __ _ _ __ _   _
                 \ \ / / / __| |/ _ \| '_ \ / _` | '__| | | |
                  \ V /| \__ \ | (_) | | | | (_| | |  | |_| |
                   \_/ |_|___/_|\___/|_| |_|\__,_|_|   \__, |
                                       Password Manager|___/\n
        """ % (Fore.WHITE, Style.BRIGHT) # Set global default colours.
        global params
        params, stat = getConfig()
        if stat == 0:
            print '[+] Cost factor: %s\n[+] Password length: %s\n[+] Config file: %s\n' % (settings(params['cost']),
                                                                                           settings(params['oLen']),
                                                                                           settings(path))
    master_password = getpass('Master password: ')
    master_password_confirm = getpass('Confirm master password: ')
    while master_password != master_password_confirm:
        print err('Passwords don\'t match!\n')
        master_password = getpass('Master password: ')
        master_password_confirm = getpass('Confirm master password: ')
    if len(master_password) >= 8:
        print #line break for formatting
        while True:
            keyword = safe_input('Keyword: ')
            if keyword:
                print 'Your password: %s\n' % (password(generate(master_password,
                                                                 keyword,
                                                                 params['cost'],
                                                                 params['oLen'])))
            else:
                print err('\nExiting...')
                raise SystemExit
    else:
        print err('Password must be at least 8 characters.\n')
        interactive(False)


def main():
    try:
        interactive()
    except KeyboardInterrupt:
        print err('\n\nKeyboard Interrupt')


if __name__ == "__main__":
    main()
