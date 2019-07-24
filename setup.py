from setuptools import setup

# Get version number from main script
with open('./visionarypm/__init__.py') as f:
    for line in f:
        if '__version__' in line:
            __version__ = line.split('=')[1].replace('\'', '').strip()
            break

setup(name='visionarypm',
      version=__version__,
      description='A smarter password manager.',
      long_description='Manages your passwords without storing anything.',
      url='https://github.com/spaceshuttl/visionary',
      author='awnumar',
      license='MIT',
      packages=['visionarypm'],
      package_data={'': ['*.txt']},
      install_requires=["scrypt", "colorama", "pyperclip", "requests"],
      entry_points={'console_scripts': ['vpm = visionarypm:main']},
      keywords=['password', 'manager', 'visionary', 'visionarypm', 'vpm'],
      zip_safe=False)
