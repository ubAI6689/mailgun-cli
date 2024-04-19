from setuptools import setup, find_packages

setup(
    name='mailgun-cli',
    version='1.0.0',
    author='Abu Ubaidah',
    author_email='ub.AI6689@gmail.com',
    description='A CLI program to control Mailgun mailing lists',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mailgun=mailgun_cli.main:main',
        ],
    },
    install_requires=[
        'requests',
    ],
)