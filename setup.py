from setuptools import setup, find_packages

setup(
    name="JABA",
    version="1.0",
    author="Erik Terres",
    author_email="erik.terres.es@gmail.com",
    description="Social Network message analyzer",
    url="https://github.com/futotta-risu/JABA",
    
    packages=['JABA'],
    extras_require=dict(tests=['tests']),
    python_requires=">=3.8",
)