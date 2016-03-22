# Visionary Password Manager

Conventional password managers have many flaws. They work by generating passwords, encrypting them with a master password, and then storing or syncing the encrypted passwords somewhere.

There are a few problems with this approach:

1. The encrypted data can be lost, thereby locking the user out of all of their accounts.
2. The encrypted data can be stolen. If the user was using a weak master password, all of their accounts can be compromised.
3. The data can only be synced to a limited number of devices.

**Visionary Password Manager** improves on these shortcomings considerably:

1. Your passwords are generated on-the-fly based on a pure algorithm. This means that the only thing that would make you lose your data is you forgetting your master password.
2. Nothing is stored so there's nothing to steal.
3. There are thousands of iterations of Scrypt, making brute-forcing infeasible.
4. No need to sync data, as there's nothing to sync! You can use this script or our API **(coming soon)** from anywhere in the world, and from any device, to generate your passwords.

##Installation:

####*Compatable with Python2 only, and optimised for Linux*.

###Option 1: pip

**Install using pip in order to get the latest stable release.**

`~ >> pip install visionarypm`

or

`~ >> python -m pip install visionarypm`

###Option 2: git clone

**Install using git to be at the bleeding edge. You'll receive the latest commit.**

```
~ >> git clone https://github.com/libeclipse/visionary.git
~ >> cd visionary
~ >> python setup.py install
```

##Usage:

Just run:

`~ >> visionarypm`

in your command line. On your first run, you'll be prompted to enter your default settings (leave blank to accept defaults). A string will be generated that you can save to the specified location. This will remove the need to remember and enter your configuration every time. **Note that different values here will generate different passwords.**

You will be then be prompted for a master password (minimum 8 characters). This is what protects all of your generated passwords so make it a strong one. Next, a keyword. This can be anything, like 'github.com' or 'facebook' or even 'not_porn' for that special folder.

A strong password will be generated based on what you entered (depending on your configuration). Visionary will carry on asking for more keywords, so just leave it blank to exit.

It's also possible to import visionarypm into your own scripts:

```
import visionarypm

my_password = visionarypm.generate('master_password', 'keyword')
```

And even specify the CPU/Memory cost parameter and the generated password's length:

`my_password = visionarypm.generate('master_password', 'keyword', cost=4096, oLen=48)`

The defaults are 2048 and 32, respectively. The maximum password length is 64 characters.

###Screenshot:

![Screenshot](https://github.com/libeclipse/visionary/blob/master/images/screenshot.png "Screenshot")

###Troubleshooting:

**"I reinstalled Visionary and I want to change my default configuration."**

You should look inside the folder where Visionary is installed for a file called `visionarypm.conf`. Simply delete it and you should be prompted for a new configuration on the next run.

**"I have forgotton my configuration settings! Help!"**

If the configuration file has been deleted, then you'll have to guess. Luckily, there's not too many possible configurations.

Possible cost factors are `1024, 2048, 4096, 8192, 16384`, and the possible password lengths are 16-64 inclusive.

**"I have forgotton my password and/or keyword! Help!**

If you've forgotton your password, then you're pretty much screwed. When it comes to keywords, they're usually easy to guess. Most people use the website link or maybe something that reminds them of it.

**"The `visionarypm` command doesn't work for me."**

Make sure Python is in properly configured and in your PATH. [How2](http://lmgtfy.com/?q=add+python+to+path)

[![forthebadge](http://forthebadge.com/images/badges/built-with-swag.svg)](http://forthebadge.com)

**Support development by donating ฿itcoins: 1ECLipSrTyitXJbeNBZVRMcRHp94HryZkj**

*"You store your passwords in plaintext?! Na mate, it's double ROT13 encryption."*
