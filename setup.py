from setuptools import find_packages, setup

PACKAGE_NAME = 'ansible-output-parser'
PACKAGE_VERSION = '0.0.4'
DESCRIPTION = 'Parser for Ansible output'
with open('README.rst', 'r') as fileHandler:
    LONG_DESCRIPTION = fileHandler.read()

TEST_REQUIRES = [
    'flake8',
    'mypy',
    'pytest',
    'twine',
    'wheel',
]


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    url='https://github.com/RockProfile/Ansible-Output-Parser',
    author='Peter McDonald',
    author_email='admin@rockprofile.com',
    maintainer='Peter McDonald',
    maintainer_email='admin@rockprofile.com',
    classifiers='Development Status :: 4 - Beta',
    license='MIT',
    license_file='LICENSE',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    keywords='ansible',
    packages=find_packages(),
    package_dir={'ansible_parser': 'ansible_parser'},
    platforms='',
    provides='ansible_parser',
    extras_require={'test': TEST_REQUIRES},
)
