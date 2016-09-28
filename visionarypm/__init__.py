#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

from colorama import init, Fore, Style
import pyperclip, requests, scrypt
import codecs, json, math, string
import os, sys


# Fixes getpass bug affecting Python 2.7 on Windows
if sys.version_info < (3,) and os.name == 'nt':
    from getpass import getpass as _getpass
    def getpass(s):
        return _getpass(s.encode('utf8'))
else:
    from getpass import getpass


__version__ = '6.3.3'


def check_for_update():
    latest_info = requests.get('https://pypi.python.org/pypi/visionarypm/json')
    if latest_info.status_code == 200:
        try:
            latest_version = json.loads(latest_info.text)['info']['version']
        except ValueError: # PyPi returned something weird
            pass
        if latest_version != __version__:
            print(color('\nUpgrade [%s --> %s] available; install with `pip install -U visionarypm`' % (__version__, latest_version), Fore.RED))
    return


def safe_input(string):
    try:
        return str(input(string))
    except EOFError:
        print(color('Input unusable.\n', Fore.RED))
        return safe_input(string)


def get_defaults(first_run=True):
    if first_run:
        print('\nEnter your preferred settings: [bigger is better]\n')
    else:
        print()  #line break for formatting
    cost = safe_input('Cost factor [default=14]: 2^')
    if cost:
        if cost.isdigit():
            cost = int(cost)
            if cost < 10 or cost > 20:
                print(color('Input must be a positive integer between 10 and 20.', Fore.RED))
                return get_defaults(False)
        else:
            print(color('Input must be a positive integer between 10 and 20.', Fore.RED))
            return get_defaults(False)
    else:
        cost = 14
    oLen = safe_input('Length of generated passwords [default=32]: ')
    if oLen:
        if oLen.isdigit():
            oLen = int(oLen)
            if oLen > 64 or oLen < 16:
                print(color('Input must be a positive integer between 16 and 64.', Fore.RED))
                return get_defaults(False)
        else:
            print(color('Input must be a positive integer between 16 and 64.', Fore.RED))
            return get_defaults(False)
    else:
        oLen = 32
    nwords = safe_input('Number of words in a readable password [default=6]: ')
    if nwords:
        if nwords.isdigit():
            nwords = int(nwords)
            if nwords > 16 or oLen < 4:
                print(color('Input must be a positive integer between 4 and 16.', Fore.RED))
                return get_defaults(False)
        else:
            print(color('Input must be a positive integer between 4 and 16.', Fore.RED))
            return get_defaults(False)
    else:
        nwords = 6
    print()  #line break for formatting
    return {"cost" : cost, "oLen" : oLen, "nwords" : nwords}


def getPath():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except:
        exit('ERROR: Cannot get path. Are you sure you\'re not running Visionary from IDLE?')


def getConfig():
    try:
        with open('%s/visionarypm.conf' % path) as f:
            config = json.loads(f.read().strip())
        if config['oLen'] < 16 or config['oLen'] > 64 or config['cost'] < 10 or config['cost'] > 20 or config['nwords'] > 16 or config['nwords'] < 4:
            exit('Invalid config! Please delete the configuration file (%s) and a new one will be generated on the next run.' % (path + '/visionarypm.conf'))
        return config, 1
    except IOError:
        config = get_defaults()
        autosave = safe_input('Do you want to save this config? (Y/n) ').lower()
        if autosave == 'yes' or autosave == 'y' or autosave == '':
            print('\nAutosaving configuration...')
            try:
                with open('%s/visionarypm.conf' % path, 'a') as f:
                    f.write(json.dumps(config))
                return config, 1
            except:
                print(color('Autosaving failed! [Permission denied]\n', Fore.RED))
                print('In order to save these settings, place %s' % color(json.dumps(config), Fore.YELLOW))
                print('in %s' % (color('%s/visionarypm.conf' % path, Fore.YELLOW)))
        return config, 0
    except (KeyError, json.decoder.JSONDecodeError):
        exit('Invalid config! Please delete the configuration file (%s) and a new one will be generated on the next run.' % (path + '/visionarypm.conf'))


