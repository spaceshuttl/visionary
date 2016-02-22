from setuptools import setup

setup(name='visionarypm',
      version='0.1',
      description='A smarter password manager.',
      url='https://github.com/libeclipse/visionary',
      author='libeclipse',
      author_email='libeclipse@gmail.com',
      license='GPLv3',
      packages=['visionarypm'],
      entry_points = {'console_scripts': ['visionarypm = visionarypm:main']},
      zip_safe=False)
