# Visionary Password Manager

Conventional password managers have many flaws. They work by generating passwords, encrypting them with a master password, and then storing or syncing the encrypted passwords somewhere.

There are a few problems with this approach:

1. The encrypted data can be lost, thereby locking the user out of all of their accounts.
2. The encrypted data can be stolen. If the user was using a weak master password, all of their accounts can be compromised.
3. The data can only be synced to a limited number of devices.

**Visionary Password Manager** improves on these shortcomings considerably:

1. Your passwords are generated on-the-fly based on a pure algorithm. This means that the only thing that would make you lose your data is you forgetting your master password.
2. Nothing is stored so there's nothing to steal.
3. There are thousands of iterations, which makes brute-forcing infeasible.
4. No need to sync data, as there's nothing to sync! You can use this script or our API *(coming soon)* from anywhere in the world, and from any device, to generate your passwords.

###NOT YET READY FOR USE!

##Installation:

###Option 1: pip

**Install using pip in order to get the latest stable release.**

`pip2 install visionarypm`

or

`python2 -m pip install visionarypm`

###Option 2: git clone

**Install using git to be at the bleeding edge. You'll receive the latest commit.**

```
git clone https://github.com/libeclipse/visionary.git
cd visionary
python2 setup.py install
```

##Usage:

```
~ » visionarypm

                      _     _                              
               /\   /(_)___(_) ___  _ __   __ _ _ __ _   _ 
               \ \ / / / __| |/ _ \| '_ \ / _` | '__| | | |
                \ V /| \__ \ | (_) | | | | (_| | |  | |_| |
                 \_/ |_|___/_|\___/|_| |_|\__,_|_|   \__, |
                                     Password Manager|___/ 

Master password: 
Keyword: github.com

Your password: 226ee1bddf2cfb0b805a0ebaa185f2ec3092937919fd76e3bc1ff22abecb9f61
```

###Screenshot:

![Screenshot](https://github.com/libeclipse/visionary/blob/master/images/screenshot.png "Screenshot")

[![forthebadge](http://forthebadge.com/images/badges/built-with-swag.svg)](http://forthebadge.com)

**Support development by donating ฿itcoins: 1ECLipSrTyitXJbeNBZVRMcRHp94HryZkj**
