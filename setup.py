from setuptools import setup

setup(name='visionarypm',
      version='5.1.0',
      description='A smarter password manager.',
      long_description = 'Manages your passwords without storing anything.',
      url='https://github.com/libeclipse/visionary',
      author='libeclipse',
      author_email='libeclipse@gmail.com',
      license='GPLv3',
      packages=['visionarypm'],
      package_data = {'' : ['*.txt']},
      install_requires=["scrypt", "colorama", "pyperclip"],
      entry_points = {'console_scripts': ['vpm = visionarypm:main']},
      keywords = ['password', 'manager', 'visionary', 'visionarypm', 'vpm'],
      zip_safe=False)
