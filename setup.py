from setuptools import setup

setup(
      name='FreeCAD-SEA',
      version='0.0',
      description="Statistical Energy Analysis module for FreeCAD.",
      long_description=open('README.txt').read(),
      author='Frederik Rietdijk',
      author_email='fridh@fridh.nl',
      license='LICENSE.txt',
      packages=['Sea'],
      zip_safe=False,
      install_requires=[
          'numpy',
          ],
      )