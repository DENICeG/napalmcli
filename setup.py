from setuptools import setup, find_packages

setup(
    name="napalmcli",
    version="0.0.1",
    description="command line interface for napalm",
    author="Thorsten Kohlhepp",
    author_email="kohlhepp at denic.de",
    url="https://github.com/DENICeG/napalmcli.git",
    packages=find_packages(),
    scripts=["bin/napalmcli.py"]
)
