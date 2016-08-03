#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals
import codecs

from colorama import init, Fore, Style
import pyperclip
import os, sys
import scrypt
import json
import math


# Fixes getpass bug affecting Python 2.7 on Windows
if sys.version_info < (3,) and os.name == 'nt':
    from getpass import getpass as _getpass
    def getpass(s):
        return _getpass(s.encode('utf8'))
else:
    from getpass import getpass


def safe_input(string):
    try:
        return str(input(string))
    except EOFError:
        print(output('Input unusable.\n', Fore.RED))
        return safe_input(string)


def get_defaults(first_run=True):
    if first_run:
        print('\nEnter your preferred settings: (bigger is better)\n')
    else:
        print()  #line break for formatting
    cost = safe_input('Cost factor [default=14]: 2^')
    if cost:
        if cost.isdigit():
            cost = int(cost)
            if cost < 10 or cost > 20:
                print(output('Input must be a positive integer between 10 and 20.', Fore.RED))
                return get_defaults(False)
        else:
            print(output('Input must be a positive integer between 10 and 20.', Fore.RED))
            return get_defaults(False)
    else:
        cost = 14
    oLen = safe_input('Length of generated passwords [default=32]: ')
    if oLen:
        if oLen.isdigit():
            oLen = int(oLen)
            if oLen > 64 or oLen < 16:
                print(output('Input must be a positive integer between 16 and 64.', Fore.RED))
                return get_defaults(False)
        else:
            print(output('Input must be a positive integer between 16 and 64.', Fore.RED))
            return get_defaults(False)
    else:
        oLen = 32
    nwords = safe_input('Number of words in a readable password [default=6]: ')
    if nwords:
        if nwords.isdigit():
            nwords = int(nwords)
            if nwords > 16 or oLen < 4:
                print(output('Input must be a positive integer between 4 and 16.', Fore.RED))
                return get_defaults(False)
        else:
            print(output('Input must be a positive integer between 4 and 16.', Fore.RED))
            return get_defaults(False)
    else:
        nwords = 6
    print()  #line break for formatting
    return {"cost" : cost, "oLen" : oLen, "nwords" : nwords}


def getPath():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except:
        exit_protocol('ERROR: Cannot get path. Are you sure you\'re not running Visionary from IDLE?')


def getConfig():
    try:
        with open('%s/visionarypm.conf' % path) as f:
            config = json.loads(f.read().strip())
        if config['oLen'] < 16 or config['oLen'] > 64 or config['cost'] < 10 or config['cost'] > 20 or config['nwords'] > 16 or config['nwords'] < 4:
            exit_protocol('Invalid config! Please delete the configuration file (%s) and a new one will be generated on the next run.' % (path + '/visionarypm.conf'))
        return config, 0
    except IOError:
        config = get_defaults()
        autosave = safe_input('Do you want to save this config? (Y/n) ').lower()
        if autosave == 'yes' or autosave == 'y' or autosave == '':
            print('\nAutosaving configuration...')
            try:
                with open('%s/visionarypm.conf' % path, 'a') as f:
                    f.write(json.dumps(config))
                return config, 0
            except:
                print(output('Autosaving failed! (Permission denied)\n', Fore.RED))
                print('In order to save these settings, place %s' % output(json.dumps(config), Fore.YELLOW))
                print('in %s' % (output('%s/visionarypm.conf' % path, Fore.YELLOW)))
        return config, 1
    except (KeyError, json.decoder.JSONDecodeError):
        exit_protocol('Invalid config! Please delete the configuration file (%s) and a new one will be generated on the next run.' % (path + '/visionarypm.conf'))


def generate(master_password, keyword, cost, oLen=None):
    hashed = codecs.encode(scrypt.hash(password = master_password,
                                       salt = keyword,
                                       N = 1 << cost,
                                       buflen=64),
                           'hex').decode('utf-8')
    if oLen:
        hashed = hashed[0:oLen]
    return hashed


def generate_readable(master_password, keyword, cost, num_words=None):
    if not num_words:
        num_words = params['nwords']
    dict_len = len(words)
    entropy_per_word = math.log(dict_len, 2)
    hash = generate(master_password, keyword, cost)
    available_entropy = len(hash) * 4
    hash = int(hash, 16)
    if (num_words * entropy_per_word) > available_entropy:
        raise Exception("The output entropy of the specified hashfunc (%d) is too small." % available_entropy)
    phrase = []
    for i in range(num_words):
        remainder = hash % dict_len
        hash = hash // dict_len
        phrase.append(words[int(remainder)].strip().decode('utf-8'))
    return " ".join(phrase).lower().capitalize()


