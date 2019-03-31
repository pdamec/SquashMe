import os
from setuptools import setup


readme = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
requirements = [req.strip() for req in open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).readlines()]

setup(
    name='squash-me',
    version='1.0.0',
    author='Patryk Damec',
    author_email='patryk.damec@gmail.com',
    packages=['squasher'],
    install_requires=requirements,
    license='',
    long_description=readme,
    entry_points={
        'console_scripts': ['sq-me=squasher.cli:main'],
    },
    test_suite="tests",
)
