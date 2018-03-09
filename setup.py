from setuptools import find_packages, setup


with open('VERSION', 'r') as f:
    version = f.read().strip()


setup(
    name='isc-style-guide',
    packages=find_packages(),
    include_package_data=True,
    description='Custom checkers for Pylint that enforce InfoScout Python style',
    url='http://github.com/infoscout/isc-style-guide',
    version=version,
    install_requires=['pylint'],
    test_suite='tests'
)
