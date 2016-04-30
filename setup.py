from setuptools import setup

setup(name='visionarypm',
      version='4.0.1',
      description='A smarter password manager.',
      url='https://github.com/libeclipse/visionary',
      author='libeclipse',
      author_email='libeclipse@gmail.com',
      license='GPLv3',
      packages=['visionarypm'],
      package_data = {'' : ['*.txt']},
      install_requires=["scrypt", "colorama", "pyperclip"],
      entry_points = {'console_scripts': ['vpm = visionarypm:main']},
      keywords = ['password', 'manager', 'visionary', 'visionarypm'],
      zip_safe=False)
