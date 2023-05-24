from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mvl/__init__.py
from mvl import __version__ as version

setup(
	name="mvl",
	version=version,
	description="CLMS ",
	author="veeramayandi.p@groupteampro.com",
	author_email="veeramayandi.p@groupteampro.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
