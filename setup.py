from setuptools import setup, find_packages

setup(
    name="JABA",
    packages=['JABA'],
    extras_require=dict(tests=['tests'])
)