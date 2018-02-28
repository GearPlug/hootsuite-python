import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='hootsuite-python',
      version='0.1',
      description='API wrapper for HootSuite written in Python',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/hootsuite-python',
      author='Nerio Rincon',
      author_email='nrincon.mr@gmail.com',
      license='GPL',
      packages=['hootsuite'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
