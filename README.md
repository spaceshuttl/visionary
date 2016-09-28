# Visionary Password Manager

 [![PyPI](https://img.shields.io/pypi/v/visionarypm.svg)](https://pypi.python.org/pypi/visionarypm) [![PyPI](https://img.shields.io/pypi/l/visionarypm.svg)](https://creativecommons.org/licenses/by/4.0/) [![Dependency Status](https://dependencyci.com/github/libeclipse/visionary/badge)](https://dependencyci.com/github/libeclipse/visionary)

Conventional password managers have a few flaws. They work by generating passwords, encrypting them with a master password, and then storing or syncing the encrypted passwords somewhere.

There are a few problems with this approach:

1. The encrypted data can be lost, thereby locking the user out of all of their accounts.
2. The encrypted data can be stolen. If the user was using a weak master password, all of their accounts can be compromised.
3. The data can only be synced to a limited number of devices.

**Visionary Password Manager** improves on these shortcomings considerably:

1. Your passwords are generated on-the-fly based on a pure algorithm. This means that the only thing that would make you lose your data is you forgetting your master password.
2. Nothing is stored so there's nothing to steal.
3. There are thousands of iterations of Scrypt, making brute-forcing infeasible.
4. No need to sync data, as there's nothing to sync! You can use this script or our API **(coming soon)** from anywhere in the world, and from any device, to generate your passwords.

## Installation

`~ >> pip install visionarypm`

or

`~ >> python -m pip install visionarypm`

## Usage

Just run:

`~ >> vpm`

in your command line. On your first run, you'll be prompted to enter your default settings (leave blank to accept defaults). A string will be generated that you can either auto-save or manually save to the specified location. This will remove the need to remember and enter your configuration every time. **Note that different values here will generate different passwords.**

You will be then be prompted for a master password (minimum 8 characters). This is what protects all of your generated passwords so make it a strong one. Next, a keyword. This can be anything, like 'github.com' or 'facebook' or even 'not_porn' for that special folder. A fingerprint will be generated and displayed. This is a string unique to your master password, and eliminates the need to re-enter it to ensure validity.

Three distinct passwords will be generated based on what you entered, a normal one, a complex one, and a readable one. You can then optionally copy one to your clipboard. Visionary will carry on asking for more keywords, so just leave it blank to exit.

Upon exit, Visionary clears your clipboard if you copied a password there, and advises you to exit your terminal to prevent scroll-back.

## Screenshot

![Screenshot](/images/screenshot.png "Screenshot")

## Troubleshooting

**"Does Visionary support both Python2 and Python3?"**

Yes.

**"I reinstalled Visionary and I want to change my default configuration."**

You should look inside the folder where Visionary is installed for a file called `visionarypm.conf`. Simply delete it and you should be prompted for a new configuration on the next run.

**"I have forgotten my configuration settings! Help!"**

If the configuration file has been deleted, then you'll have to guess. The possible configuration options are listed in the table below:

| Configuration field            | Possible values (inclusive) |
| :----------------------------: | :-------------------------: |
| Cost factor                    | 2^10 - 2^20                 |
| Password lengths               | 16 - 64                     |
| Words in readable password     | 4 - 16                      |

**"I have forgotten my password and/or keyword! Help!**

If you've forgotten your password, then you're pretty much screwed. When it comes to keywords, they're usually easy to guess. Most people use the website link or maybe something that reminds them of it.

**"The `vpm` command doesn't work for me."**

Make sure Python is properly configured and in your PATH. [How2](http://lmgtfy.com/?q=add+python+to+path)

**"Nothing is typed when I try to enter my master password."**

It's a security feature. Your password is being entered, you just can't see it.
