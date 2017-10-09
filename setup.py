from setuptools import setup, find_packages

with open('READMY.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ManySync',
    version='0.1.0',
    description='Map your box.com folders to your desktop file system, the way you want!',
    long_description=readme,
    author='Raphael Gabbarelli',
    author_email='raphael@gabbarelli.it',
    url='https://github.com/raphaelgabbarelli/ManySync',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)