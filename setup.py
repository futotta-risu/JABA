from setuptools import setup, find_packages

setup(name="JABA", packages=find_packages(where='JABA'),extras_require=dict(tests=['tests']))