def generate(master_password, keyword, cost, oLen=None, num_words=None):

    if not num_words:
        num_words = params['nwords']

    def normal_password():
        seed = scrypt.hash(password=master_password,
                           salt=keyword,
                           N=1<<cost,
                           buflen=64)
        return codecs.encode(seed, 'hex').decode('utf-8')

    normal = normal_password()

    # Courtesy of rubik
    def complex_password():
        # A random shuffle of string.punctuation + string.ascii_uppercase
        to_add = '*>OI+D~}E{AF"`KXR\[J:-&#BQWN;$%TGPZ.=U,_HS()@L\'|<M]YCV/?!^'
        required = (string.ascii_lowercase,
                    string.ascii_uppercase,
                    string.digits,
                    string.punctuation)

        def nth_perm(S, n):
            '''Compute the n-th lexicographic permutation of the alphabet S.'''
            p = []
            for l in range(len(S) - 1, -1, -1):
                i, n = divmod(n, math.factorial(l))
                p.append(S[i])
                S = S[:i] + S[i + 1:]
            return p

        res = []
        perm_number = len(keyword) * sum(map(ord, keyword))
        chosen_perm = nth_perm(to_add, perm_number % math.factorial(len(to_add)))
        for i, c in enumerate(normal):
            # 2/3 of the original is preserved
            if i % 3:
                res.append(c)
                continue
            # We index from the bottom of the string, because that's where the
            # permutation changes most
            res.append(chosen_perm[-((i + len(keyword)) % len(to_add) + 1)])
        # There's a little possibility that the required chars aren't there
        for i, req in enumerate(required):
            if not set(req).intersection(res):
                res[i] = req[len(keyword) % len(req)]
        return ''.join(res)

    def readable_password():
        dict_len = len(words)
        entropy_per_word = math.log(dict_len, 2)
        available_entropy = len(normal) * 4
        phrase, seed = [], int(normal, 16)
        for i in range(num_words):
            remainder = seed % dict_len
            seed = seed // dict_len
            phrase.append(words[int(remainder)].strip().decode('utf-8'))
        return " ".join(phrase).lower().capitalize()

    complex = complex_password()
    readable = readable_password()

    if oLen:
        normal = normal[0:oLen]
        complex = complex[0:oLen]

    return [normal, complex, readable]


def copy_to_clipboard(generated):
    global copied
    selection = safe_input('Which password would you like to copy? [1/2/3] ').strip()
    if selection in ['1', '2', '3']:
        password = generated[int(selection) - 1]
    else:
        print(color('Invalid option. Pick either 1, 2 or 3.\n', Fore.RED))
        return copy_to_clipboard(generated)
    try:
        pyperclip.copy(password)
        copied = True
        print('\nCopied!\n')
    except pyperclip.exceptions.PyperclipException:
        print(color('Could not copy! If you\'re using linux, make sure xclip is installed.\n', Fore.RED))


def color(text, color):
    return '%s%s%s' % (color, text, Fore.RESET)


def exit(msg=''):
    if copied:
        pyperclip.copy('')
    if msg:
        print(color('\n%s' % msg, Fore.RED))
    print(color('\nExiting securely... You are advised to close this terminal.', Fore.RED))
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
        print(color('  Please report any issues at https://github.com/libeclipse/visionary/issues', Fore.YELLOW))
        # Check for update
        check_for_update()
        # Grab configuration
        global params
        params, saved = getConfig()
        print("""
[+] Cost factor: 2^%s
[+] Length of passwords: %s
[+] Words in readable password: %s""" % (color(params['cost'], Fore.YELLOW),
                                         color(params['oLen'], Fore.YELLOW),
                                         color(params['nwords'], Fore.YELLOW)))
        if saved:
            print("[+] Config file: %s" % color('%s/visionarypm.conf' % path, Fore.YELLOW))
    print()  #line break for formatting
    master_password = getpass('Master password: ')
    if len(master_password) >= 8:
        # Fingerprint confirms to the user that they entered the correct master password.
        fingerprint = generate(master_password, b'', params['cost'], num_words=5)[2]
        print('Fingerprint: %s\n' % color(fingerprint, Fore.YELLOW))
        while True:
            keyword = safe_input('Keyword: ')
            if keyword:
                # Generate passwords
                generated = generate(master_password, keyword, params['cost'], oLen=params['oLen'])
                print('\n[%s] Normal password: %s' % (color('1', Fore.YELLOW), color(generated[0], Fore.CYAN)))
                print('[%s] Complex password: %s' % (color('2', Fore.YELLOW), color(generated[1], Fore.CYAN)))
                print('[%s] Readable password: %s\n' % (color('3', Fore.YELLOW), color(generated[2], Fore.CYAN)))
                # Copy to clipboard
                confirm = safe_input('Would you like to copy a password to the clipboard? [Y/n] ').lower().strip()
                if confirm == 'yes' or confirm == 'y' or confirm == '':
                    copy_to_clipboard(generated)
                else:
                    print()  #line break for formatting
            else:
                exit()
    else:
        print(color('Password must be at least 8 characters.', Fore.RED))
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
        exit('\nKeyboard Interrupt')
    #except Exception as e:
    #    exit('ERROR: %s\n\nPlease report this error at https://github.com/libeclipse/visionary/issues' % repr(e))


if __name__ == "__main__":
    main()