def copy_to_clipboard(generated):
    global copied
    selection = safe_input('Which password would you like to copy? (1/2) ').strip()
    if selection == '1':
        password = generated[0]
    elif selection == '2':
        password = generated[1]
    else:
        print(output('Invalid option. Pick either 1 or 2.\n', Fore.RED))
        return copy_to_clipboard(generated)
    try:
        pyperclip.copy(password)
        copied = True
        print('\nCopied!\n')
        return
    except pyperclip.exceptions.PyperclipException:
        print(output('Could not copy! If you\'re using linux, make sure xclip is installed.\n', Fore.RED))


def output(text, color):
    return '%s%s%s' % (color, text, Fore.RESET)


def exit_protocol(msg=''):
    if copied:
        pyperclip.copy('')
    if msg:
        print(output('\n%s' % msg, Fore.RED))
    print(output('\nExiting securely... You are advised to close this terminal.', Fore.RED))
    raise SystemExit


def interactive(first_run=True):
    if first_run:
        print("""%s%s
                        _     _
                 /\   /(_)___(_) ___  _ __   __ _ _ __ _   _
                 \ \ / / / __| |/ _ \| '_ \ / _` | '__| | | |
                  \ V /| \__ \ | (_) | | | | (_| | |  | |_| |
                   \_/ |_|___/_|\___/|_| |_|\__,_|_|   \__, |
                                       Password Manager|___/\n
        """ % (Fore.WHITE, Style.BRIGHT)) # Set global default colours.
        print(output('  Please report any issues at https://github.com/libeclipse/visionary/issues', Fore.YELLOW))
        global params
        params, stat = getConfig()
        if stat == 0:
            print("""
[+] Cost factor: 2^%s
[+] Length of conventional password: %s
[+] Words in readable password: %s
[+] Config file: %s""" % (output(params['cost'], Fore.YELLOW),
                          output(params['oLen'], Fore.YELLOW),
                          output(params['nwords'], Fore.YELLOW),
                          output('%s/visionarypm.conf' % path, Fore.YELLOW)))
    print()  #line break for formatting
    master_password = getpass('Master password: ')
    if len(master_password) >= 8:
        # Fingerprint confirms to the user that they entered the correct master password.
        fingerprint = generate_readable(master_password,
                                        b'',
                                        params['cost'],
                                        5)
        print('Fingerprint: %s\n' % output(fingerprint, Fore.YELLOW))
        while True:
            keyword = safe_input('Keyword: ')
            if keyword:
                # Generate password
                conventional = generate(master_password,
                                        keyword,
                                        params['cost'],
                                        params['oLen'])
                readable = generate_readable(master_password,
                                             keyword,
                                             params['cost'])
                generated = [conventional, readable]
                print('\n[%s] Conventional password: %s' % (output('1', Fore.YELLOW), output(generated[0], Fore.CYAN)))
                print('[%s] Readable password: %s\n' % (output('2', Fore.YELLOW), output(generated[1], Fore.CYAN)))
                # Copy to clipboard
                confirm = safe_input('Would you like to copy a password to the clipboard? (Y/n) ').lower().strip()
                if confirm == 'yes' or confirm == 'y' or confirm == '':
                    copy_to_clipboard(generated)
                else:
                    print()  #line break for formatting
            else:
                exit_protocol()
                raise SystemExit
    else:
        print(output('Password must be at least 8 characters.', Fore.RED))
        interactive(False)


# Initialise colours for multi-platform support.
init()

# Initialise input for multi-version support.
try:
    input = raw_input
except NameError:
    pass

# Global parameters
params = {}
path = getPath()
copied = False
with open('%s/words.txt' % path, 'rb') as f:
    words = f.read().splitlines()


def main():
    try:
        interactive()
    except KeyboardInterrupt:
        exit_protocol('\nKeyboard Interrupt')
    except Exception as e:
        exit_protocol('ERROR: %s\n\nPlease report this error at https://github.com/libeclipse/visionary/issues' % repr(e))


if __name__ == "__main__":
    main()
