from setuptools import find_packages, setup

PACKAGE_NAME = 'Anislbe Output Parser'
PACKAGE_VERSION = '0.0.2'
DESCRIPTION = 'Parser for Ansible output'
with open('README.md', 'r') as fileHandler:
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
    url='',
    download_url='',
    project_urls={},
    author='Peter McDonald',
    author_email='me@petermcdonald.co.uk',
    maintainer='Peter McDonald',
    maintainer_email='me@petermcdonald.co.uk',
    classifiers='',
    license='MIT',
    license_file='LICENSE',
    license_files='LICENSE',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='',
    keywords='ansible',
    packages=find_packages(),
    package_dir={'ansible_parser': 'ansible_parser'},
    platforms='',
    provides='',
    requires='',
    extras_require={'test': TEST_REQUIRES},
    obsoletes='',
)
